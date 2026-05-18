.. _uc-sup-01-parte-03:

==========================================
Parte 3 — Flujo principal (Camino feliz)
==========================================

3.1 Resumen del flujo
=====================

::

   PASO 1   Supervisor selecciona llamada a monitorear    (Frontend)
   PASO 2   POST /api/supervisor/monitor/{call_id}/       (FE → BE)
   PASO 3   Validar JWT (CNST-009)                        (AuthGuard)
   PASO 4   Verificar SUP-001 monitor_live_calls          (AuthGuard)
   PASO 5   Validar segmento (P-04, CNST-008)             (SegmentFilter)
   PASO 6   Validar llamada activa (call_id, estado)      (Backend → Telephony)
   PASO 7   Validar reason ≥ 20 chars                     (Backend)
   PASO 8   Crear MonitorSession (INSERT)                  (Backend → BD)
   PASO 9   Establecer bridge de audio (TelephonyClient)   (Backend → Telephony)
   PASO 10  Emitir tono audible al agente                  (Telephony → Agente)
   PASO 11  Emitir AuditEvent(CALL_MONITORED)              (Backend → BD)
   PASO 12  200 OK con monitor_session_id                  (BE → FE)

3.2 Detalle paso a paso
=======================

PASO 2 — Request
-----------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Método**
   - POST
 * - **Path**
   - ``/api/supervisor/monitor/{call_id}/``
 * - **Headers**
   - ``Authorization: Bearer <token>``
 * - **Body**
   - ``{"mode": "silent"|"whisper", "reason": "<min 20 chars>"}``

PASO 3-4 — Validacion auth + RBAC
-----------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - Middleware valida JWT (CNST-009). AuthorizationGuard verifica
     que el invocante posee función ``SUP-001 monitor_live_calls``
     en su conjunto efectivo de funciones (asignación directa o
     via AGR-012).
 * - **Errores**
   - EX-01 (401 UNAUTHORIZED — token inválido),
     EX-02 (403 FORBIDDEN — no posee SUP-001).

PASO 5 — Validar segmento
--------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - SegmentFilter verifica que el agente de la llamada
     ``call_id`` pertenece al segmento del supervisor
     (CNST-008 — data segmentation). No puede monitorear
     llamadas de agentes fuera de su área.
 * - **Errores**
   - EX-03 (403 SEGMENT_VIOLATION — agente fuera de segmento).

PASO 6 — Validar llamada activa
---------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - ``ActiveCallRepository.get(call_id)`` — verifica existencia
     y estado ``ACTIVE`` en el sistema de telefonía.
 * - **Errores**
   - EX-04 (404 CALL_NOT_FOUND),
     EX-05 (400 CALL_NOT_ACTIVE — llamada ya terminó).

PASO 7 — Validar reason
------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - Verificar ``len(reason) >= 20``. La justificación es
     obligatoria para operaciones de supervisión (política
     de compliance interno).
 * - **Errores**
   - EX-06 (400 REASON_TOO_SHORT).

PASO 8 — Crear MonitorSession
-------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - ``MonitorSession.objects.create(supervisor=invoker,
     call_id=call_id, mode=mode, reason=reason,
     started_at=NOW(), state='ACTIVE')``
 * - **Clase**
   - ``MonitorSession`` (escritura — INSERT)

PASO 9 — Bridge de audio
--------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - ``TelephonyClient.bridge_listen(session_id, mode)``
     Modo ``silent``: supervisor recibe audio del canal
     agent↔client (unidireccional). Modo ``whisper``:
     supervisor envía audio solo al canal del agente
     (supervisor→agente; cliente no oye).
 * - **Errores**
   - EX-07 (503 TELEPHONY_UNAVAILABLE — servicio de telefonía
     no responde).

PASO 10 — Tono de notificacion
--------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - TelephonyClient emite tono audible de "monitor on" al
     canal del agente. Este paso es **obligatorio por
     compliance** y no es bypasseable.
 * - **Justificacion**
   - LFPDPPP y política interna requieren que el agente sepa
     que está siendo supervisado.

PASO 11 — AuditEvent
----------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Accion**
   - ``AuditEvent.objects.create(event_type='CALL_MONITORED',
     actor_user_id=invoker.id, occurred_at=NOW(),
     payload={call_id, agent_id, mode, reason,
     monitor_session_id})``
 * - **CNST**
   - CNST-025 auditoría inmutable; CNST-026 sin PII innecesaria.

PASO 12 — Response 200
-----------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Body**
   - ``{"monitor_session_id": "<uuid>", "mode": "silent",
     "call_id": "<id>", "started_at": "<iso8601>"}``

3.3 Atomicidad
==============

PASOS 8 y 11 dentro de transacción:

::

   BEGIN
     INSERT INTO monitor_sessions (...);
     INSERT INTO audit_events (event_type='CALL_MONITORED', ...);
   COMMIT

   -- PASO 9-10 post-COMMIT: bridge de audio
   -- (la sesión ya existe en BD antes de activar telefonía)
   TelephonyClient.bridge_listen(session_id, mode)

Si la transacción falla, el bridge de audio NO se activa.
Si el bridge falla, se revierte el estado de MonitorSession
a ``FAILED`` y se crea ``AuditEvent(MONITOR_FAILED)``.
