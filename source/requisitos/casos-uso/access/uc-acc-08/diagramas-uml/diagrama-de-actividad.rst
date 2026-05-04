8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_08 — actividad

 @startuml

 start

 :POST exceptional-permissions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene grant_exceptional_permission?) then (no)
   :403; :Audit UNAUTHORIZED ALERTA ALTA;
   stop
 else (si)
 endif

 if (User existe + state OK?) then (no)
   :404 / 400; stop
 else (si)
 endif

 if (P-11 viola?) then (si)
   :400 SELF_GRANT_FORBIDDEN;
   :Audit ALERTA CRITICA;
   stop
 else (no)
 endif

 if (justification + expires_at validos?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 if (Funciones validas?) then (no)
   :400; stop
 else (si)
 endif

 :Filtrar idempotencia;
 if (Quedan funciones a grant?) then (no)
   :Audit GRANT_NOOP;
   :200 OK informativo;
   stop
 else (si)
 endif

 :Construir effective_post_grant;
 :Evaluar SoDRules;

 if (SoD viola?) then (si)
   :409 SOD_VIOLATION;
   :Audit GRANT_FAILED ALERTA;
   stop
 else (no)
 endif

 :Iniciar transaccion atomica;
 :registrar ExceptionalPermission (N);
 :registrar InternalMessage (obligatorio P-10);
 if (Mailbox OK?) then (no)
   :ROLLBACK;
   :500 MAILBOX_FAILED;
   stop
 else (si)
 endif
 :registrar AuditEvent
  EXCEPTIONAL_PERMISSION_GRANTED;
 :Commit;

 :PermissionCache.invalidate post-COMMIT;
 :201 Created;

 stop

 @enduml

