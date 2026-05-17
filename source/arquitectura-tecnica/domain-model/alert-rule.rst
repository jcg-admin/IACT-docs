.. meta::
 :artefacto: AT_DM_CLASS_ALERT_RULE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_rule:

=========
AlertRule
=========

Definición declarativa de una regla de alerta. Especifica
qué métrica observar, sobre qué scope, con qué condición y
ventana temporal, y qué acciones disparar al cumplirse. Es
el insumo del evaluador del motor de alertas (``AlertEngine``)
y la fuente de verdad para configurar el monitoreo del
sistema.

Cada regla tiene su propio ciclo de vida (``RuleState``)
independiente del de las ``Alert`` instances que produce.
Una regla puede estar ``DRAFT`` (siendo editada),
``ENABLED`` (activa, evaluándose), ``DISABLED``
(desactivada por el operador) o ``ARCHIVED`` (retirada,
preservada por trazabilidad — BR-009).

.. uml::
 :caption: Clase AlertRule — definición declarativa de
           regla con condición, scope, ventana y acciones.

 @startuml

 class AlertRule {
   + rule_id : UUID
   + name : String
   + description : String
   + metric : MetricId
   + scope : Scope
   + condition : Condition
   + window : Duration
   + cooldown : Duration
   + severity : Severity
   + actions : List<Action>
   + status : RuleState
   + created_at : DateTime
   + updated_at : DateTime
   + created_by : UUID
   --
   + enable() : void
   + disable(reason : String) : void
   + archive() : void
   + matches(measurement : Measurement) : Boolean
   + is_in_cooldown(now : DateTime, last_fired_at : DateTime) : Boolean
 }

 class Condition {
   + operator : ComparisonOperator
   + threshold_value : Double
   + aggregation : Aggregation
 }

 class Scope {
   + scope_type : ScopeType
   + entity_ids : Set<UUID>
   + tags : Map<String, String>
 }

 enum RuleState {
   DRAFT
   ENABLED
   DISABLED
   ARCHIVED
 }

 enum Severity {
   INFO
   WARNING
   CRITICAL
 }

 enum ComparisonOperator {
   GT
   GTE
   LT
   LTE
   EQ
   NEQ
 }

 enum Aggregation {
   AVG
   SUM
   MIN
   MAX
   COUNT
   P95
   P99
 }

 enum ScopeType {
   GLOBAL
   SEGMENT
   QUEUE
   AGENT
   CAMPAIGN
 }

 AlertRule "1" *-- "1" Condition : has
 AlertRule "1" *-- "1" Scope : applies_to
 AlertRule "1" *-- "1..*" Action : triggers
 AlertRule "1" -- "1" RuleState
 AlertRule "1" -- "1" Severity
 Condition "1" -- "1" ComparisonOperator
 Condition "1" -- "1" Aggregation
 Scope "1" -- "1" ScopeType

 note bottom of AlertRule
   actions : {ordered}
 end note

 note right of AlertRule
   BR-009: archive en lugar de delete.
   cooldown evita ruido por oscilacion
   alrededor del threshold.
 end note

 @enduml

Restricciones aplicables
========================

- **BR-009** — bajas lógicas: ``archive()`` no borra, marca
  ``ARCHIVED``.
- **CNST-030** — Separacion de deberes: la edición y la habilitación de
  reglas son operaciones distintas (RBAC granular).
- **P-32** — reason-required: ``disable()`` exige razón
  documentada para auditoría.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index` —
  configurar reglas (CRUD).
- :doc:`/requisitos/casos-uso/alerts/uc-alr-02/index` —
  ver alertas activas (consume reglas).
- :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index` —
  acknowledge.

Relaciones
==========

- Composición fuerte con ``Condition`` y ``Scope``: ambos
  son partes constitutivas de la regla, no tienen sentido
  fuera de ella.
- Asociación con ``Action`` (lista): las acciones
  configuradas a disparar (notificar, escalar, pausar
  pipeline).
- Indirectamente produce instancias de ``Alert`` cuando
  evaluación matchea.
