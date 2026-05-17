.. _uc-usr-06-parte-05:

==========================================
Parte 5 — Excepciones
==========================================

E1 — Actor sin funcion ``unblock_users``
==========================================

**Trigger:** paso 2 detecta funcion ausente.

**Respuesta:** ``403 PERMISSION_DENIED`` con
``{error: 'PERMISSION_DENIED', required_function:
'unblock_users'}``.

**Audit:** ``ACCESS_DENIED`` con
``attempted_action: 'unblock_users'``.

E2 — User objetivo no existe
=============================

**Trigger:** paso 3 no encuentra User.

**Respuesta:** ``404 USER_NOT_FOUND``.

**Audit:** NO se emite (CNST-026).

E3 — User en estado ELIMINATED
===============================

**Trigger:** paso 4 detecta ``User.state = ELIMINATED``.

**Respuesta:** ``409 USER_ELIMINATED`` con
``{message: 'cannot unblock eliminated user; ELIMINATED
is terminal state'}``.

**Razon:** ELIMINATED es estado terminal. Recovery de
ELIMINATED requiere otro UC administrativo no incluido
en el cluster actual.

E4 — Auto-desbloqueo prohibido
================================

**Trigger:** paso 5 detecta
``User.user_id = admin.user_id``.

**Respuesta:** ``409 SELF_UNBLOCK_FORBIDDEN`` con
``{message: 'admin cannot unblock their own account;
contact another admin'}``.

**Razon:** simetria con UC_USR_05. En la practica, un
admin BLOCKED no puede autenticarse para invocar el
endpoint, pero el check defiende contra escenarios de
manipulacion de session admin.

E5 — Reason ausente o invalida
================================

**Trigger:** payload invalido (sin ``reason``, vacia, o
>500 chars).

**Respuesta:** ``400 REASON_REQUIRED`` con
``constraint: '1..500 characters'``.

E6 — Falla de transaccion
==========================

**Trigger:** falla SQL durante UPDATE o emit.

**Respuesta:** ``500 UNBLOCK_FAILED``,
``transaction_rolled_back: true``.

**Recovery:** rollback completo —
``User.state`` permanece BLOCKED. AuditService emite
``USER_UNBLOCK_FAILED`` con causa SQL.

**Razon:** atomicidad — el estado o se restaura todo
(state + AuditEvent) o nada.
