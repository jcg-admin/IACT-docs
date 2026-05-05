.. meta::
 :artefacto: AT_DM_CLASS_TIMING_CALCULATOR
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_timing_calculator:

================
TimingCalculator
================

Calcula métricas de tiempo de respuesta operacional sobre
una ``Alert``: **TTAK** (*time-to-acknowledge*, latencia
desde ``triggered_at`` hasta ``acknowledged_at``) y **TTAR**
(*time-to-resolve*, latencia desde ``triggered_at`` hasta
el cierre o resolución). Útil para reportes de SLA y
postmortems.

Componente puro (stateless): cada llamada recibe una
``Alert`` o un set y produce el resultado calculado. No
mantiene estado entre invocaciones.

.. uml::
 :caption: Clase TimingCalculator — métricas de respuesta
           TTAK / TTAR sobre Alert.

 @startuml

 class TimingCalculator {
   - business_calendar : BusinessCalendar
   --
   + compute_ttak(alert : Alert) : Duration
   + compute_ttar(alert : Alert) : Duration
   + compute_response_metrics(alerts : List<Alert>) : ResponseMetrics
   + compute_business_ttak(alert : Alert) : Duration
   + compute_business_ttar(alert : Alert) : Duration
 }

 class ResponseMetrics {
   + count : Integer
   + ttak_avg : Duration
   + ttak_p50 : Duration
   + ttak_p95 : Duration
   + ttar_avg : Duration
   + ttar_p50 : Duration
   + ttar_p95 : Duration
 }

 class Alert
 class BusinessCalendar
 class Duration

 TimingCalculator "1" o-- "1" BusinessCalendar : uses
 TimingCalculator "1" ..> "0..*" Alert : reads
 TimingCalculator "1" ..> "0..*" ResponseMetrics : returns
 TimingCalculator "1" ..> "0..*" Duration : returns

 note right of TimingCalculator
   Stateless. compute_business_*
   excluye horas no-laborables segun
   BusinessCalendar para SLA reales.
 end note

 @enduml

Operaciones principales
=======================

- ``compute_ttak(alert)`` — TTAK en tiempo real
  (``acknowledged_at - triggered_at``). Devuelve duración
  con resolución de segundos.
- ``compute_ttar(alert)`` — TTAR en tiempo real
  (``resolved_at - triggered_at``).
- ``compute_business_ttak(alert)`` /
  ``compute_business_ttar(alert)`` — variantes que
  excluyen horas no laborables del cálculo, usando
  ``BusinessCalendar``. Útil para SLA contractuales.
- ``compute_response_metrics(alerts)`` — agregación: avg,
  p50, p95 de TTAK y TTAR sobre un set.

Casos especiales
================

- ``acknowledged_at`` ``null`` → TTAK indeterminado;
  devuelve ``null`` o duración hasta ``now`` según
  política.
- ``resolved_at`` ``null`` → TTAR indeterminado;
  análogo.
- Set vacío en ``compute_response_metrics`` → devuelve
  ``ResponseMetrics`` con ``count=0`` y duraciones nulas.

Restricciones aplicables
========================

- **CNST-024** — los datos consumidos respetan retención.
- ``BusinessCalendar`` debe estar versionado para que las
  métricas históricas sigan siendo reproducibles si las
  reglas de calendario cambian.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index` —
  reportes de historial usan
  ``compute_response_metrics``.

Relaciones
==========

- Agregación con ``BusinessCalendar`` (servicio externo).
- Lee instancias de ``Alert``.
- Devuelve ``ResponseMetrics`` o ``Duration``.
- No tiene estado persistente; usable concurrentemente
  sin sincronización.
