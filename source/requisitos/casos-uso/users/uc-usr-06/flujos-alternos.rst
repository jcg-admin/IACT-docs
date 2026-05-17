.. _uc-usr-06-parte-04:

==========================================
Parte 4 — Flujos alternos
==========================================

A1 — User ya esta ACTIVE
=========================

**Trigger:** paso 4 detecta ``User.state = ACTIVE``.

**Flujo:**

1. Sistema NO ejecuta cambio (ya esta activo).
2. NO emite AuditEvent (no hay transicion).
3. Responde ``200 OK`` con
   ``{user_id, state: 'ACTIVE', already_unblocked: true}``.

A2 — User BLOCKED sin AuditEvent de bloqueo previo
====================================================

**Trigger:** paso 6 NO encuentra AuditEvent
``USER_BLOCKED`` ni ``ACCOUNT_LOCKED`` previo para el
User (estado inconsistente — el state=BLOCKED apareció
sin trazabilidad).

**Flujo:**

1. Sistema emite warning de auditoria
   ``USER_STATE_INCONSISTENCY`` para investigar el origen
   del state.
2. Procede con el desbloqueo igualmente para no dejar al
   User atrapado en el estado.
3. AuditEvent ``USER_UNBLOCKED`` se emite con
   ``original_block_event_id = null`` y
   ``original_block_type = 'UNKNOWN'``.

**Razon:** la consistencia del state es responsabilidad
del sistema; un User en BLOCKED siempre debe poder
desbloquearse aunque la trazabilidad este rota
(diagnostico se hace por separado).

A3 — User INACTIVE
===================

**Trigger:** paso 4 detecta ``User.state = INACTIVE``.

**Flujo:**

1. Sistema NO procede con desbloqueo a ACTIVE — la
   semantica de INACTIVE es "no puede entrar al sistema
   por compliance"; restaurar a ACTIVE viola esa
   invariante.
2. Responde ``409 INVALID_STATE_TRANSITION`` con
   ``{from: 'INACTIVE', to_requested: 'ACTIVE',
   reason: 'use UC_USR_03 para reactivar usuario inactivo'}``.

**Razon:** UC_USR_06 es especificamente "desbloquear"
(BLOCKED→ACTIVE). Reactivar INACTIVE→ACTIVE es scope de
UC_USR_03 (modify) que tiene su propia logica de
verificacion.
