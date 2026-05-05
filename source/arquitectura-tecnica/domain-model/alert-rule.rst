.. meta::
 :artefacto: AT_DM_CLASS_ALERT_RULE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_rule:

=========
AlertRule
=========

Regla de alerta configurada. Define condicion, ventana temporal, cooldown y acciones.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AlertRule — stub pendiente de desarrollo.

 @startuml

 class AlertRule {
  + id : UUID
  + name : String
  + metric : String
  + scope : String
  + condition : String
  + window : Duration
  + severity : Severity
  + actions : List
  + cooldown : Duration
  + status : RuleState
 }

 @enduml
