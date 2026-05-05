.. meta::
 :artefacto: AT_DESIGN_MOD_VIS_REPORTS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_vis_reports:

===================================================
Design View — MOD_Reports: Reporteria y Dashboard
===================================================

Patron de interaccion del modulo de reportes. Muestra el filtrado de
``Report`` por ``ReportScope``, la composicion de ``Metric``, y la
exportacion asincrona via ``ExportJob`` con ciclo
QUEUED → PROCESSING → DONE.

.. uml::
 :caption: Design View MOD_Reports — reporte con filtros, metricas y exportacion asincrona.

 @startuml

 actor AGR_OPERADOR

 participant InterfazReportes   <<frontend>>
 participant ReportingService   <<api>>
 participant RepositorioReport  <<repository>>
 participant ColaProcesamiento  <<queue>>
 database    AlmacenDatos       <<postgresql>>

 AGR_OPERADOR -> InterfazReportes : GET /reports\n?scope=AGENTS\n&from=2026-01-01
 activate InterfazReportes

 InterfazReportes -> ReportingService : filtrarReportes(scope:ReportScope.AGENTS, filtros)
 activate ReportingService

 ReportingService -> RepositorioReport : filter(ReportScope.AGENTS, filtros)
 activate RepositorioReport
 RepositorioReport -> AlmacenDatos : SELECT reports WHERE scope=AGENTS
 AlmacenDatos --> RepositorioReport : List<Report>
 RepositorioReport --> ReportingService : reportes
 deactivate RepositorioReport

 ReportingService -> AlmacenDatos : SELECT metrics\nWHERE name IN (\n  ABANDONMENT_RATE,\n  AVG_WAIT_TIME\n)
 AlmacenDatos --> ReportingService : List<Metric>

 ReportingService --> InterfazReportes : Report + Metric[]
 deactivate ReportingService
 InterfazReportes --> AGR_OPERADOR : dashboard
 deactivate InterfazReportes

 AGR_OPERADOR -> InterfazReportes : POST /reports/{id}/export\n{format:EXCEL}
 activate InterfazReportes

 InterfazReportes -> ReportingService : exportar(report_id, ExportFormat.EXCEL)
 activate ReportingService

 ReportingService -> AlmacenDatos : INSERT export_jobs{\n  job_id:UUID,\n  report_id,\n  format:EXCEL,\n  state:JobState.QUEUED,\n  enqueued_at\n}
 AlmacenDatos --> ReportingService : ExportJob creado

 ReportingService -> ColaProcesamiento : encolar(job_id)
 ColaProcesamiento --> ReportingService : OK

 ReportingService --> InterfazReportes : 202 Accepted {job_id}
 deactivate ReportingService
 InterfazReportes --> AGR_OPERADOR : job_id

 ... procesamiento asincrono ...

 ColaProcesamiento -> AlmacenDatos : UPDATE export_jobs\nSET state=DONE,\n  completed_at,\n  artifact_path
 deactivate InterfazReportes

 note right of ColaProcesamiento
   CNST-019 v3.0.0: cola asincrona abstracta.
   CNST-020 v3.0.0: throttling abstracto.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/report`
 :doc:`/arquitectura-tecnica/domain-model/metric`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
