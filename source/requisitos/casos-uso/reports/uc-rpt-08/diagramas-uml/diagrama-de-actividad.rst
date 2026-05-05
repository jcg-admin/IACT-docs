8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_08 — list

 @startuml
 start
 :GET /api/reports/scheduled/;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403; stop
 endif
 :Query schedules del User (o scope);
 :Aplicar filtros;
 :Paginar;
 :200 OK;
 stop
 @enduml

