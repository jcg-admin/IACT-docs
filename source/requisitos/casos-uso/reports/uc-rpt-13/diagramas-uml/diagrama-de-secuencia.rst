.. _uc-rpt-13-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_RPT_13 — flujo de consulta de reporte.

 @startuml

 actor "view_reports" as view_reports
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "SegmentResolver" as SegmentResolver
 database   "Base Analitica IVR" as BaseAnaliticaIVR

 view_reports -> SvcAplicacion: GET /api/v1/reportes/abandono/
 SvcAplicacion -> SvcAplicacion: verificar capability
 SvcAplicacion -> SegmentResolver: resolve(user)
 SegmentResolver --> SvcAplicacion: [nacional_A, ...]
 SvcAplicacion -> BaseAnaliticaIVR: callproc(sp_rpt_llamadas_abandonadas, [trimestre])
 BaseAnaliticaIVR --> SvcAplicacion: rows abandono por segmento
 SvcAplicacion --> view_reports: 200 ReporteAbandono

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
