.. _uc-rpt-13-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_13 — clases del reporte de abandono.

 @startuml

 class AbandonmentReportService {
   + get(trimestre, invoker) : ReporteAbandono
 }

 class SegmentResolver {
   + resolve(user) : set of String
 }

 AbandonmentReportService --> SegmentResolver : invokes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/abandonment-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`.
