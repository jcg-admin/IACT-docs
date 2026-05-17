8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_AUTH_02 — flujo principal

 @startuml

 actor Usuario as Usuario
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "LogoutEndpoint" as Logoutview
 participant "AuthService" as Authservice
 database "Base de Datos\n(analitica)" as BaseDeDatos
 database "Blacklist\n(cache/BD)" as Blacklist

 Usuario -> InterfazDeUsuario: Click "Cerrar sesion"
 InterfazDeUsuario -> InterfazDeUsuario: Confirm (modal opcional)
 InterfazDeUsuario -> Logoutview: POST /api/auth/logout/\nAuthorization: Bearer ...

 Logoutview -> Logoutview: Validar JWT (CNST-009)
 alt Token invalido
   Logoutview --> InterfazDeUsuario: 401 INVALID_TOKEN
 else Token valido
   Logoutview -> Authservice: logout(user_id, session_id)

   group Transaccion atomica
     Authservice -> BaseDeDatos: consultar Session WHERE\n  session_id=? AND state='ACTIVE'
     BaseDeDatos --> Authservice: session
     Authservice -> BaseDeDatos: actualizar Session SET\n  state='CLOSED',\n  close_reason='USER_LOGOUT',\n  closed_at=marca_tiempo_actual
     Authservice -> Blacklist: registrar BlacklistedToken\n  (access + refresh)
     Authservice -> BaseDeDatos: registrar AuditEvent\n  (event_type='LOGOUT')
   end

   Authservice --> Logoutview: success
   Logoutview --> InterfazDeUsuario: 200 OK\n{"message": "Sesion cerrada"}
   InterfazDeUsuario -> InterfazDeUsuario: limpia almacenamiento local\nlimpia Gestor de Estado
   InterfazDeUsuario --> Usuario: Redirect /login
 end

 @enduml

