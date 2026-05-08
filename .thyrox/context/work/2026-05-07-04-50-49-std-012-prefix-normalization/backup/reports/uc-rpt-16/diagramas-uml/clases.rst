8.4 Clases
==========

.. uml::

 @startuml
 class MenuIVRReportService {
   + get(trimestre, vista, invoker) : ReporteMenuIVR
 }
 class SegmentResolver
 MenuIVRReportService --> SegmentResolver
 @enduml
