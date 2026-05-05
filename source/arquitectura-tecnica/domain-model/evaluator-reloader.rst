.. meta::
 :artefacto: AT_DM_CLASS_EVALUATOR_RELOADER
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

.. _dm_class_evaluator_reloader:

=================
EvaluatorReloader
=================

Coordinador que **propaga cambios de configuración** de
``AlertRule`` al motor evaluador en tiempo de ejecución.
Cuando el operador crea, edita, habilita o deshabilita una
regla, este componente se encarga de que el evaluador
recoja la versión actualizada sin requerir reinicio.

Soporta tres modos: recarga puntual de una regla
(``reload_rule``), recarga del set completo
(``reload_all``) y verificación de versión actual
(``current_version``).

.. uml::
 :caption: Clase EvaluatorReloader — propaga cambios de
           AlertRule al motor evaluador en runtime.

 @startuml

 class EvaluatorReloader {
   - rule_repo : AlertRuleRepo
   - evaluator : AlertEvaluator
   - version_clock : VersionClock
   --
   + reload_rule(rule_id : UUID) : ReloadResult
   + reload_all() : ReloadResult
   + current_version() : Integer
   - apply_diff(removed : Set<UUID>, added : Set<UUID>, \
                modified : Set<UUID>) : ReloadResult
   - bump_version() : Integer
 }

 class ReloadResult {
   + ok : Boolean
   + rules_loaded : Integer
   + rules_dropped : Integer
   + errors : List<ReloadError>
   + new_version : Integer
 }

 class ReloadError {
   + rule_id : UUID
   + reason : String
 }

 class AlertRuleRepo
 class AlertEvaluator
 class VersionClock

 EvaluatorReloader o-- AlertRuleRepo : reads
 EvaluatorReloader o-- AlertEvaluator : updates
 EvaluatorReloader *-- VersionClock : composes
 EvaluatorReloader ..> ReloadResult : returns
 ReloadResult *-- "*" ReloadError

 note right of EvaluatorReloader
   Hot-reload: el evaluador no se reinicia.
   version_clock identifica la generacion
   de reglas activa.
 end note

 @enduml

Operaciones principales
=======================

- ``reload_rule(rule_id)`` — re-lee una regla específica
  desde ``AlertRuleRepo`` y la propaga al evaluador.
  Útil cuando la edición es puntual.
- ``reload_all()`` — re-sincroniza completamente el set de
  reglas del evaluador con el repositorio. Más costosa,
  necesaria tras importaciones masivas o recovery.
- ``current_version()`` — devuelve la versión actual
  de configuración. Útil para diagnósticos.

Garantías
=========

- **Eventual consistency** — recargas exitosas se reflejan
  en ≤ N segundos en el evaluador (configurable).
- **Sin pérdida de evaluaciones** — la transición usa
  doble buffer: el set viejo sigue activo hasta que el
  nuevo está listo.
- **Atomicidad por regla** — si la carga de una regla
  falla, las demás se cargan; el resultado lista los
  errores.

Restricciones aplicables
========================

- **CNST-025** — los reloads se auditan via
  ``AuditService`` con tipo ``CONFIG_CHANGED``.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index` —
  invoca ``reload_rule`` tras CRUD de regla.

Relaciones
==========

- Agregación con ``AlertRuleRepo`` (lee, no posee).
- Agregación con ``AlertEvaluator`` (lo actualiza, no lo
  posee).
- Composición con ``VersionClock`` (componente interno).
