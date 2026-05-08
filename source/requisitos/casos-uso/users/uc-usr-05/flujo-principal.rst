.. _uc-usr-05-parte-03:

==========================================
Parte 3 — Flujo principal
==========================================

3.1 Disparador
==============

El admin autenticado solicita el bloqueo de un User
objetivo desde la interfaz administrativa, especificando:

- ``user_id`` del User a bloquear.
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
   - ``POST /users/{user_id}/block`` con
     ``{reason: "..."}``
   -
 * - 2
   -
   -
   - ``AuthorizationGuard`` verifica funcion
     ``block_users`` activa en el effective_set del admin.
     Caso negativo → excepcion E1 (ver excepciones).
 * - 3
   -
   -
   - Carga ``User`` por ``user_id``. Si no existe →
     excepcion E2.
 * - 4
   -
   -
   - Verifica ``User.state = ACTIVE``. Otro estado →
     flujo alterno A1, A2 o excepcion E3.
 * - 5
   -
   -
   - Verifica ``User.user_id != admin.user_id``. Si
     coinciden → excepcion E4 (auto-bloqueo prohibido).
 * - 6
   -
   -
   - Inicia transaccion atomica:

     1. ``UPDATE User SET state='BLOCKED' WHERE user_id``.
     2. ``UPDATE Session SET state='CLOSED',
        close_reason='USER_BLOCKED', closed_at=now
        WHERE user_id AND state='ACTIVE'`` (registra
        ``sessions_closed_count``).
     3. ``INSERT INTO BlacklistedToken
        (token_hash, user_id, blacklisted_at, reason)``
        por cada refresh token vivo del User (registra
        ``tokens_blacklisted_count``).
     4. ``AuditService.emit('USER_BLOCKED',
        {actor_id, target_user_id, reason,
        sessions_closed_count, tokens_blacklisted_count})``.
 * - 7
   -
   -
   - Commit transaccion.
 * - 8
   -
   -
   - Responde ``200 OK`` con
     ``{user_id, state: 'BLOCKED', blocked_at,
     sessions_closed_count, tokens_blacklisted_count}``.
 * - 9
   - Admin
   - Recibe confirmacion del bloqueo
   -

3.3 Salida
==========

El User queda bloqueado. Cualquier intento de login en
adelante responde ``401 ACCOUNT_BLOCKED``. Las sesiones
del User reciben tambien ``401`` en el siguiente
refresh-token o request protegido (token blacklisteado).

3.4 Idempotencia
================

UC_USR_05 NO es idempotente: si el User ya esta en
``BLOCKED``, una segunda invocacion responde con flujo
alterno A1 (ver flujos-alternos.rst). El sistema NO
re-emite ``USER_BLOCKED`` ni cierra sesiones (ya cerradas).
