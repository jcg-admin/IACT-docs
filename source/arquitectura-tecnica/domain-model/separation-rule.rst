.. meta::
 :artefacto: AT_DM_CLASS_SEPARATION_RULE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_separation_rule:

==============
SeparationRule
==============

Regla de separacion de funciones (SoD). Define conjuntos de funciones
RBAC que no pueden ser asignadas simultaneamente al mismo usuario
(CNST-030). Las reglas se desactivan, no se eliminan (BR-009 v2.0.0).

.. uml::
 :caption: Clase SeparationRule — regla de separacion de funciones (SoD).

 @startuml

 class SeparationRule {
   + rule_id : UUID
   + name : String
   + conflicting_functions : List<String>
   + rule_group : String
   + state : RuleState
   --
   + create()                  <<create_separation_rule>>
   + view()                    <<view_separation_rules>>
   + update_separation_rule()  <<update_separation_rule>>
   + disable_separation_rule() <<disable_separation_rule>>
 }

 enum RuleState {
   ENABLED
   DISABLED
 }

 class Function {
   + name : String
   + module : Module
 }

 SeparationRule -- RuleState
 SeparationRule "1" -- "*" Function : (lista funciones en conflicto)

 note right of SeparationRule
   BR-009 v2.0.0: desactivar, no eliminar.
   CNST-030: enforcement SoD en tiempo de asignacion.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function`
