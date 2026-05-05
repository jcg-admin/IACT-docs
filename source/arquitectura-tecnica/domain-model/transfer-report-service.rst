.. meta::
 :artefacto: AT_DM_CLASS_TRANSFERENCIAS_REPORT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_transferencias_report_service:

===========================
TransferReportService
===========================

Servicio de reporte de **transferencias entre centros**:
volumen, latencia media de transferencia, tasa de éxito y
matriz origen→destino para detectar centros saturados o
cuellos de botella en el routing.

Aplica filtros de segmento (CNST-008) antes de agregar.

.. uml::
 :caption: Clase TransferReportService — reporte de
           transferencias entre centros con matriz O/D.

 @startuml

 abstract class BaseReportService

 class TransferReportService {
   --
   + get(invoker : User, period : Period, \
         filters : TransferFilters) : TransferenciasReport
   + by_center(invoker : User, period : Period) : List<CenterTransferStats>
   + origin_destination_matrix(invoker : User, \
                                 period : Period) : OriginDestinationMatrix
 }

 BaseReportService <|-- TransferReportService

 class TransferenciasReport {
   + period : Period
   + total_transfers : Integer
   + successful_transfers : Integer
   + success_rate : Double
   + average_transfer_time : Duration
   + by_status : Map<TransferStatus, Integer>
 }

 class CenterTransferStats {
   + center_id : UUID
   + transfers_in : Integer
   + transfers_out : Integer
   + balance : Integer
 }

 class OriginDestinationMatrix {
   + cells : Map<Pair<UUID, UUID>, Integer>
 }

 enum TransferStatus {
   COMPLETED
   FAILED
   ABANDONED_DURING_TRANSFER
   REJECTED_BY_TARGET
 }

 class TransferDailyStatRepo

 TransferReportService "1" o-- "1" TransferDailyStatRepo : reads
 TransferReportService "1" ..> "1" TransferenciasReport : <<returns>>
 TransferReportService "1" ..> "0..*" CenterTransferStats : <<returns>>
 TransferReportService "1" ..> "0..1" OriginDestinationMatrix : <<returns>>

 note right of TransferReportService
   Hereda apply_segment_filter de
   BaseReportService.
   origin_destination_matrix expone
   la matriz centro_origen → centro_destino.
 end note

 @enduml

Trazabilidad a UCs
==================

Reporte derivado del cluster ``uc-rpt-*``. Insumo para
balanceo de carga y diseño de routing.

Relaciones
==========

- Agregación con ``TransferDailyStatRepo`` y
  ``SegmentResolver``.
- Composición con ``KPICalculator``.
- Devuelve DTOs especializados.
