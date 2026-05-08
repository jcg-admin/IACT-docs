.. _uc-usr-05-parte-04:

==========================================
Parte 4 — Flujos alternos
==========================================

A1 — User ya esta BLOCKED
==========================

**Trigger:** paso 4 detecta ``User.state = BLOCKED``.

**Flujo:**

1. Sistema NO ejecuta cambio de estado (idempotencia
   logica — ya esta bloqueado).
2. Sistema NO emite AuditEvent (no hay transicion).
3. Sistema responde ``200 OK`` con
   ``{user_id, state: 'BLOCKED', already_blocked: true}``.

**Razon:** evitar duplicar AuditEvents y no falsificar la
trazabilidad del bloqueo original (que pudo haber sido
manual previo o automatico BR-015).

A2 — User esta INACTIVE
========================

**Trigger:** paso 4 detecta ``User.state = INACTIVE``.

**Flujo:**

1. Sistema permite la transicion ``INACTIVE → BLOCKED``
   (admin tiene autoridad para imponer estado mas
   restrictivo).
2. NO hay sesiones que cerrar (User INACTIVE no puede
   tener Sessions ACTIVE — invariante preservada por
   UC_USR_03).
3. NO hay tokens que blacklistar (token vivo implica
   sesion vigente).
4. AuditService emite ``USER_BLOCKED`` con
   ``{from_state: 'INACTIVE', sessions_closed_count: 0,
   tokens_blacklisted_count: 0}``.
5. Responde ``200 OK``.

**Razon:** un User inactivado por compliance puede
necesitar ser bloqueado adicionalmente (semantica:
INACTIVE = no puede entrar al sistema; BLOCKED = no
puede entrar Y existe causa administrativa que requiere
trazabilidad).

A3 — Bloqueo automatico ya hizo la transicion (BR-015)
=======================================================

**Trigger:** paso 4 detecta ``User.state = BLOCKED`` Y el
ultimo AuditEvent es ``ACCOUNT_LOCKED`` (automatico
BR-015), no ``USER_BLOCKED`` (manual).

**Flujo:**

1. Sistema NO duplica el bloqueo (User ya esta BLOCKED).
2. AuditService emite ``USER_BLOCK_REASON_OVERRIDE`` con
   ``{actor_id, target_user_id, original_reason:
   'FAILED_LOGIN_LIMIT', new_reason: '<motivo admin>'}``.
3. Esto preserva la trazabilidad del bloqueo automatico
   pero anota que un admin agrego razon administrativa
   adicional (e.g., investigacion subsecuente).
4. Responde ``200 OK`` con ``{state: 'BLOCKED',
   reason_overridden: true}``.

**Razon:** soporta el caso real donde BR-015 bloqueo a un
User por intentos fallidos y posteriormente un admin
investiga y agrega contexto. El estado no cambia, la
historia se enriquece.
