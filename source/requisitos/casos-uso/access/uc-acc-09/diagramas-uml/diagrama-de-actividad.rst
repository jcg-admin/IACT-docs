8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_09 — actividad

 @startuml

 start

 :GET /api/access/audit/?...;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (view_audit_log?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (Filtros validos whitelist?) then (no)
   :400 BAD_FILTER; stop
 else (si)
 endif

 :Construir query con
  event_type__in=ACCESS_EVENT_TYPES
  + filters provistos;
 :consultar paginado;
 :Aplicar mascarado PII;

 if (filter target_user_id?) then (si)
   :Audit ACCESS_AUDIT_VIEWED;
 else (no)
 endif

 :200 OK;

 stop

 @enduml

