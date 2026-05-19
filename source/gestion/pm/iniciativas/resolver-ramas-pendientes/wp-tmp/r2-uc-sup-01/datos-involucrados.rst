.. _uc-sup-01-parte-07:

==========================================
Parte 7 — Datos involucrados
==========================================

7.1 Entidades principales
==========================

MonitorSession
--------------

Registro de una sesión de monitoreo activa o histórica.

.. list-table::
 :widths: 20 20 15 45
 :header-rows: 1

 * - Campo
   - Tipo
   - Nulable
   - Descripción
 * - ``id``
   - UUID
   - No
   - Identificador único de la sesión de monitoreo.
     Generado por el Backend al crear la sesión (PASO 8).
 * - ``supervisor_id``
   - FK → User
   - No
   - Usuario que inició el monitoreo. Posee
     ``SUP-001 monitor_live_calls``.
 * - ``call_id``
   - String
   - No
   - Identificador de la llamada activa en TelephonyClient.
 * - ``agent_id``
   - FK → User
   - No
   - Agente en la llamada monitoreada. Recuperado de
     ``ActiveCallRepository`` en PASO 6.
 * - ``mode``
   - Enum(``silent``, ``whisper``)
   - No
   - Modo de monitoreo activo. Actualizable via FA-01.
 * - ``reason``
   - String (≥20 ch)
   - No
   - Justificación de compliance proporcionada por el supervisor.
 * - ``state``
   - Enum(``ACTIVE``, ``ENDED``, ``AUTO_ENDED``, ``FAILED``)
   - No
   - Estado actual de la sesión.
 * - ``started_at``
   - DateTime
   - No
   - Timestamp UTC de inicio (NOW() en PASO 8).
 * - ``ended_at``
   - DateTime
   - Sí
   - Timestamp UTC de cierre. Nulo mientras la sesión
     está ``ACTIVE``.
 * - ``end_reason``
   - String
   - Sí
   - Razón de cierre: ``SUPERVISOR_STOP``, ``CALL_ENDED``,
     ``TELEPHONY_FAILED``. Nulo si la sesión está activa.

----

AuditEvent — CALL_MONITORED
-----------------------------

Registro inmutable (CNST-025) del evento de inicio de monitoreo.

.. list-table::
 :widths: 20 20 60
 :header-rows: 1

 * - Campo
   - Tipo
   - Valor en este UC
 * - ``event_type``
   - String
   - ``CALL_MONITORED``
 * - ``actor_user_id``
   - FK → User
   - ID del supervisor invocante.
 * - ``occurred_at``
   - DateTime
   - NOW() — mismo timestamp que ``MonitorSession.started_at``.
 * - ``payload``
   - JSONB
   - ``{call_id, agent_id, mode, reason, monitor_session_id}``

**Campos del payload:**

.. code-block:: json

 {
   "call_id": "<string>",
   "agent_id": "<uuid>",
   "mode": "silent|whisper",
   "reason": "<string ≥ 20 chars>",
   "monitor_session_id": "<uuid>"
 }

.. note::

 El payload NO incluye datos del cliente (caller): número de
 teléfono, nombre, ni contenido de la conversación.
 CNST-026 — sin PII innecesaria.

7.2 Entidades de lectura (no escritura)
========================================

User (supervisor)
-----------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Acceso**
   - Lectura — el ``supervisor_id`` se obtiene del JWT.
 * - **Campos usados**
   - ``id``, ``segment_id`` (para CNST-008),
     ``effective_functions`` (para verificar ``SUP-001``).

User (agente target)
---------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Acceso**
   - Lectura — el ``agent_id`` se obtiene de
     ``ActiveCallRepository.get(call_id).agent_id``.
 * - **Campos usados**
   - ``id``, ``segment_id`` (para validación CNST-008).

ActiveCall
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Acceso**
   - Lectura en PASO 6. No se escribe en este UC.
 * - **Campos usados**
   - ``call_id``, ``state`` (debe ser ``ACTIVE``),
     ``agent_id`` (para obtener el agente asociado).

7.3 Flujo de datos — request/response
=======================================

**Request (PASO 2):**

.. code-block:: json

 POST /api/supervisor/monitor/{call_id}/
 Authorization: Bearer <token>
 Content-Type: application/json

 {
   "mode": "silent",
   "reason": "Verificación de calidad — seguimiento semanal"
 }

**Response exitosa (PASO 12):**

.. code-block:: json

 HTTP 200 OK
 {
   "monitor_session_id": "550e8400-e29b-41d4-a716-446655440000",
   "mode": "silent",
   "call_id": "CALL-2026-001234",
   "started_at": "2026-05-02T14:30:00Z"
 }

**Response de error (ejemplo EX-06):**

.. code-block:: json

 HTTP 400 Bad Request
 {
   "error": "REASON_TOO_SHORT",
   "detail": "El campo reason debe tener al menos 20 caracteres",
   "actual_length": 8,
   "required_length": 20
 }

7.4 Restricciones de datos
============================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **mode**
   - Solo acepta ``"silent"`` o ``"whisper"``. Cualquier otro
     valor retorna 400 con ``{"error": "INVALID_MODE"}``.
 * - **reason**
   - String requerido. Mínimo 20 caracteres. Sin máximo definido
     en este UC (el campo en BD es TEXT).
 * - **call_id**
   - Path parameter. Validado como string no vacío. La existencia
     se verifica contra TelephonyClient en PASO 6.
 * - **monitor_session_id**
   - UUID v4 generado por el Backend. Opaco al cliente — no tiene
     significado de negocio más allá de identificar la sesión.
