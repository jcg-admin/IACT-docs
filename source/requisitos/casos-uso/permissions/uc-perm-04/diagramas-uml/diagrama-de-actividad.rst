8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_04 — actividad

 @startuml

 start

 :DELETE .../{permission_id}/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene revoke_exceptional?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (Permission existe?) then (no)
   :404; stop
 else (si)
 endif

 if (state == REVOKED?) then (si)
   :Audit REVOKE_NOOP;
   :200 informativo; stop
 else (no)
 endif

 if (state == EXPIRED?) then (si)
   :400 INVALID_STATE; stop
 else (no — ACTIVE)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_REVOKE_FORBIDDEN;
   :Audit ALERTA;
   stop
 else (no)
 endif

 if (reason valido?) then (no)
   :400; stop
 else (si)
 endif

 :Iniciar transaccion atomica;
 :actualizar state=REVOKED + metadata;
 :registrar InternalMessage (HARD);
 if (Mailbox OK?) then (no)
   :ROLLBACK; :500 MAILBOX_FAILED;
   stop
 else (si)
 endif
 :registrar AuditEvent\nEXCEPTIONAL_PERMISSION_REVOKED;
 :Commit;

 :PermCache.invalidate post-COMMIT;
 :200 OK;

 stop

 @enduml

