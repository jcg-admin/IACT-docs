.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_audit_service:

============
AuditService
============

Punto de entrada único para la emisión de eventos de auditoría.
Orquesta la pipeline completa: validación (``AuditValidator``)
→ sanitización (``Sanitizer`` + ``PIIScanner``) → persistencia
append-only (``AuditRepo``) → notificación post-commit
(``AlertHook``).

Implementa el patrón **P-09 audit-or-abort**: si cualquier paso
falla, el UC invocante recibe la excepción y debe hacer
ROLLBACK de la transacción de negocio. Sin auditoría no hay
escritura.

.. uml::
 :caption: Clase AuditService — fachada de emisión de eventos
           de auditoría con pipeline P-09.

 @startuml

 class AuditService {
   - validator : AuditValidator
   - pii_scanner : PIIScanner
   - sanitizer : Sanitizer
   - repo : AuditRepo
   - alert_hook : AlertHook
   --
   + emit(event : AuditEvent) : EmitResult
   + emit_batch(events : List<AuditEvent>) : List<EmitResult>
   - validate(event : AuditEvent) : ValidationResult
   - sanitize(event : AuditEvent) : AuditEvent
   - persist(event : AuditEvent) : UUID
   - notify_post_commit(event : AuditEvent) : void
 }

 class EmitResult {
   + ok : Boolean
   + event_id : UUID
   + error : String
 }

 class AuditValidator
 class PIIScanner
 class Sanitizer
 class AuditRepo
 class AlertHook

 AuditService "1" *-- "1" AuditValidator : composes
 AuditService "1" *-- "1" PIIScanner : composes
 AuditService "1" *-- "1" Sanitizer : composes
 AuditService "1" o-- "1" AuditRepo : uses
 AuditService "1" o-- "1" AlertHook : uses
 AuditService "1" ..> "1" EmitResult : <<returns>>

 note right of AuditService
   P-09 audit-or-abort:
   fallo en cualquier paso aborta
   la transaccion del UC invocante.
 end note

 @enduml

Pipeline de emit
================

1. ``validate(event)`` — delega a ``AuditValidator``.
2. ``sanitize(event)`` — primero ``PIIScanner.scan()`` para
   detectar y enmascarar; luego ``Sanitizer.normalize()`` para
   forma canónica.
3. ``persist(event)`` — delega a ``AuditRepo.append()``.
4. ``notify_post_commit(event)`` — delega a ``AlertHook`` solo
   tras COMMIT confirmado de la transacción del UC invocante.

Restricciones aplicables
========================

- **CNST-025** — append-only sin UPDATE/DELETE.
- **CNST-026** — sanitización PII obligatoria antes de
  persistir.
- **P-09** — falla de cualquier paso ⇒ ROLLBACK del UC.
- **P-44** — visibilidad audit prio: notificación
  post-commit no bloquea el UC invocante (best-effort, con
  cola de retry).

Trazabilidad a UCs
==================

Invocado por todos los UCs que producen eventos auditables.
Subset representativo:

- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index` (LOGIN)
- :doc:`/requisitos/casos-uso/access/uc-acc-01/index`
  (PERMISSION_GRANT)
- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`
  (ACCESS_GROUP_COMPOSITION_CHANGED)
- :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`
  (ALERT_ACKNOWLEDGED)
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index`
  (ETL_RETRY)

Relaciones
==========

- Composición fuerte con ``AuditValidator``, ``PIIScanner``,
  ``Sanitizer``: estos componentes solo existen como parte del
  servicio.
- Agregación con ``AuditRepo``: el repo puede existir
  independientemente y ser usado por ``AuditQueryService``.
- Agregación con ``AlertHook``: el hook tiene su propio ciclo
  de vida y puede ser invocado por otros productores.
