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
ClientesReportService
=====================

Servicio de reporte de **clientes únicos** que llamaron en
un período: cuenta callers únicos, tasa de retorno (repeat
caller rate) y curva de retención por trimestre.

Útil para análisis de churn y dimensionar campañas de
fidelización. Aplica filtros de segmento (CNST-008) antes
de agregar.

.. uml::
 :caption: Clase ClientesReportService — reporte de
           clientes únicos y retención.

 @startuml

 class ClientesReportService {
   - caller_stat_repo : CallerDailyStatRepo
   - kpi_calculator : KPICalculator
   - segment_resolver : SegmentResolver
   --
   + get(invoker : User, period : Period, \
         filters : ClientFilters) : ClientesReport
   + by_segment(invoker : User, period : Period) : List<SegmentClientStats>
   + retention_curve(invoker : User, period : Period) : RetentionCurve
   - apply_segment_filter(filters : ClientFilters, segment : Segment) : ClientFilters
 }

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
 class KPICalculator
 class SegmentResolver

 ClientesReportService o-- CallerDailyStatRepo : reads
 ClientesReportService *-- KPICalculator : composes
 ClientesReportService o-- SegmentResolver : reads
 ClientesReportService ..> ClientesReport : returns
 ClientesReportService ..> SegmentClientStats : returns
 ClientesReportService ..> RetentionCurve : returns

 note right of ClientesReportService
   retention_curve mide qué porcentaje
   de callers del mes N volvió en el
   mes N+1, N+2, etc.
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
