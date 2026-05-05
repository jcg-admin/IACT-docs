.. meta::
 :artefacto: AT_DM_CLASS_ABANDONO_REPORT_SERVICE
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

.. _dm_class_abandono_report_service:

=====================
AbandonmentReportService
=====================

Servicio de reporte especializado en **llamadas
abandonadas**: agrega métricas de abandono (tasa, tiempo
medio antes del abandono, distribución por intervalo de
espera) sobre un período. Particularmente útil para
detectar SLA breaches y dimensionar staffing.

Usa el ``QueueDailyStatRepo`` (lectura) y aplica filtros
de segmento (CNST-008) antes de agregar.

.. uml::
 :caption: Clase AbandonmentReportService — reporte de
           llamadas abandonadas con KPIs especializados.

 @startuml

 abstract class BaseReportService

 class AbandonmentReportService {
   --
   + get(invoker : User, period : Period, \
         filters : AbandonFilters) : AbandonReport
   + by_queue(invoker : User, period : Period) : List<QueueAbandonStats>
   + abandonment_curve(invoker : User, period : Period) : AbandonmentCurve
 }

 BaseReportService <|-- AbandonmentReportService

 class AbandonReport {
   + period : Period
   + total_offered : Integer
   + total_abandoned : Integer
   + abandonment_rate : Double
   + average_wait_before_abandon : Duration
   + by_interval : Map<WaitInterval, Integer>
 }

 class QueueAbandonStats {
   + queue_id : UUID
   + abandonment_rate : Double
   + worst_hour : DateTime
 }

 class AbandonmentCurve {
   + buckets : List<Bucket>
 }

 enum WaitInterval {
   UNDER_5S
   FROM_5S_TO_10S
   FROM_10S_TO_30S
   FROM_30S_TO_60S
   OVER_60S
 }

 class QueueDailyStatRepo

 AbandonmentReportService "1" o-- "1" QueueDailyStatRepo : reads
 AbandonmentReportService "1" ..> "1" AbandonReport : <<returns>>
 AbandonmentReportService "1" ..> "0..*" QueueAbandonStats : <<returns>>
 AbandonmentReportService "1" ..> "0..1" AbandonmentCurve : <<returns>>

 note bottom of AbandonReport
   by_interval : {ordered}
 end note

 note right of AbandonmentReportService
   Hereda apply_segment_filter de
   BaseReportService. abandonment_curve
   agrupa por WaitInterval para
   identificar el "punto critico".
 end note

 @enduml

Trazabilidad a UCs
==================

Reporte derivado del cluster ``uc-rpt-*``. Reutilizado por
dashboards y reportes históricos cuando filtran por
abandono.

Relaciones
==========

- Agregación con ``QueueDailyStatRepo`` y
  ``SegmentResolver``.
- Composición con ``KPICalculator``.
- Devuelve DTOs especializados.
