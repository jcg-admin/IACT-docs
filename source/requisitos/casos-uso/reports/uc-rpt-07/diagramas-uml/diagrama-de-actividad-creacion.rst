8.2 Diagrama de actividad (creacion)
====================================

.. uml::
 :caption: UC_RPT_07 — crear

 @startuml
 start
 :POST con schedule;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403; stop
 endif
 :Validar cron / frecuencia / period;
 if (User > 10?) then (si)
   :429; stop
 endif
 :Calcular next_run_at;
 :registrar ScheduledReport;
 :Audit CREATED;
 :201;
 stop
 @enduml

