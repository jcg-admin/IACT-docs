.. _uc-usr-06-parte-02:

==========================================
Parte 2 — Actores y precondiciones
==========================================

2.1 Actores
===========

2.1.1 Actor Principal
---------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Rol**
   - Admin de Usuarios
 * - **Funcion RBAC**
   - ``unblock_users``
 * - **AGR tipico**
   - AGR-002 ``user_admin_group``
 * - **Justificacion**
   - El desbloqueo restaura acceso al sistema; restringido
     a admins con autorizacion explicita.

2.1.2 Actores Secundarios
--------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **AuthorizationGuard**
   - Verifica que el admin posea la funcion
     ``unblock_users`` activa.
 * - **AuditService**
   - Persiste el AuditEvent ``USER_UNBLOCKED`` y consulta
     el evento original de bloqueo para enriquecer la
     payload.
 * - **User desbloqueado**
   - Receptor del efecto. No interactua con el UC; al
     proximo intento de login obtiene exito (vs 401
     ACCOUNT_BLOCKED previo).

2.2 Precondiciones
==================

P1
  El actor primario esta autenticado (sesion vigente).

P2
  El actor primario tiene la funcion ``unblock_users``
  activa en su effective_set.

P3
  El User objetivo existe en BD.

P4
  El User objetivo esta en estado ``BLOCKED``. Otro
  estado origen → flujo alterno o excepcion (ver A1, E3).

P5
  El admin no se desbloquea a si mismo (no aplica en
  practica — un BLOCKED user no puede autenticarse, asi
  que no podria invocar el endpoint; mantenemos el check
  por simetria con UC_USR_05 y por defensa contra
  manipulacion de session admin previa).

2.3 Postcondiciones
===================

PostC1
  ``User.state = ACTIVE``.

PostC2
  Existe ``AuditEvent USER_UNBLOCKED`` con:

  - ``actor_id = admin``,
  - ``target_user_id = User.user_id``,
  - ``original_block_event_id`` = event_id del ultimo
    USER_BLOCKED o ACCOUNT_LOCKED del User,
  - ``reason`` = motivo administrativo del desbloqueo.

PostC3
  Sessions cerradas durante el bloqueo permanecen
  cerradas. El User debe re-loguear.

PostC4
  Tokens blacklistados permanecen blacklistados.

PostC5
  Assignments del User (suspendidos logicamente durante
  el bloqueo) vuelven a ser efectivos para el calculo
  de effective_set en la proxima sesion.
