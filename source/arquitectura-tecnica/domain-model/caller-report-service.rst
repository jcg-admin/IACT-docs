.. meta::
 :artefacto: AT_DM_CLASS_CLIENTES_REPORT_SERVICE
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

.. _dm_class_clientes_report_service:

=====================
CallerReportService
=====================

Servicio de reporte de **clientes únicos** que llamaron en
un período: cuenta callers únicos, tasa de retorno (repeat
caller rate) y curva de retención por trimestre.

Útil para análisis de churn y dimensionar campañas de
fidelización. Aplica filtros de segmento (CNST-008) antes
de agregar.

.. uml::
 :caption: Clase CallerReportService — reporte de
           clientes únicos y retención.

 @startuml

 abstract class BaseReportService

 class CallerReportService {
   --
   + get(invoker : User, period : Period, \
         filters : ClientFilters) : ClientesReport
   + by_segment(invoker : User, period : Period) : List<SegmentClientStats>
   + retention_curve(invoker : User, period : Period) : RetentionCurve
 }

 BaseReportService <|-- CallerReportService

 class ClientesReport {
   + period : Period
   + total_unique_callers : Integer
   + repeat_caller_rate : Double
   + new_callers : Integer
   + returning_callers : Integer
   + retention_by_month : Map<Month, Double>
 }

 class SegmentClientStats {
   + segment_id : UUID
   + unique_callers : Integer
   + repeat_rate : Double
 }

 class RetentionCurve {
   + buckets : List<Bucket>
 }

 class CallerDailyStatRepo

 CallerReportService "1" o-- "1" CallerDailyStatRepo : reads
 CallerReportService "1" ..> "1" ClientesReport : <<returns>>
 CallerReportService "1" ..> "0..*" SegmentClientStats : <<returns>>
 CallerReportService "1" ..> "0..1" RetentionCurve : <<returns>>

 note bottom of ClientesReport
   retention_by_month : {ordered}
 end note

 note right of CallerReportService
   Hereda apply_segment_filter de
   BaseReportService. retention_curve
   mide qué porcentaje de callers del
   mes N volvió en el mes N+1, N+2.
 end note

 @enduml

Trazabilidad a UCs
==================

Reporte derivado del cluster ``uc-rpt-*``. Insumo para
reportes ejecutivos trimestrales.

Relaciones
==========

- Agregación con ``CallerDailyStatRepo`` y
  ``SegmentResolver``.
- Composición con ``KPICalculator``.
- Devuelve DTOs especializados.
