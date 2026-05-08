Aplicación a IACT — ``ConsultaReporteRequest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Caso concreto: en ``rpt_app`` muchos métodos
reciben ``user_id``, ``segmento_id``,
``fecha_desde``, ``fecha_hasta`` como parámetros
sueltos:

- ``Reporte.generar(user_id, segmento_id,
  fecha_desde, fecha_hasta)``
- ``Reporte.exportar(user_id, segmento_id,
  fecha_desde, fecha_hasta, formato)``
- ``Reporte.contar_filas(user_id, segmento_id,
  fecha_desde, fecha_hasta)``

Snapshot post-refactor: extraer un
``ConsultaReporteRequest`` que agrupa esos cuatro
campos y aporta su validación canónica
(CNST_031: rango ≤ 6 meses).

.. uml::

   @startuml
   title Snapshot post-refactor — ReportQueryRequest

   class ReportQueryRequest {
     + user_id : int
     + segment_id : int
     + date_from : date
     + date_to : date
     --
     + validate() : bool
     - _verify_max_range() : bool
   }

   class Report {
     - _filters : List<Filter>
     --
     + generate(req : ReportQueryRequest) : Result
     + export(req : ReportQueryRequest, format : str) : TaskId
     + count_rows(req : ReportQueryRequest) : int
     - _apply_filters(req : ReportQueryRequest) : Query
   }

   class ExportReportFacade

   ExportReportFacade ..> ReportQueryRequest : uses
   ExportReportFacade ..> Report : injects
   Report ..> ReportQueryRequest : receives
   @enduml
