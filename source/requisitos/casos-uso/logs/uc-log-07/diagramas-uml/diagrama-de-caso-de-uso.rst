8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_07 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_technical_metrics" as INVOKER
 actor "MetricsTSDB (Prometheus)" as TSDB <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nVer Metricas Tecnicas" as UC_LOG_07
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por service\n+ endpoint" as FILTRAR
   usecase "Aplicar group_by\n(service | endpoint)" as GROUPBY
   usecase "Calcular agregados\n(avg, p95, p99)" as METRIC_AGG
 }

 INVOKER --> UC_LOG_07
 UC_LOG_07 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_07 ..> FILTRAR : <<include>>
 UC_LOG_07 ..> GROUPBY : <<include>>
 UC_LOG_07 ..> METRIC_AGG : <<include>>

 FILTRAR --> TSDB
 METRIC_AGG --> TSDB

 note bottom of UC_LOG_07
   CNST-009 fechas relativas.
   MetricsTSDB: Prometheus o
   compatible. Latencias y rates
   por servicio/endpoint.
 end note

 @enduml
