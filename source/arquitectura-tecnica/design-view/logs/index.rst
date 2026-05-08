.. meta::
 :artefacto: AT_DESIGN_MOD_LOGS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_logs:

============================================================
Design View — MOD_Logs: Vista de Diseño
============================================================

Caja del modulo **MOD_Logs** (consulta de logs operacionales,
infraestructura y metricas tecnicas). Cubre las consultas
estructuradas con filtros y paginacion, y el calculo de
KPIs agregados (p95/p99) sobre las metricas tecnicas.

Materializa los UCs UC_LOG_01..07 documentados en
:doc:`/arquitectura-tecnica/use-case-view/logs/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Logs — entidades de log y servicios de
           consulta agregada. Detalle interno en
           :doc:`bounded-context`.

 @startuml

 package "MOD_Logs" {
   class ApplicationLog <<entity>>
   class InfrastructureLog <<entity>>
   class TechnicalMetric <<entity>>
 }

 class AuditQueryService <<external>>
 class KpiCalculator <<external>>

 AuditQueryService ..> ApplicationLog : <<query>>
 AuditQueryService ..> InfrastructureLog : <<query>>
 KpiCalculator ..> TechnicalMetric : <<agrega p95/p99>>

 note bottom of ApplicationLog
   3 entidades de log/metric.
   ColumnCatalog y validators
   en :doc:`bounded-context`.
 end note

 @enduml

Lectura del diagrama
====================

- **Tres entidades de observabilidad:** ``ApplicationLog``
  (logs aplicativos), ``InfrastructureLog`` (logs de infra)
  y ``TechnicalMetric`` (metricas tecnicas con timestamps).
- ``AuditQueryService`` reutilizado del modulo Audit provee
  la maquinaria de query con filtros + paginacion.
- ``KpiCalculator`` agrega ``TechnicalMetric`` a percentiles
  (p50, p95, p99) usados en dashboards de salud del sistema.
- ``ColumnCatalog`` (en :doc:`bounded-context`) describe los campos
  consultables de cada tipo de log.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/application-log` —
  ApplicationLog.
- :doc:`/arquitectura-tecnica/domain-model/infrastructure-log` —
  InfrastructureLog.
- :doc:`/arquitectura-tecnica/domain-model/technical-metric` —
  TechnicalMetric.
- :doc:`/arquitectura-tecnica/domain-model/log-store` —
  LogStore.
- :doc:`/arquitectura-tecnica/domain-model/infra-log-store` —
  InfraLogStore.
- :doc:`/arquitectura-tecnica/domain-model/column-catalog` —
  ColumnCatalog.
- :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
  KpiCalculator.
- :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
  AuditQueryService (reutilizado).

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Logs

 bounded-context
 interaction-pattern
 log-retention-flow

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/logs/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/audit/index` —
   AuditQueryService reutilizado.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
