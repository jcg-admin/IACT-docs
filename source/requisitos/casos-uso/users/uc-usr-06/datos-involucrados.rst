.. _uc-usr-06-parte-07:

==========================================
Parte 7 — Datos involucrados
==========================================

7.1 Entidades primarias
========================

User
----

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Rol en UC_USR_06
 * - ``user_id``
   - Identificador (input).
 * - ``state``
   - Lectura ``BLOCKED`` → escritura ``ACTIVE``.
 * - ``primary_access_group_id``
   - Sin escritura — preservado.
 * - ``segment_id``
   - Sin escritura — preservado.

AuditEvent
-----------

Doble rol:

- **Lectura:** lookup del ultimo evento de bloqueo
  (``USER_BLOCKED`` / ``ACCOUNT_LOCKED`` /
  ``USER_BLOCK_REASON_OVERRIDE``) para capturar
  ``original_block_event_id``.
- **Escritura:** insercion del nuevo
  ``USER_UNBLOCKED``.

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo del USER_UNBLOCKED emitido
   - Valor
 * - ``event_type``
   - ``'USER_UNBLOCKED'``
 * - ``actor_id``
   - admin
 * - ``target_user_id``
   - User desbloqueado
 * - ``payload``
   - JSON con ``{reason, original_block_event_id,
     original_block_type, from_state}``

7.2 Entrada del endpoint
=========================

::

  POST /users/{user_id}/unblock
  Authorization: Bearer <jwt>
  Content-Type: application/json

  {
    "reason": "investigacion concluida sin sancion"
  }

7.3 Salida del endpoint
========================

::

  HTTP 200 OK

  {
    "user_id": "...",
    "state": "ACTIVE",
    "unblocked_at": "2026-05-08T11:00:00Z",
    "original_block_event_id": "..."
  }

7.4 Sin PII en payload audit
=============================

CNST-026 aplica. payload del AuditEvent no contiene
email, full_name ni datos personales del User.
