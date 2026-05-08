.. meta::
 :artefacto: AT_DM_CLASS_SEPARATION_RULE_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_separation_rule_repo:

==================
SeparationRuleRepo
==================

Repositorio CRUD de ``SeparationRule`` (reglas de separacion que declaran
conjuntos de funciones mutuamente excluyentes). Las 3 reglas estaticas
actuales (SOD-001..003 segun CNST-030) se persisten aqui; este repo
permite agregar nuevas, actualizar parametros o desactivar.

Provee queries especializadas para ``RuleValidator``: dado un set
candidato de funciones, retorna todas las reglas activas que aplican
a funciones del set, para que el validator decida si hay violacion
separacion write-time (BR-007).

.. uml::
 :caption: Clase SeparationRuleRepo — CRUD + queries de separacion.

 @startuml

 class SeparationRuleRepo {
   - storage_backend : StorageBackend
   --
   + create(rule : SeparationRule) : UUID
   + get_by_id(rule_id : UUID) : SeparationRule
   + get_by_name(name : String) : SeparationRule
   + find_active() : List<SeparationRule>
   + find_applicable(function_codenames : List<String>) : List<SeparationRule>
   + update(rule_id : UUID, changes : Map) : SeparationRule
   + disable(rule_id : UUID, actor_id : UUID, reason : String) : SeparationRule
   + exists_name(name : String) : Boolean
 }

 class SeparationRule

 SeparationRuleRepo "1" --> "*" SeparationRule : gestiona

 note bottom of SeparationRuleRepo
   BR-009 disable, no DELETE.
   CNST-030 conjuntos disjuntos.
   find_applicable es la query
   critica usada por RuleValidator
   en cada assignment write-time.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben:

- :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
  gestionar ciclo de vida de reglas de separacion: create, update, disable.

UCs que leen (validan separacion):

- :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
  asignar funciones: find_applicable + RuleValidator.evaluate.
- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  asignar AGR: validar separacion sobre funciones expandidas del AGR.
- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  permiso temporal: validar separacion write-time.
- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  modificar AGR composition: validar nueva composicion no rompe separacion.
- :doc:`/requisitos/casos-uso/access/uc-acc-05/index` —
  ver reglas de separacion: find_active (vista operativa, read-only).

Relaciones
==========

- :doc:`separation-rule` — entity gestionada.
- :doc:`rule-validator` — consumidor principal de find_applicable.
- :doc:`evaluator-reloader` — recarga reglas activas tras cambio.
- :doc:`audit-service` — emite SEPARATION_RULE_CREATED / UPDATED / DISABLED.
