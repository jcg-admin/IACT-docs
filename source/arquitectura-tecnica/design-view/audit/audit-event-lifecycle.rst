.. meta::
 :artefacto: AT_DESIGN_STATE_AUDIT_EVENT
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: AuditEvent
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_audit_event:

============================================================
Design View — Ciclo de Vida: AuditEvent
============================================================

Maquina de estados de un ``AuditEvent``. El modelo es **append-only,
inmutable** (CNST-025): un evento, una vez persistido, no se
modifica. La FSM cubre la trayectoria desde la captura por el
middleware hasta la purga eventual segun politica de retencion.

.. uml::
 :caption: AuditEvent FSM — RECEIVED -> PERSISTED -> PURGED.

 @startuml

 [*] --> RECEIVED : middleware.intercept()\n(request entrante)

 RECEIVED --> PERSISTED : audit-validator.persist()\n(write succeeded, hash chained)
 RECEIVED --> REJECTED  : audit-validator.persist()\n(write failed)

 PERSISTED --> PURGED : retention-policy.expire()\n(retencion vencida)

 PURGED   --> [*]
 REJECTED --> [*] : alert (audit gap)

 note right of RECEIVED
   Estado transitorio en memoria.
   Si el proceso muere antes de
   persistir, se pierde el evento
   (riesgo aceptado: el log normal
   captura el request).
 end note

 note right of PERSISTED
   Append-only. Cada evento incluye
   ``hash_prev`` encadenado para
   verificacion de integridad.
 end note

 note bottom of REJECTED
   Caso anormal — write fail al
   storage de audit. Dispara alerta
   inmediata (audit gap) y se
   investiga manualmente.
 end note

 note bottom of PURGED
   Eliminacion fisica tras retencion
   (politica regulatoria). El hash
   chain se preserva mediante un
   marker de purga.
 end note

 @enduml

Invariantes
============

- **I-AUD-01:** ``PERSISTED`` es un estado terminal en
  cuanto a contenido — no admite UPDATE. Cualquier cambio
  posterior crea un nuevo ``AuditEvent`` (e.g. correccion).
- **I-AUD-02:** ``hash_prev`` debe coincidir con el ``hash``
  del evento inmediato anterior. Una ruptura del chain
  dispara alerta de tampering.
- **I-AUD-03:** ``REJECTED`` no es un evento persistido en
  el log de audit — es una alerta operativa.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-validator` —
   service que ejecuta la transicion ``RECEIVED → PERSISTED``.
 - :doc:`bounded-context` — contexto del modulo Audit.
 - :doc:`interaction-pattern` — patron de captura por
   middleware.
