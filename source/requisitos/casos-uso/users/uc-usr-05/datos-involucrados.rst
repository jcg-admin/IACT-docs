.. _uc-usr-05-parte-07:

==========================================
Parte 7 — Datos involucrados
==========================================

7.1 Entidades primarias
========================

User
----

Atributos relevantes para UC_USR_05:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Rol en UC_USR_05
 * - ``user_id : UUID``
   - Identificador del User a bloquear (input).
 * - ``state : UserState``
   - Lectura del estado origen (ACTIVE/INACTIVE/BLOCKED/
     ELIMINATED) y escritura a ``BLOCKED``.
 * - ``primary_access_group_id``
   - Sin escritura — se preserva.
 * - ``segment_id``
   - Sin escritura — se preserva.

Session
-------

Cierre masivo de sesiones del User:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Rol en UC_USR_05
 * - ``session_id``
   - Identificador.
 * - ``user_id``
   - Filtro de la query masiva.
 * - ``state``
   - Lectura ``ACTIVE`` → escritura ``CLOSED``.
 * - ``close_reason``
   - Escritura ``'USER_BLOCKED'``.
 * - ``closed_at``
   - Escritura ``now``.

BlacklistedToken
-----------------

INSERT N tokens:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Rol en UC_USR_05
 * - ``token_hash``
   - Hash del refresh token vivo.
 * - ``user_id``
   - FK al User bloqueado.
 * - ``blacklisted_at``
   - ``now``.
 * - ``reason``
   - ``'USER_BLOCKED'``.

AuditEvent
-----------

Insercion de evento USER_BLOCKED:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Rol en UC_USR_05
 * - ``event_id : UUID``
   - PK generada.
 * - ``event_type``
   - ``'USER_BLOCKED'`` o ``'USER_BLOCK_REASON_OVERRIDE'``
     (alterno A3).
 * - ``actor_id``
   - admin ejecutor.
 * - ``target_user_id``
   - User bloqueado.
 * - ``occurred_at``
   - ``now``.
 * - ``payload``
   - JSON con
     ``{reason, sessions_closed_count,
     tokens_blacklisted_count, from_state}``.

7.2 Entrada del endpoint
=========================

::

  POST /users/{user_id}/block
  Authorization: Bearer <jwt>
  Content-Type: application/json

  {
    "reason": "investigacion ABC-123"
  }

7.3 Salida del endpoint
========================

::

  HTTP 200 OK

  {
    "user_id": "...",
    "state": "BLOCKED",
    "blocked_at": "2026-05-08T10:23:45Z",
    "sessions_closed_count": 2,
    "tokens_blacklisted_count": 3
  }

7.4 Sin PII en payload audit
=============================

CNST-026 aplica: el AuditEvent.payload NO contiene email,
full_name, ni cualquier dato de identidad personal del
User bloqueado. Solo identificadores y contadores
agregados.
