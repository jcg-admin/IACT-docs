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
   :actualizar Session.state = CLOSED;
   :registrar BlacklistedToken (access, refresh);
   :registrar AuditEvent LOGOUT;
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

