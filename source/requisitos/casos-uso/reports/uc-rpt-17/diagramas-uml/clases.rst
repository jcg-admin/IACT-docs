8.4 Clases
==========

.. uml::

 @startuml
 class ClientesReportService {
   + get(trimestre, invoker) : ReporteClientes
 }
 class ServicioReportes {
   + clientes(trimestre) : list[dict]
 }
 class SegmentResolver
 ClientesReportService --> ServicioReportes
 ClientesReportService --> SegmentResolver
 @enduml
