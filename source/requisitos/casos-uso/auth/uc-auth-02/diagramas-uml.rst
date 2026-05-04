.. _uc-auth-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_02 — vista de actores y casos asociados

 @startuml

 left to right direction

 actor "User" as USER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_02\nCerrar Sesion" as UC02
   usecase "Validar token" as VTK
   usecase "Cerrar Session" as CSE
   usecase "Blacklist tokens" as BLK
   usecase "Emitir AuditEvent\nLOGOUT" as EMI
 }

 USER --> UC02
 UC02 ..> VTK : <<include>>
 UC02 ..> CSE : <<include>>
 UC02 ..> BLK : <<include>>
 UC02 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log : (consume\nUC_AUD_*)

 note bottom of UC02
   CNST-009 autenticacion
   CNST-013 manejo estandar
   CNST-025 auditoria inmutable
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_AUTH_02 — flujo principal

 @startuml

 actor Usuario as Usuario
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "LogoutView\n(DRF)" as Logoutview
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
     Authservice -> BaseDeDatos: SELECT Session WHERE\n  session_id=? AND state='ACTIVE'
     BaseDeDatos --> Authservice: session
     Authservice -> BaseDeDatos: UPDATE Session SET\n  state='CLOSED',\n  close_reason='USER_LOGOUT',\n  closed_at=NOW()
     Authservice -> Blacklist: INSERT BlacklistedToken\n  (access + refresh)
     Authservice -> BaseDeDatos: INSERT AuditEvent\n  (event_type='LOGOUT')
   end

   Authservice --> Logoutview: success
   Logoutview --> InterfazDeUsuario: 200 OK\n{"message": "Sesion cerrada"}
   InterfazDeUsuario -> InterfazDeUsuario: localStorage.clear\nRedux clear
   InterfazDeUsuario --> Usuario: Redirect /login
 end

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_AUTH_02 — actividad

 @startuml

 start

 :Usuario clickea "Cerrar sesion";
 :Frontend confirma (opcional);
 :POST /api/auth/logout/;

 if (Token JWT valido?) then (no)
   :Retornar 401 INVALID_TOKEN;
   stop
 else (si)
 endif

 :Localizar Session;

 if (Session existe?) then (no)
   :Retornar 401 SESSION_NOT_FOUND;
   stop
 else (si)
 endif

 if (User matchea?) then (no)
   :Retornar 401 USER_MISMATCH;
   note right
     Posible hijack — alerta
   end note
   stop
 else (si)
 endif

 if (Session.state == ACTIVE?) then (no)
   :FA-02/FA-03 (idempotente);
   :Emitir AuditEvent LOGOUT_REPLAY;
   :Retornar 200 OK informativo;
   stop
 else (si)
 endif

 partition "Transaccion atomica" {
   :UPDATE Session.state = CLOSED;
   :INSERT BlacklistedToken (access, refresh);
   :INSERT AuditEvent LOGOUT;
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :Retornar 500/503;
   stop
 else (si)
 endif

 :Frontend limpia localStorage;
 :Frontend redirige a /login;

 stop

 @enduml

8.4 Diagrama de estados — Session
=================================

.. uml::
 :caption: Estados de la entidad Session relevantes a UC_AUTH_02

 @startuml

 [*] --> ACTIVE : UC_AUTH_01 exito

 ACTIVE --> CLOSED : UC_AUTH_02\n(USER_LOGOUT)
 ACTIVE --> CLOSED : CNST-005\n(TIMEOUT)
 ACTIVE --> CLOSED : CNST-004\n(SUPERSEDED) por\nUC_AUTH_01 nuevo
 ACTIVE --> CLOSED : UC_AUTH_05\n(ADMIN_REVOKED)

 CLOSED --> [*]

 note right of CLOSED
   close_reason indica la causa.
   Idempotente: re-entrar a CLOSED
   no cambia close_reason.
 end note

 @enduml
