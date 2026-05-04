.. meta::
 :artefacto: AT_DM_CLASS_TECHNICAL_METRIC
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_technical_metric:

===============
TechnicalMetric
===============

Metrica de infraestructura. Distinta de ``Metric`` (bounded context
Reports): ``TechnicalMetric`` mide respuesta, throughput, errores,
CPU y memoria; ``Metric`` mide indicadores de negocio del call center.
Por D-05 vive en el bounded context Logs por cohesion con MOD_Logs.

.. uml::
 :caption: Clase TechnicalMetric — metrica de infraestructura del sistema.

 @startuml

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

 enum TechMetricName {
   RESPONSE_TIME
   THROUGHPUT
   ERROR_RATE
   CPU
   MEMORY
 }

 TechnicalMetric -- TechMetricName

 note bottom of TechnicalMetric
   D-05: NO es un log; agregacion.
   Distinta de Metric (negocio) del contexto Reports.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/metric`
