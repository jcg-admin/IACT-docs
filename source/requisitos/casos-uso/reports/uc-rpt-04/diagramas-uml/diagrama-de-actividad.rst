8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_04 — flujo

 @startuml
 start
 :POST /api/reports/export/;
 if (JWT?) then (no)
   :401; stop
 endif
 if (export_csv?) then (no)
   :403 + audit; stop
 endif
 :Validar payload + estimacion;
 if (Excede limites?) then (si)
   :400; stop
 endif
 if (User > 5 jobs?) then (si)
   :429; stop
 endif
 :Crear ExportJob;
 :Encolar en worker;
 :Audit REPORT_EXPORT_QUEUED;
 :202 con job_id;
 :Worker toma job;
 :Recheck permiso del User;
 if (Permiso revocado?) then (si)
   :failed PERMISSION_REVOKED;
   stop
 endif
 :Stream query Analytics;
 :Sanitizar + escribir archivo;
 if (> 200 MB?) then (si)
   :failed TOO_LARGE; stop
 endif
 :Subir a storage + URL firmado;
 :Audit REPORT_EXPORT_COMPLETED;
 :Notify mailbox del User;

 stop
 @enduml

