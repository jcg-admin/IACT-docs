8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_02 — actividad

 @startuml

 start

 :DELETE /api/users/{id}/functions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (revoke_functions?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (Payload valido?) then (no)
   :400 VALIDATION_ERROR
    (incluye revoke_reason missing); stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 if (User ELIMINATED?) then (si)
   :400 INVALID_USER_STATE; stop
 else (no)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_REVOKE_FORBIDDEN;
   :Audit ALERTA;
   stop
 else (no)
 endif

 :consultar Assignments ACTIVE matching;
 :Filtrar idempotente
  (skip ya REVOKED);

 if (Quedan funciones a revocar?) then (no)
   :Audit FUNCTIONS_REVOKE_NOOP;
   :200 OK informativo;
   stop
 else (si)
 endif

 :Calcular post_revoke_active_count;
 :Detectar warnings (no_functions,
  critical_revoked, last_holder);

 if (BLOCK_LAST_HOLDER y last_holder violado?) then (si)
   :409 LAST_HOLDER_PROTECTION;
   :Audit FUNCTIONS_REVOKE_FAILED;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :actualizar Assignments → REVOKED + metadata;
   :registrar AuditEvent FUNCTIONS_REVOKED;
   if (notify activo?) then (si)
     :registrar InternalMessage;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500 / 503;
   stop
 else (si)
 endif

 :PermissionCache.invalidate(target.id)
  (post-COMMIT);
 :200 OK con warnings;
 :Frontend toast + warnings UI;

 stop

 @enduml

