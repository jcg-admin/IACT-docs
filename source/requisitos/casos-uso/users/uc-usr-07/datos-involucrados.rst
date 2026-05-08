.. _uc-usr-07-parte-07:

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
   - Rol en UC_USR_07
 * - ``user_id``
   - Lectura — derivado de ``jwt.user_id``.
 * - ``full_name``
   - Lectura + escritura (si esta en payload).
 * - ``email``
   - Lectura + escritura con validacion.
 * - ``state``
   - Lectura (precondicion ACTIVE).
 * - ``primary_access_group_id``
   - Sin escritura (campo prohibido por payload).
 * - ``segment_id``
   - Sin escritura.

AuditEvent
-----------

Solo escritura:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Atributo
   - Valor
 * - ``event_type``
   - ``'PROFILE_UPDATED'``
 * - ``actor_id``
   - User editando (= target_user_id en UC_USR_07)
 * - ``target_user_id``
   - mismo que actor_id
 * - ``payload``
   - JSON con
     ``{fields_changed: ['full_name'?, 'email'?]}``.
     **NO contiene los valores** (CNST-026).

7.2 Entrada del endpoint
=========================

::

  PATCH /users/me
  Authorization: Bearer <jwt>
  Content-Type: application/json

  {
    "full_name": "Nuevo Nombre",   // opcional
    "email": "nuevo@example.com"   // opcional
  }

7.3 Salida del endpoint
========================

::

  HTTP 200 OK

  {
    "user_id": "...",
    "full_name": "Nuevo Nombre",
    "email": "nuevo@example.com",
    "updated_at": "2026-05-08T11:30:00Z"
  }

7.4 Validacion de email
========================

7.4.1 Formato
--------------

Regex pragmatico (no full RFC 5322):

::

  ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$

7.4.2 Unicidad
---------------

Constraint UNIQUE en BD sobre ``User.email`` (case-
insensitive). Si la query previa al UPDATE detecta
colision, retorna E4 sin tocar BD. La transaccion atomica
garantiza que entre la query de unicidad y el UPDATE no
hay race condition (row-lock implicito de la transaccion).

7.5 Sin PII en payload audit
=============================

CNST-026: ``PROFILE_UPDATED.payload`` contiene unicamente
``fields_changed`` (lista de nombres). NO contiene
``full_name``, ``email``, ni valores antes/despues.

Para reconstruir el cambio si es necesario, el auditor
consulta los datos en otros sistemas con autorizacion
explicita (no estan en el AuditEvent).
