.. _uc-rpt-16-parte-08-diagrama-clases:

8.4 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_16 — clases.

 @startuml

 class IvrNavigationReportService {
   + get(trimestre, vista, invoker) : ReporteMenuIVR
 }

 class SegmentResolver {
   + resolve(user) : set of String
 }

 IvrNavigationReportService --> SegmentResolver : invokes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service`.
