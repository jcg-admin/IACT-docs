.. _uc-usr-06-parte-03:

==========================================
Parte 3 — Flujo principal
==========================================

3.1 Disparador
==============

El admin autenticado solicita el desbloqueo de un User
desde la interfaz administrativa, especificando:

- ``user_id`` del User a desbloquear.
- ``reason`` (texto libre obligatorio, max 500 caracteres).

3.2 Flujo nominal
=================

.. list-table::
 :widths: 5 30 30 35
 :header-rows: 1

 * - #
   - Actor
   - Accion
   - Sistema
 * - 1
   - Admin
   - ``POST /users/{user_id}/unblock`` con
     ``{reason: "..."}``
   -
 * - 2
   -
   -
   - ``AuthorizationGuard`` verifica funcion
     ``unblock_users`` activa. Negativo → E1.
 * - 3
   -
   -
   - Carga ``User`` por ``user_id``. No existe → E2.
 * - 4
   -
   -
   - Verifica ``User.state = BLOCKED``. Otro estado →
     A1 (idempotencia) o E3.
 * - 5
   -
   -
   - Verifica ``User.user_id != admin.user_id`` (defensa
     simetrica con UC_USR_05). Coinciden → E4.
 * - 6
   -
   -
   - Lookup del ultimo AuditEvent del User cuyo
     ``event_type`` esta en
     ``{USER_BLOCKED, ACCOUNT_LOCKED,
     USER_BLOCK_REASON_OVERRIDE}``. Captura
     ``original_block_event_id``. Si no existe AuditEvent
     de bloqueo previo → flujo alterno A2 (estado
     inconsistente — emitir warning pero proceder).
 * - 7
   -
   -
   - Inicia transaccion atomica:

     1. ``UPDATE User SET state='ACTIVE' WHERE user_id``.
     2. ``AuditService.emit('USER_UNBLOCKED',
        {actor_id, target_user_id, reason,
        original_block_event_id, original_block_type})``.
 * - 8
   -
   -
   - Commit transaccion.
 * - 9
   -
   -
   - Responde ``200 OK`` con
     ``{user_id, state: 'ACTIVE', unblocked_at,
     original_block_event_id}``.
 * - 10
   - Admin
   - Recibe confirmacion del desbloqueo
   -

3.3 Salida
==========

El User puede iniciar sesion normalmente. La proxima
invocacion de UC_AUTH_01 con sus credenciales validas
genera nueva Session y nuevos tokens.

3.4 Idempotencia
================

UC_USR_06 NO es idempotente: si el User ya esta
``ACTIVE``, una segunda invocacion responde con flujo
alterno A1 (ver flujos-alternos.rst). El sistema NO
re-emite ``USER_UNBLOCKED`` ni cambia el estado.
