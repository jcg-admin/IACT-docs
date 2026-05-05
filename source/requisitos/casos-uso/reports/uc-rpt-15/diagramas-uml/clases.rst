8.3 Clases
==========

.. uml::

 @startuml
 class TransferenciasReportService {
   + get(trimestre, invoker) : ReporteTransferencias
 }
 class ServicioReportes {
   + centros_transferencia(trimestre) : list[dict]
   + centros_xsegmento(trimestre) : list[dict]
 }
 class SegmentResolver
 TransferenciasReportService --> ServicioReportes
 TransferenciasReportService --> SegmentResolver
 @enduml
