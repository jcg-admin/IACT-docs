.. _uc-auth-01-parte-08:

==================================
Parte 8 — Diagramas UML
==================================

Cuatro diagramas PlantUML que cubren las cuatro
vistas canonicas del UC: caso de uso (estatica),
secuencia (dinamica temporal), actividad
(dinamica de control de flujo) y estados (ciclo
de vida de la ``Session``).

Politica del proyecto: PlantUML obligatorio (no
Mermaid). Estilos centralizados en
``_static/plantuml-styles.puml``.

8.1 Diagrama de caso de uso
===========================

Vista estatica de actores y relaciones
inter-UC. Per UML_07 y la decision DEC-A06,
UC_AUTH_01 se modela como **un solo nodo** —
los sub-pasos viven en el diagrama de secuencia
(§ 8.2).

.. uml::
 :caption: UC_AUTH_01 — diagrama de caso de uso

 @startuml

 left to right direction

 actor "User"                   as User
 actor "Sistema"                 as Sistema <<system>>
 actor "view_audit_log"                 as view_audit_log <<system>>

 rectangle "IACT — MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as UC01
   usecase "UC_AUTH_04\nCambiar\nContrasena"  as UC04
 }

 User  --> UC01 : presenta\ncredenciales
 UC01 --> Sistema  : valida + emite\ntokens + Session
 UC01 --> view_audit_log  : registra\nAuditEvent LOGIN

 UC04 ..> UC01 : <<extend>>\n[primer login\no expirado]

 note bottom of UC01
   Pre-cond CNST-003 (Session en BD)
   Pre-cond CNST-004 (sesion unica)
   Pre-cond CNST-011 (throttling)
   Pos-cond CNST-025 (audit inmutable)
 end note

 @enduml

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

 ServicioDeAutenticacion -> BaseDeDatos : SELECT User WHERE\nusername = ?
 BaseDeDatos --> ServicioDeAutenticacion : User

 alt User no existe
   ServicioDeAutenticacion --> InterfazDeUsuario : 401 INVALID_CREDENTIALS
   ServicioDeAutenticacion -> BaseDeDatos : INSERT AuditEvent\nLOGIN_FAILED
 else User existe
   ServicioDeAutenticacion -> Authservice : authenticate(user, password)
   activate Authservice
   Authservice -> Authservice : verificarHash()
   alt password incorrecto
     Authservice --> ServicioDeAutenticacion : invalid
     ServicioDeAutenticacion --> InterfazDeUsuario : 401 INVALID_CREDENTIALS
     ServicioDeAutenticacion -> BaseDeDatos : INSERT AuditEvent\nLOGIN_FAILED
   else password correcto
     Authservice --> ServicioDeAutenticacion : valid
     deactivate Authservice

     ServicioDeAutenticacion -> BaseDeDatos : BEGIN TRANSACTION
     ServicioDeAutenticacion -> BaseDeDatos : UPDATE Session\nSET state='CLOSED'\nWHERE user_id=X\nAND state='ACTIVE'
     ServicioDeAutenticacion -> BaseDeDatos : INSERT AuditEvent\nSESSION_CLOSED (n)
     ServicioDeAutenticacion -> BaseDeDatos : INSERT Session\n(state='ACTIVE')
     ServicioDeAutenticacion -> BaseDeDatos : INSERT AuditEvent\nLOGIN
     ServicioDeAutenticacion -> BaseDeDatos : UPDATE User\nSET last_login_at=NOW()
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
   CNST-005: expires_at = NOW() + 15 min
   CNST-025: AuditEvent inmutable
 end note

 @enduml

8.3 Diagrama de actividad
=========================

Vista del control de flujo con bifurcaciones por
las distintas excepciones y flujos alternos.

.. uml::
 :caption: UC_AUTH_01 — flujo de control con decisiones

 @startuml

 start

 :Recibir POST /api/auth/login/;
 :Validar Serializer;
 if (formato OK?) then (no)
   :Responder 400\nVALIDATION_ERROR;
   stop
 endif

 :Aplicar throttling CNST-011;
 if (dentro de limite?) then (no)
   :Responder 429\nRATE_LIMITED;
   :Emitir AuditEvent\nLOGIN_THROTTLED;
   stop
 endif

 :Buscar User por username;
 if (User existe?) then (no)
   :Responder 401\nINVALID_CREDENTIALS;
   :Emitir AuditEvent\nLOGIN_FAILED;
   stop
 endif

 if (User.state == BLOCKED?) then (si)
   :Responder 403\nACCOUNT_BLOCKED;
   :Emitir AuditEvent\nLOGIN_BLOCKED;
   stop
 endif

 if (User.state == INACTIVE?) then (si)
   :Responder 403\nACCOUNT_INACTIVE;
   :Emitir AuditEvent\nLOGIN_INACTIVE;
   stop
 endif

 :Verificar password (hash criptografico);
 if (password correcto?) then (no)
   :Responder 401\nINVALID_CREDENTIALS;
   :Emitir AuditEvent\nLOGIN_FAILED;
   stop
 endif

 :BEGIN TRANSACTION;
 :Cerrar Sessions ACTIVE\ndel User (CNST-004);
 :Crear Session nueva\n(CNST-003, CNST-005);
 :Emitir AuditEvent LOGIN\n(CNST-025);
 :Actualizar User.last_login_at;

 if (BD ok?) then (no)
   :ROLLBACK;
   :Responder 503\nDB_TRANSIENT_ERROR;
   stop
 endif

 :COMMIT;

 :Generar tokens JWT;

 if (User.first_login?) then (si)
   :Responder 200 con\nnext_step="change_password";
   :Frontend redirige\na UC_AUTH_04;
 elseif (password proximo\na expirar?) then (si)
   :Responder 200 con\nwarning password_expiring;
   :Frontend muestra modal\nopcional UC_AUTH_04;
 else (no)
   :Responder 200 con\ntokens y user;
   :Frontend redirige\nal landing;
 endif

 stop

 @enduml

8.4 Diagrama de estados de Session
==================================

Ciclo de vida de la entidad ``Session`` desde la
perspectiva de UC_AUTH_01 y los UCs que la
consumen.

.. uml::
 :caption: Estados de la clase Session

 @startuml

 [*] --> ACTIVE : UC_AUTH_01\n(crear)

 ACTIVE --> ACTIVE : actividad del\nusuario\n(extiende\nexpires_at)

 ACTIVE --> CLOSED : UC_AUTH_02\n(cierre por\nusuario)
 ACTIVE --> CLOSED : UC_AUTH_01 nuevo\n(SUPERSEDED\npor CNST-004)
 ACTIVE --> CLOSED : UC_AUTH_05\n(admin close)
 ACTIVE --> EXPIRED : timeout\n(CNST-005)\nsin actividad

 CLOSED --> [*]
 EXPIRED --> [*]

 note right of ACTIVE
   state vigente
   permite uso de tokens
   expires_at se actualiza
   con cada request
 end note

 note bottom of CLOSED
   close_reason ∈ {
     USER_LOGOUT,
     SUPERSEDED,
     ADMIN_CLOSE,
     EXPIRED
   }
   closed_at = NOW()
 end note

 note bottom of EXPIRED
   transicion automatica
   cuando expires_at < NOW()
   y no hay actividad
 end note

 @enduml

8.5 Notas sobre los diagramas
=============================

- Los diagramas viven **en este archivo**, no
  en archivos separados, por simplicidad de
  edicion. Si el render se vuelve pesado en
  futuras iteraciones, se puede dividir en
  archivos individuales (e.g.
  ``diagramas-uml/sequence.rst``).
- Las flechas y notaciones siguen las
  convenciones de
  :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso`,
  :doc:`/base-cognitiva/_uml/uml-09-diagramas-secuencias`,
  :doc:`/base-cognitiva/_uml/uml-08-diagramas-estados`,
  :doc:`/base-cognitiva/_uml/uml-11-diagramas-actividades`.
- Las clases del modelo de dominio aparecen
  como participantes (en secuencia) o como
  estados (en estados de ``Session``); el
  modelo completo vive en
  :doc:`/arquitectura-tecnica/modelo-dominio-iact`.
