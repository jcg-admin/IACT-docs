.. _uc-usr-07-parte-03:

==========================================
Parte 3 — Flujo principal
==========================================

3.1 Disparador
==============

El User autenticado solicita actualizar su perfil con
``PATCH /users/me`` con un payload parcial conteniendo los
campos a modificar.

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
   - User
   - ``PATCH /users/me`` con
     ``{full_name?, email?}``
   -
 * - 2
   -
   -
   - ``AuthorizationGuard`` verifica funcion
     ``edit_own_profile`` activa. Negativo → E1.
 * - 3
   -
   -
   - Carga ``User`` por ``jwt.user_id`` (no se pasa en
     URL — infiere del JWT).
 * - 4
   -
   -
   - Verifica ``User.state = ACTIVE``. Otro estado → E2.
 * - 5
   -
   -
   - Valida payload: al menos un campo presente, formato
     correcto. Vacio o invalido → E5/E6.
 * - 6
   -
   -
   - Si se incluye ``email`` y difiere del actual:

     - Verifica formato (regex).
     - Verifica unicidad (no colision). Caso negativo →
       E3 / E4.
 * - 7
   -
   -
   - Inicia transaccion atomica:

     1. ``UPDATE User SET <campos modificados>``.
     2. ``AuditService.emit('PROFILE_UPDATED',
        {actor_id, target_user_id,
        fields_changed: [...]})``.
 * - 8
   -
   -
   - Commit transaccion.
 * - 9
   -
   -
   - Responde ``200 OK`` con
     ``{user_id, full_name, email, updated_at}``.
 * - 10
   - User
   - Recibe confirmacion del cambio
   -

3.3 Salida
==========

El perfil queda actualizado. La sesion permanece
vigente; siguientes operaciones del User retornan los
nuevos valores en endpoints como ``GET /users/me``.

3.4 Idempotencia
================

UC_USR_07 es **idempotente cuando el payload coincide
con el estado actual** (ej. ``full_name`` enviado igual
al ``full_name`` ya guardado): la transaccion se ejecuta
pero NO emite ``PROFILE_UPDATED`` (no hay diff). Ver
flujo alterno A1.
