8.4 Clases
==========

.. uml::

 @startuml
 class MenuIVRReportService {
   + get(trimestre, vista, invoker) : ReporteMenuIVR
 }
 class ServicioReportes {
   + menu_redirigidos(trimestre) : list[dict]
   + menu_centro(trimestre) : list[dict]
   + cmenu_error(trimestre) : list[dict]
 }
 class SegmentResolver
 MenuIVRReportService --> ServicioReportes
 MenuIVRReportService --> SegmentResolver
 @enduml
