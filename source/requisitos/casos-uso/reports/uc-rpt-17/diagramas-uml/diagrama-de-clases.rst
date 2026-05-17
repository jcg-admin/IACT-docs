.. _uc-rpt-17-parte-08-diagrama-clases:

8.4 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_17 — clases.

 @startuml

 class CallerReportService {
   + get(trimestre, invoker) : ReporteClientes
 }

 class SegmentResolver {
   + resolve(user) : set of String
 }

 CallerReportService --> SegmentResolver : invokes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service`.
