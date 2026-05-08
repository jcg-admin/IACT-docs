.. _uc-usr-05-parte-05:

==========================================
Parte 5 — Excepciones
==========================================

E1 — Actor sin funcion ``block_users``
=======================================

**Trigger:** paso 2 detecta que el effective_set del
admin NO contiene la funcion ``block_users`` activa.

**Respuesta:** ``403 FORBIDDEN`` con cuerpo
``{error: 'PERMISSION_DENIED', required_function:
'block_users'}``.

**Audit:** AuditService emite ``ACCESS_DENIED`` con
``{actor_id, target_user_id, attempted_action:
'block_users', resource: 'User'}``.

E2 — User objetivo no existe
=============================

**Trigger:** paso 3 no encuentra ``User`` por
``user_id``.

**Respuesta:** ``404 NOT_FOUND`` con
``{error: 'USER_NOT_FOUND'}``.

**Audit:** NO se emite AuditEvent (CNST-026 — no hay
target valido para registrar).

E3 — User objetivo en estado ELIMINATED
========================================

**Trigger:** paso 4 detecta ``User.state = ELIMINATED``
(baja logica via UC_USR_04).

**Respuesta:** ``409 CONFLICT`` con
``{error: 'USER_ELIMINATED', message: 'cannot block
already eliminated user'}``.

**Razon:** ELIMINATED es estado terminal; bloquear no
tiene sentido semantico (la cuenta ya no existe
funcionalmente). Trazabilidad ya esta preservada por el
AuditEvent USER_ELIMINATED.

E4 — Auto-bloqueo prohibido
============================

**Trigger:** paso 5 detecta
``User.user_id = admin.user_id``.

**Respuesta:** ``409 CONFLICT`` con
``{error: 'SELF_BLOCK_FORBIDDEN', message: 'admin cannot
block their own account'}``.

**Razon:** previene lock-out accidental que pueda dejar
sin admins activos al sistema. El desbloqueo de la propia
cuenta requiere otro admin (UC_USR_06 con actor distinto)
— evitar esa cadena de dependencia comenzando por
prohibirla.

E5 — Reason ausente o invalida
===============================

**Trigger:** payload no contiene ``reason`` o tiene 0
caracteres o supera 500 caracteres.

**Respuesta:** ``400 BAD_REQUEST`` con
``{error: 'REASON_REQUIRED', constraint: '1..500
characters'}``.

**Audit:** NO se emite (CNST-026 — error de input no
constituye AuditEvent).

E6 — Falla de transaccion en cierre masivo
===========================================

**Trigger:** falla SQL durante cierre de Sessions o
INSERT de BlacklistedToken (paso 6).

**Respuesta:** ``500 INTERNAL_SERVER_ERROR`` con
``{error: 'BLOCK_FAILED', transaction_rolled_back: true}``.

**Recovery:** la transaccion se hace rollback completo —
``User.state`` no cambia, sesiones quedan abiertas,
tokens NO blacklistados. AuditService emite
``USER_BLOCK_FAILED`` con causa SQL para diagnostico.

**Razon:** atomicidad — el bloqueo o se completa todo o
no se aplica nada. No queda estado inconsistente
(``state=BLOCKED`` con sesiones abiertas).
