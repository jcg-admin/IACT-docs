8.3 Diagrama de actividad (ejecucion)
=====================================

.. uml::
 :caption: UC_RPT_07 — auto run

 @startuml
 start
 :Scheduler tick;
 :Query schedules con next_run_at <= now;
 while (schedules pendientes?)
   :Re-check permiso del User;
   if (Permiso ok?) then (no)
     :Audit PERMISSION_LOST;
     :Skip + reschedule next;
   else (si)
     :Enqueue ExportJob;
     :Update last_run_at + next_run_at;
     :Audit EXECUTED;
   endif
 endwhile
 stop
 @enduml

