.. meta::
 :artefacto: AT_DESIGN_MOD_SYS_LOGS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_sys_logs:

=============================================
Design View — MOD_Logs: Bitacoras del Sistema
=============================================

Patron de interaccion del modulo de logs. Muestra la busqueda de
``ApplicationLog`` por nivel y modulo, y la exportacion asincrona
via ``ExportJob``. Los logs se escriben por el sistema (record()),
no por el usuario.

.. uml::
 :caption: Design View MOD_Logs — busqueda y exportacion de logs de aplicacion.

 @startuml

 actor AGR_ADMIN

 participant InterfazLogs               <<frontend>>
 participant ServicioLogs               <<api>>
 participant RepositorioApplicationLog  <<repository>>
 participant ServicioExportacion        <<api>>
 database    AlmacenDatos               <<postgresql>>

 AGR_ADMIN -> InterfazLogs : GET /logs/application\n?level=ERROR\n&source_module=ServicioAuth\n&from=2026-05-01
 activate InterfazLogs

 InterfazLogs -> ServicioLogs : buscarLogs(level, source_module, desde)
 activate ServicioLogs

 ServicioLogs -> RepositorioApplicationLog : search(LogLevel.ERROR, source_module, rango)
 activate RepositorioApplicationLog
 RepositorioApplicationLog -> AlmacenDatos : SELECT application_logs\nWHERE level=ERROR\nAND source_module=?\nAND occurred_at >= ?
 AlmacenDatos --> RepositorioApplicationLog : List<ApplicationLog>
 RepositorioApplicationLog --> ServicioLogs : resultados
 deactivate RepositorioApplicationLog

 ServicioLogs --> InterfazLogs : pagina de ApplicationLog
 deactivate ServicioLogs
 InterfazLogs --> AGR_ADMIN : tabla de logs
 deactivate InterfazLogs

 AGR_ADMIN -> InterfazLogs : POST /logs/export\n{format:CSV, filters}
 activate InterfazLogs

 InterfazLogs -> ServicioExportacion : exportarLogs(filtros, format:CSV)
 activate ServicioExportacion

 ServicioExportacion -> AlmacenDatos : INSERT export_jobs{\n  job_id:UUID,\n  format:ExportFormat.CSV,\n  state:JobState.QUEUED\n}
 AlmacenDatos --> ServicioExportacion : ExportJob encolado

 ServicioExportacion --> InterfazLogs : 202 Accepted {job_id}
 deactivate ServicioExportacion
 InterfazLogs --> AGR_ADMIN : job_id para seguimiento
 deactivate InterfazLogs

 note right of AlmacenDatos
   CNST-024: politica de retencion de logs.
   ApplicationLog.record() es del sistema,
   no del usuario.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/application-log`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
