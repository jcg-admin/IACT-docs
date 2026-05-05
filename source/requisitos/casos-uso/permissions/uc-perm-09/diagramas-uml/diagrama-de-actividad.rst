8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_09 — emit

 @startuml

 start

 :Caller invoca con event_type, payload, ctx;

 if (Validacion estructural?) then (no)
   :AuditValidationError; stop
 else (si)
 endif

 if (PII detectado?) then (si)
   :AuditPIIDetected; stop
 else (no)
 endif

 :Sanitizar (hash de PII si requerido);
 :Construir AuditEvent con UUID v7;
 :registrar en transaccion del caller;

 if (registro ok?) then (no)
   :AuditWriteFailed;
   :Caller hace ROLLBACK;
   stop
 else (si)
 endif

 if (event_type CRITICAL?) then (si)
   :Replicar a log secundario sincrono;
 else (no)
 endif

 :Caller COMMIT;
 :AlertEngine push (best-effort);
 :Retornar id al caller;

 stop

 @enduml

