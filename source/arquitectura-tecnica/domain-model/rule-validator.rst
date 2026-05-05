.. meta::
 :artefacto: AT_DM_CLASS_RULE_VALIDATOR
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

.. _dm_class_rule_validator:

=============
RuleValidator
=============

Validador de admisibilidad de una ``AlertRule`` antes de
persistirla. Verifica que la regla sea **estructuralmente
correcta**, **semánticamente coherente** y **autorizada**
para el ``scope`` declarado por el usuario que la edita.

Es invocado por el servicio de configuración antes del
``save()``. Si la validación falla, ningún cambio se
propaga al evaluador (``EvaluatorReloader``) ni al
repositorio (``AlertRuleRepo``).

.. uml::
 :caption: Clase RuleValidator — gate de admisibilidad de
           AlertRule (estructura + semántica + autorización).

 @startuml

 class RuleValidator {
   - metric_catalog : MetricCatalog
   - segment_resolver : SegmentResolver
   --
   + validate(rule : AlertRule, invoker : User) : ValidationReport
   + validate_structure(rule : AlertRule) : List<ValidationError>
   + validate_metric_known(rule : AlertRule) : Boolean
   + validate_condition_coherent(rule : AlertRule) : Boolean
   + validate_window_positive(rule : AlertRule) : Boolean
   + validate_scope_authorized(rule : AlertRule, invoker : User) : Boolean
   + validate_actions_executable(rule : AlertRule) : List<ValidationError>
 }

 class ValidationReport {
   + ok : Boolean
   + errors : List<ValidationError>
   + warnings : List<ValidationWarning>
   --
   + has_blocking_errors() : Boolean
 }

 class ValidationError {
   + field : String
   + code : ErrorCode
   + message : String
 }

 class ValidationWarning {
   + field : String
   + message : String
 }

 enum ErrorCode {
   STRUCTURE_INVALID
   METRIC_UNKNOWN
   CONDITION_INCOHERENT
   WINDOW_NEGATIVE
   SCOPE_UNAUTHORIZED
   ACTION_NOT_EXECUTABLE
 }

 class AlertRule
 class User
 class MetricCatalog
 class SegmentResolver

 RuleValidator o-- MetricCatalog : reads
 RuleValidator o-- SegmentResolver : reads
 RuleValidator ..> AlertRule : validates
 RuleValidator ..> User : checks scope
 RuleValidator ..> ValidationReport : returns
 ValidationReport *-- "*" ValidationError
 ValidationReport *-- "*" ValidationWarning
 ValidationError -- ErrorCode

 note right of RuleValidator
   Bloquea persistencia de reglas
   malformadas, semánticamente
   incoherentes o con scope no
   autorizado para el invoker.
 end note

 @enduml

Capas de validación
===================

1. **Estructural** — campos requeridos presentes, tipos
   correctos, formato válido.
2. **Catálogo** — la métrica referenciada existe en el
   ``MetricCatalog``; la agregación es compatible con la
   métrica.
3. **Coherencia semántica** — la condición tiene sentido
   para la métrica y la agregación (ej. ``COUNT > 0`` es
   coherente; ``AVG > 0`` solo si la métrica acepta
   negativos).
4. **Autorización de scope** — el ``invoker`` tiene
   visibilidad sobre el ``scope`` declarado (CNST-008
   segmentación).
5. **Acciones ejecutables** — las acciones referenciadas
   existen y el ``invoker`` puede invocarlas.

Restricciones aplicables
========================

- **CNST-008** — segmentación: scope cross-segmento
  bloqueado salvo permiso explícito.
- **P-15** — RBAC granular: configurar reglas requiere
  ``manage_alert_rules``.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index` —
  validación previa a CRUD.

Relaciones
==========

- Agregación con ``MetricCatalog`` y ``SegmentResolver``
  (servicios externos al bounded context).
- Valida instancias de ``AlertRule`` sin modificarlas.
- Devuelve ``ValidationReport`` consumido por el servicio
  de configuración.
