8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_USR_04 — actividad

 @startuml

 start

 :Invoker abre detalle del User;
 :Click "Eliminar";
 :Modal robusto + escribir "ELIMINAR";

 if (Confirma?) then (no)
   :Cancelar; stop
 else (si)
 endif

 :DELETE /api/users/{id}/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene deactivate_users?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404 USER_NOT_FOUND; stop
 else (si)
 endif

 if (User ya ELIMINATED?) then (si)
   if (politica strict?) then (si)
     :409 USER_ALREADY_ELIMINATED; stop
   else (no — default idempotente)
     :Audit USER_ELIMINATE_NOOP;
     :200 OK informativo;
     stop
   endif
 else (no)
 endif

 if (invoker.id == target.id?) then (si)
   :400 SELF_ELIMINATION_FORBIDDEN;
   :Audit USER_ELIMINATE_FAILED ALERTA;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :actualizar User → ELIMINATED + metadata;
   :actualizar Assignments activas → REVOKED;
   :actualizar Sessions activas → CLOSED;
   :registrar BlacklistedToken por cada Session;
   if (politica notify?) then (si)
     :registrar InternalMessage;
     if (mailbox OK?) then (no)
       :mailbox_failed=true (sin abort);
     else (si)
     endif
   else (no)
   endif
   :registrar AuditEvent USER_ELIMINATED;
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500 / 503;
   stop
 else (si)
 endif

 :200 OK con resumen
  (sessions_closed,
   assignments_revoked);
 :Frontend toast + refresh;

 stop

 @enduml

