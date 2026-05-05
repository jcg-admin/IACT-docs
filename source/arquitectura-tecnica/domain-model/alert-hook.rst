.. meta::
 :artefacto: AT_DM_CLASS_ALERT_HOOK
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

.. _dm_class_alert_hook:

=========
AlertHook
=========

Hook que se dispara **post-commit** de un ``AuditEvent`` para
notificar al motor de alertas (``AlertEngine``, bounded
context Alerts) cuando el evento coincide con reglas
configuradas. Es el puente entre Audit y Alerts.

Operación clave: ``on_commit(event)``. Se invoca SOLO tras
COMMIT confirmado de la transacción del UC invocante.
Best-effort: si falla la notificación, el evento ya está
persistido y el UC ya completó; se reintenta con
backoff exponencial vía cola de retry.

.. uml::
 :caption: Clase AlertHook — puente Audit → Alerts disparado
           post-commit.

 @startuml

 class AlertHook {
   - alert_engine : AlertEngine
   - retry_queue : RetryQueue
   - rule_matcher : AlertRuleMatcher
   - max_retries : Integer
   --
   + on_commit(event : AuditEvent) : NotifyResult
   + retry_pending() : Integer
   - match_rules(event : AuditEvent) : List<AlertRule>
   - dispatch(event : AuditEvent, rule : AlertRule) : void
   - schedule_retry(event : AuditEvent, attempt : Integer) : void
 }

 class NotifyResult {
   + ok : Boolean
   + matched_rules_count : Integer
   + dispatched_count : Integer
   + failures : List<NotifyFailure>
 }

 class NotifyFailure {
   + rule_id : UUID
   + reason : String
   + retry_scheduled : Boolean
 }

 class AlertEngine
 class AlertRuleMatcher
 class RetryQueue
 class AuditEvent

 AlertHook o-- AlertEngine : notifies
 AlertHook *-- AlertRuleMatcher : composes
 AlertHook o-- RetryQueue : uses
 AlertHook ..> AuditEvent : reads
 AlertHook ..> NotifyResult : returns
 NotifyResult *-- "*" NotifyFailure

 note right of AlertHook
   Best-effort post-commit.
   Fallo no afecta UC invocante:
   evento ya persistido, retry async.
 end note

 @enduml

Operaciones principales
=======================

- ``on_commit(event)`` — invocada por ``AuditService`` solo
  tras COMMIT confirmado. Detecta reglas que matchean y
  dispara notificaciones.
- ``retry_pending()`` — procesa la cola de retry para
  notificaciones que fallaron en intentos previos.
  Devuelve cantidad de jobs procesados.
- ``schedule_retry(event, attempt)`` — encola para
  reintento con backoff exponencial; si ``attempt >
  max_retries`` el evento se marca como
  ``DELIVERY_ABANDONED`` (visible solo en monitoreo
  interno, no afecta UC).

Garantías
=========

- **At-least-once delivery** — se reintentará hasta
  ``max_retries`` veces.
- **No bloquea UC invocante** — fallar en
  ``on_commit`` no rompe el flujo del usuario.
- **Idempotencia** — el ``AlertEngine`` es responsable
  de deduplicar dispatches con el mismo
  ``(event_id, rule_id)``.

Restricciones aplicables
========================

- **P-44** — visibilidad audit prio: alertas críticas se
  generan post-commit sin bloquear ROLLBACK.
- **CNST-024** — retención de retry queue acotada por
  política.

Trazabilidad a UCs
==================

Indirectamente involucrado en todo UC que escriba
``AuditEvent`` con tipos que matchean ``AlertRule``
configuradas. Especialmente:

- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index`
  (LOGIN fallido → alerta de seguridad).
- :doc:`/requisitos/casos-uso/access/uc-acc-01/index`
  (PERMISSION_GRANT → alerta a auditor).
- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`
  (cambio de composición → alerta a sec officer).

Relaciones
==========

- Agregación con ``AlertEngine`` (bounded context
  Alerts; ciclo de vida independiente).
- Composición con ``AlertRuleMatcher`` (componente
  interno).
- Agregación con ``RetryQueue`` (servicio de
  infraestructura).
- Lee instancias de ``AuditEvent`` sin modificarlas.
