.. meta::
 :artefacto: AT_DM_CLASS_THRESHOLD
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_threshold:

=========
Threshold
=========

Umbral de alerta que define el criterio de disparo. Cuando una metrica
supera el valor configurado con el operador de comparacion indicado,
se genera una ``Alert``.

.. uml::
 :caption: Clase Threshold — umbral de disparo de alerta.

 @startuml

 class Threshold {
   + threshold_id : UUID
   + metric_id : UUID
   + comparison_operator : CompOp
   + value : Double
   + severity : Severity
   --
   + configure()         <<configure_alerts>>
 }

 enum CompOp {
   GT
   GE
   LT
   LE
   EQ
   NE
 }

 Threshold -- CompOp

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-alerts`
 :doc:`/arquitectura-tecnica/domain-model/alert`
