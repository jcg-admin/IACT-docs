8.2 Diagrama de secuencia
=========================

Vista temporal del flujo principal con los
participantes principales del backend.

.. uml::
 :caption: UC_AUTH_01 — secuencia del flujo principal

 @startuml

 actor       Usuario as Usuario
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "Servicio de Autenticacion" as ServicioDeAutenticacion
 participant "AuthService" as Authservice
 database    "Base de Datos\n(User, Session,\nAuditEvent)" as BaseDeDatos

 Usuario -> InterfazDeUsuario : POST /login\n{username, password}
 activate InterfazDeUsuario

 InterfazDeUsuario -> ServicioDeAutenticacion : POST /api/auth/login/
 activate ServicioDeAutenticacion

 ServicioDeAutenticacion -> ServicioDeAutenticacion : Serializer.validate()\n(CNST-012)
 ServicioDeAutenticacion -> ServicioDeAutenticacion : throttle_check()\n(CNST-011)

 ServicioDeAutenticacion -> BaseDeDatos : consultar User donde\nusername = ?
 BaseDeDatos --> ServicioDeAutenticacion : User

 alt User no existe
   ServicioDeAutenticacion --> InterfazDeUsuario : 401 INVALID_CREDENTIALS
   ServicioDeAutenticacion -> BaseDeDatos : registrar AuditEvent\nLOGIN_FAILED
 else User existe
   ServicioDeAutenticacion -> Authservice : authenticate(user, password)
   activate Authservice
   Authservice -> Authservice : verificarHash()
   alt password incorrecto
     Authservice --> ServicioDeAutenticacion : invalid
     ServicioDeAutenticacion --> InterfazDeUsuario : 401 INVALID_CREDENTIALS
     ServicioDeAutenticacion -> BaseDeDatos : registrar AuditEvent\nLOGIN_FAILED
   else password correcto
     Authservice --> ServicioDeAutenticacion : valid
     deactivate Authservice

     ServicioDeAutenticacion -> BaseDeDatos : BEGIN TRANSACTION
     ServicioDeAutenticacion -> BaseDeDatos : actualizar Session\nSET state='CLOSED'\nWHERE user_id=X\nAND state='ACTIVE'
     ServicioDeAutenticacion -> BaseDeDatos : registrar AuditEvent\nSESSION_CLOSED (n)
     ServicioDeAutenticacion -> BaseDeDatos : registrar Session\n(state='ACTIVE')
     ServicioDeAutenticacion -> BaseDeDatos : registrar AuditEvent\nLOGIN
     ServicioDeAutenticacion -> BaseDeDatos : actualizar User\nSET last_login_at=marca_tiempo_actual
     ServicioDeAutenticacion -> BaseDeDatos : COMMIT

     ServicioDeAutenticacion -> ServicioDeAutenticacion : generate_jwt_tokens()
     ServicioDeAutenticacion --> InterfazDeUsuario : 200 OK\n{tokens, user, session}
   end
 end
 deactivate ServicioDeAutenticacion

 InterfazDeUsuario -> InterfazDeUsuario : store tokens
 InterfazDeUsuario --> Usuario : redirect to landing
 deactivate InterfazDeUsuario

 note over BaseDeDatos
   CNST-003: Session persistida en BaseDeDatos
   CNST-004: sesion unica
   CNST-005: expires_at = marca_tiempo_actual + 15 min
   CNST-025: AuditEvent inmutable
 end note

 @enduml

