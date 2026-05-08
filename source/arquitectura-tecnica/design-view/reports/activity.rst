.. meta::
 :artefacto: AT_DESIGN_ACT_EXPORT_ASYNC
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: export-async
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_act_export_async:

============================================================
Design View — Flujo: Export Asincrono de Reportes
============================================================

Flujo de exportacion asincrona de reportes y logs. El usuario
solicita un export, recibe un ``ExportJob`` con ID, y puede
descargar cuando el ``ExportWorker`` complete el trabajo.

Cubre los UCs UC_RPT_04 (exportar reporte), UC_LOG_04 (exportar
logs).

.. uml::
 :caption: Flujo export async — enqueue -> worker -> download.

 @startuml

 start

 partition "Sincrono — request" {
   :Usuario solicita export(report_id, format);
   :AuthorizationGuard.verify();
   :ExportJob.create(state=pending,
   user_id, report_id, format);
   :ExportWorker.enqueue(job_id);
   :Retornar 202 {job_id, status_url};
 }

 partition "Asincrono — worker" {
   :ExportWorker.dequeue(job_id);
   :ExportJob.update(state=processing);
   :Cargar Report o ApplicationLog data;
   :Aplicar formato (CSV, XLSX, PDF);

   if (export ok?) then (si)
     :Persistir archivo en storage;
     :ExportJob.update(state=ready,
     download_url, expires_at);
     :Notificar usuario (mailbox o email);
   else (no)
     :ExportJob.update(state=failed, error);
     :Notificar error;
   endif

   :Emitir AuditEvent(type=export_completed);
 }

 partition "Sincrono — download" {
   :Usuario consulta status(job_id);
   if (state == ready?) then (si)
     :Redirect a download_url;
   else (no)
     :Retornar status actual;
   endif
 }

 partition "Cleanup" {
   :Scheduler periodico;
   :ExportJob.cleanup_expired();
   :ExportJob.update(state=expired);
 }

 stop

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/reports/sequence`
 - :doc:`/arquitectura-tecnica/design-view/reports/state`
 - :doc:`/arquitectura-tecnica/use-case-view/reports/uc-rpt-04-exportar-reporte`
 - :doc:`/arquitectura-tecnica/use-case-view/logs/uc-log-04-exportar-logs`
 - :doc:`/arquitectura-tecnica/domain-model/export-job`
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`
 - :doc:`/arquitectura-tecnica/domain-model/report`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
