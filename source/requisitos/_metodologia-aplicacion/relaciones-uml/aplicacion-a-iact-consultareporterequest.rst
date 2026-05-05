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
   title Snapshot post-refactor — ConsultaReporteRequest

   class ConsultaReporteRequest {
     + user_id : int
     + segmento_id : int
     + fecha_desde : date
     + fecha_hasta : date
     --
     + validar() : bool
     - _verificar_rango_max() : bool
   }

   class Reporte {
     - _filtros : List<Filtro>
     --
     + generar(req : ConsultaReporteRequest) : Resultado
     + exportar(req : ConsultaReporteRequest, formato : str) : TareaId
     + contar_filas(req : ConsultaReporteRequest) : int
     - _aplicar_filtros(req : ConsultaReporteRequest) : Query
   }

   class ExportarReporteFacade

   ExportarReporteFacade ..> ConsultaReporteRequest : usa
   ExportarReporteFacade ..> Reporte : inyecta
   Reporte ..> ConsultaReporteRequest : recibe
   @enduml
