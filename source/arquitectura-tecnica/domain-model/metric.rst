.. meta::
 :artefacto: AT_DM_CLASS_METRIC
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_metric:

======
Metric
======

Metrica de negocio del call center. Distinta de ``TechnicalMetric``
(bounded context Logs): ``Metric`` mide indicadores de negocio
(tasa de abandono, tiempo promedio de espera, eficiencia);
``TechnicalMetric`` mide infraestructura.

.. uml::
 :caption: Clase Metric — metrica de negocio del call center.

 @startuml

 class Metric {
   + metric_id : UUID
   + name : MetricName
   + formula : String
   + unit : String
   --
   + compute()
   + view()                <<view_dashboard>>
 }

 enum MetricName {
   ABANDONMENT_RATE
   AVG_WAIT_TIME
   EFFICIENCY_INDEX
   ANSWERED_RATE
 }

 Metric -- MetricName

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-reports`
 :doc:`/arquitectura-tecnica/domain-model/report`
 :doc:`/arquitectura-tecnica/domain-model/technical-metric`
