.. meta::
 :artefacto: AT_DM_CLASS_ALERT_RULE_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert_rule_repo:

=============
AlertRuleRepo
=============

Repositorio de persistencia y consulta de instancias
``AlertRule``. Distinto de ``AlertRepo`` (que maneja las
alertas ya disparadas), su responsabilidad es el ciclo de
vida del **catalogo de reglas** que el motor de alertas
evalua periodicamente.

1. **Persistir** reglas creadas o modificadas por usuarios
   con codename ``manage_alerts`` (``create``, ``update``).
2. **Consultar** el catalogo activo para que el
   ``EvaluatorReloader`` lo refresque (``list_active``,
   ``by_id``).

La operacion de baja sigue ``BR-009`` — soft delete, no
eliminacion fisica. La regla queda en estado ``INACTIVE``
para preservar trazabilidad de alertas historicas que la
referencian.

.. uml::
 :caption: Clase AlertRuleRepo — gestion del catalogo de
           AlertRule con soft delete (BR-009).

 @startuml

 class AlertRuleRepo {
   - storage_backend : StorageBackend
   --
   + create(rule : AlertRule, actor_user_id : UUID) : AlertRule
   + update(rule : AlertRule, actor_user_id : UUID) : AlertRule
   + by_id(rule_id : UUID) : AlertRule
   + list_active() : List<AlertRule>
   + list_all(filters : AlertRuleFilters) : List<AlertRule>
   + disable(rule_id : UUID, actor_user_id : UUID) : AlertRule
 }

 class AlertRuleFilters {
   + state : AlertRuleState
   + scope : Scope
   + severity : Severity
 }

 class AlertRule
 class AlertRuleState

 AlertRuleRepo "1" ..> "0..*" AlertRule : persists/queries
 AlertRuleRepo "1" ..> "0..*" AlertRuleFilters : queries with

 note right of AlertRuleRepo
   disable(rule_id) NO borra fisicamente
   — soft delete (BR-009).
 end note

 @enduml

Operaciones principales
=======================

- ``create(rule, actor)`` — persiste una nueva regla. El
  ``actor_user_id`` debe tener codename ``manage_alerts``.
- ``update(rule, actor)`` — actualiza una regla existente
  incrementando su ``version``.
- ``by_id(rule_id)`` — recupera una regla por su id.
- ``list_active()`` — devuelve el catalogo de reglas en
  estado ``ACTIVE`` para que el ``EvaluatorReloader`` lo
  refresque tras cada cambio.
- ``disable(rule_id, actor)`` — marca la regla como
  ``INACTIVE`` (BR-009 baja logica).

Restricciones aplicables
========================

- **BR-009** — la baja es logica. ``disable`` no elimina la
  regla; cambia su estado a ``INACTIVE`` para preservar
  trazabilidad con alertas historicas.
- **CNST-025** — cada operacion de mutacion se audita via
  ``AuditService.emit()`` (responsabilidad del invocante).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index` —
  ``create``, ``update``, ``disable``.

Relaciones
==========

- Persiste y consulta instancias de ``AlertRule``.
- Es notificado indirectamente por ``EvaluatorReloader``
  cuando una regla cambia, para refrescar el catalogo
  activo.
- No conoce ``Alert`` (alertas disparadas); esa
  responsabilidad es de ``AlertRepo``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`
