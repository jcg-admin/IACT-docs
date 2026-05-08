.. _uc-usr-07-parte-02:

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
   - Cualquier User autenticado
 * - **Funcion RBAC**
   - ``edit_own_profile``
 * - **AGR**
   - No aplica — capability default por User al creacion
 * - **Justificacion**
   - Self-service: cualquier User puede editar su perfil
     sin requerir admin. La capability se asigna
     automaticamente al crear el User (UC_USR_01).

El actor opera **sobre si mismo** unicamente; el endpoint
infiere ``target_user_id = jwt.user_id`` (no se pasa como
parametro de URL).

2.1.2 Actores Secundarios
--------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **AuthorizationGuard**
   - Verifica funcion ``edit_own_profile`` activa.
 * - **AuditService**
   - Persiste ``PROFILE_UPDATED`` con diff de campos
     (sin valores PII).
 * - **EmailValidator**
   - Verifica formato + unicidad del nuevo email.

2.2 Precondiciones
==================

P1
  El actor esta autenticado (sesion vigente).

P2
  El actor tiene la funcion ``edit_own_profile`` activa.

P3
  El actor esta en estado ``ACTIVE``. Users en
  ``BLOCKED``/``INACTIVE``/``ELIMINATED`` no pueden
  invocar el endpoint (defensa adicional aunque la
  autenticacion ya filtra estos casos).

P4
  El payload contiene al menos un campo a modificar
  (``full_name`` y/o ``email``). Payload vacio → E5.

2.3 Postcondiciones
===================

PostC1
  Los campos especificados en el payload estan
  actualizados en ``User``.

PostC2
  Si ``email`` fue modificado, el nuevo email es unico
  en BD (constraint preservada).

PostC3
  Existe ``AuditEvent PROFILE_UPDATED`` con
  ``actor_id = target_user_id = User.user_id``,
  ``payload = {fields_changed: ['full_name', 'email']}``
  (sin valores PII).

PostC4
  La sesion actual del User permanece vigente. No se
  cierra ni se requiere re-login.
