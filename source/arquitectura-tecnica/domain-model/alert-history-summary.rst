.. meta::
 :artefacto: AT_DM_CLASS_ALERT_HISTORY_SUMMARY
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_history_summary:

====================
AlertHistorySummary
====================

DTO inmutable que agrega resultados de una consulta historica
de alertas. Es producido por ``AlertHistoryService.query``
combinando filas crudas de ``AlertRepo`` con timings
computados por ``TimingCalculator``.

Provee:

1. **Conteo total** y agrupaciones por severidad para mostrar
   distribucion en la UI.
2. **Percentiles de tiempo de reconocimiento (TTAR) y de
   resolucion (TTAK)** para SLA monitoring.
3. **Filas individuales** con el detalle de cada alerta del
   resultado.

.. uml::
 :caption: AlertHistorySummary — agregaciones de
           historial de alertas con percentiles.

 @startuml

 class AlertHistorySummary {
   + range : DateRange
   + total_alerts : Integer
   + by_severity : Map<Severity, Integer>
   + by_rule : Map<UUID, Integer>
   + ttak_p50 : Duration
   + ttak_p95 : Duration
   + ttar_p50 : Duration
   + ttar_p95 : Duration
   + rows : List<AlertHistoryRow>
 }

 class AlertHistoryRow {
   + alert_id : UUID
   + rule_name : String
   + severity : Severity
   + triggered_at : DateTime
   + acknowledged_at : DateTime
   + resolved_at : DateTime
 }

 class DateRange
 class Severity

 AlertHistorySummary "1" --> "*" AlertHistoryRow : details
 AlertHistorySummary --> DateRange
 AlertHistorySummary ..> Severity

 @enduml

Atributos
=========

- ``range : DateRange`` — periodo cubierto.
- ``total_alerts : Integer`` — cardinalidad total.
- ``by_severity / by_rule`` — mapas de agrupacion.
- ``ttak_p50/p95`` — Time To Acknowledge percentiles.
- ``ttar_p50/p95`` — Time To Resolve percentiles.
- ``rows : List<AlertHistoryRow>`` — detalle por alerta.

Restricciones aplicables
========================

- **CNST-018** — los rows respetan el ``SegmentScope`` del
  usuario que solicita el reporte.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index` —
  consulta de historial de alertas.

Relaciones
==========

- Producido por ``AlertHistoryService.query``.
- Consumido por la UI de uc-alr-04.
- ``AlertHistoryRow`` es nested DTO.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator`
