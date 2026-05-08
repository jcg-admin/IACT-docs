.. meta::
 :artefacto: AT_UC_LOG_07_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_log_07_ver_metricas_tecnicas:

============================================================
UC_LOG_07 — Ver Metricas Tecnicas
============================================================

Latencias y rates por servicio/endpoint. ``view_technical_metrics``
sobre TechnicalMetric (TSDB Prometheus-compatible). Agregados avg,
p95, p99.

.. uml::
 :caption: UC_LOG_07 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_technical_metrics" as view_technical_metrics
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "TechnicalMetric" as TechnicalMetric <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nVer Metricas Tecnicas" as UC_LOG_07
   usecase "Verificar\nview_technical_metrics" as VERIFICAR_AGR
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por service\n+ endpoint" as FILTRAR
   usecase "Aplicar group_by\n(service | endpoint)" as GROUPBY
   usecase "Calcular agregados\n(avg, p95, p99)" as METRIC_AGG
 }

 view_technical_metrics --> UC_LOG_07

 UC_LOG_07 ..> VERIFICAR_AGR : <<include>>
 UC_LOG_07 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_07 ..> FILTRAR : <<include>>
 UC_LOG_07 ..> GROUPBY : <<include>>
 UC_LOG_07 ..> METRIC_AGG : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTRAR --> TechnicalMetric
 GROUPBY --> KpiCalculator
 METRIC_AGG --> KpiCalculator
 METRIC_AGG --> TechnicalMetric

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/technical-metric` —
   TSDB Prometheus.
 - :doc:`/arquitectura-tecnica/domain-model/metric` —
   Metric base.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   agregacion p95/p99.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   KpiAggregationStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/logs/uc-log-07/index` —
   spec textual.
