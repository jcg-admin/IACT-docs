.. _uc-rpt-15-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_15 — clases.

 @startuml

 class TransferReportService {
   + get(trimestre, invoker) : ReporteTransferencias
 }

 class SegmentResolver {
   + resolve(user) : set of String
 }

 TransferReportService --> SegmentResolver : invokes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service`.
