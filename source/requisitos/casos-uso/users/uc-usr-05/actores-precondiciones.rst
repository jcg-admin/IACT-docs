.. _uc-usr-05-parte-02:

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
   - ``block_users``
 * - **AGR tipico**
   - AGR-002 ``user_admin_group``
 * - **Justificacion**
   - El bloqueo administrativo es operacion sensible
     restringida a admins con autorizacion explicita.

El actor primario inicia el UC manualmente; el sistema
**nunca** dispara UC_USR_05 directamente (eso es BR-015,
distinto).

2.1.2 Actores Secundarios
--------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **AuthorizationGuard**
   - Verifica que el admin posea la funcion ``block_users``
     activa antes de permitir el bloqueo.
 * - **AuditService**
   - Persiste el AuditEvent ``USER_BLOCKED`` inmutable.
 * - **User bloqueado**
   - Receptor del efecto. No interactua con el UC
     directamente; recibe (a partir de la transicion) las
     respuestas 401 en cualquier endpoint protegido.

2.2 Precondiciones
==================

P1
  El actor primario esta autenticado (sesion vigente).

P2
  El actor primario tiene la funcion ``block_users``
  activa en su effective_set.

P3
  El User objetivo existe en BD (``user_id`` valido).

P4
  El User objetivo NO esta en estado ``ELIMINATED``
  (eliminacion ya es terminal — ver UC_USR_04).

P5
  El User objetivo NO es el propio actor (un admin no
  puede auto-bloquearse — proteccion contra
  lock-out accidental).

2.3 Postcondiciones
===================

PostC1
  ``User.state = BLOCKED``.

PostC2
  Todas las Sessions del User en estado ACTIVE pasan a
  ``state = CLOSED`` con ``close_reason = 'USER_BLOCKED'``
  y ``closed_at = now``.

PostC3
  Todos los refresh tokens vivos del User estan en
  ``BlacklistedToken`` (INSERT por cada token).

PostC4
  Existe un ``AuditEvent`` tipo ``USER_BLOCKED`` con
  ``actor_id = admin``, ``target_user_id = User.user_id``,
  ``reason = motivo administrativo``, contadores
  ``sessions_closed``, ``tokens_blacklisted``.

PostC5
  Cualquier intento futuro de login del User responde
  401 con codigo ``ACCOUNT_BLOCKED`` hasta que UC_USR_06
  lo desbloquee.
