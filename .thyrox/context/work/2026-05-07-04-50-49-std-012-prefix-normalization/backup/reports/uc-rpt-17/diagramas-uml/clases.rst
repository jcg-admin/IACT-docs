8.4 Clases
==========

.. uml::

 @startuml
 class CallerReportService {
   + get(trimestre, invoker) : ReporteClientes
 }
 class SegmentResolver
 CallerReportService --> SegmentResolver
 @enduml
