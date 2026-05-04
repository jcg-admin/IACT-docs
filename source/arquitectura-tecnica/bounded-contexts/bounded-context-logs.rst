.. meta::
 :artefacto: AT_DOMINIO_08_LOGS
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_logs:

========================================
Modelo de Dominio — Bounded Context Logs
========================================

4.8 Logs
--------

Cinco clases: ``ApplicationLog``, ``ETLLog``, ``InfrastructureLog``,
``SystemHealth`` y ``TechnicalMetric``. Las dos ultimas no son logs
en sentido estricto (D-05): ``SystemHealth`` es un snapshot de
estado, ``TechnicalMetric`` es una agregacion. Viven en este
contexto por cohesion del modulo MOD_Logs y porque comparten la
politica de retencion CNST-024.

``TechnicalMetric`` es distinta de la clase ``Metric`` del contexto
Reports & Metrics: aquella mide infraestructura (response time,
throughput, error rate, CPU, memoria); esta mide negocio
(abandonment_rate, avg_wait_time, efficiency_index).

.. uml::
 :caption: Bounded context Logs — logs aplicativos, ETL e
           infraestructura, mas snapshot de salud y metricas
           tecnicas.

 @startuml

 class ApplicationLog {
   + log_id : UUID
   + level : LogLevel
   + message : String
   + source_module : String
   + occurred_at : DateTime
   + user_id : UUID
   --
   + record()              <<sistema>>
   + view()                <<view_application_logs>>
   + search()              <<search_logs>>
   + export()              <<export_logs>>
 }

 class ETLLog {
   + log_id : UUID
   + execution_id : UUID
   + level : LogLevel
   + message : String
   + occurred_at : DateTime
   --
   + record()
   + view()                <<view_etl_logs>>
 }

 class InfrastructureLog {
   + log_id : UUID
   + host : String
   + level : LogLevel
   + message : String
   + occurred_at : DateTime
   --
   + record()
   + view()                <<view_infrastructure_logs>>
 }

 class SystemHealth {
   + snapshot_id : UUID
   + captured_at : DateTime
   + cpu_usage_pct : Double
   + memory_usage_pct : Double
   + disk_usage_pct : Double
   + services_status : Map<String,String>
   --
   + snapshot()           <<sistema>>
   + view()               <<view_system_health>>
 }

 class TechnicalMetric {
   + metric_id : UUID
   + name : TechMetricName
   + value : Double
   + sampled_at : DateTime
   + period : String
   --
   + aggregate()          <<sistema>>
   + view()               <<view_technical_metrics>>
 }

 enum LogLevel {
   TRACE
   DEBUG
   INFO
   WARN
   ERROR
   FATAL
 }

 enum TechMetricName {
   RESPONSE_TIME
   THROUGHPUT
   ERROR_RATE
   CPU
   MEMORY
 }

 ApplicationLog -- LogLevel
 ETLLog -- LogLevel
 InfrastructureLog -- LogLevel
 TechnicalMetric -- TechMetricName

 note right of SystemHealth
   D-05: NO es un log; snapshot
   efimero de estado. Retencion
   per CNST-024.
 end note

 note right of TechnicalMetric
   D-05: NO es un log; agregacion.
   Distinta de Metric (negocio) del
   contexto Reports & Metrics.
 end note

 note bottom of ApplicationLog
   CNST-024: retencion de logs.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
