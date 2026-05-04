8.2 Diagrama de actividad (list)
================================

.. uml::
 :caption: UC_PERM_10 — list

 @startuml

 start
 :GET con filtros + cursor;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_audit_log?) then (no)
   :403 + UNAUTHORIZED audit;
   stop
 endif
 if (Filtros validos?) then (no)
   :400; stop
 endif
 :Query AuditRepo (read replica);
 :Sanitizar (truncar payload);
 :Construir cursor;
 :Estimar total;
 :Emit AUDIT_LOG_QUERIED (UC_PERM_09);
 if (Meta-audit ok?) then (no)
   :503; stop
 endif
 :200 OK;
 stop

 @enduml

