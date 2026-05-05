8.3 Clases
==========

.. uml::

 @startuml
 class TransferReportService {
   + get(trimestre, invoker) : ReporteTransferencias
 }
 class SegmentResolver
 TransferReportService --> SegmentResolver
 @enduml
