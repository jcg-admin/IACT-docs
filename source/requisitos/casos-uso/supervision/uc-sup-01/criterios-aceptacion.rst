.. _uc-sup-01-parte-09:

==========================================
Parte 9 — Criterios de aceptación
==========================================

9.1 Criterios funcionales
==========================

CA-01 — Activar monitor en modo silent
----------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Un supervisor con sesión activa (JWT válido) que posee
     ``SUP-001 monitor_live_calls`` y existe una llamada
     ``ACTIVE`` con un agente en su segmento.
 * - **Cuando**
   - Envía ``POST /api/supervisor/monitor/{call_id}/``
     con ``{"mode": "silent", "reason": "Verificación de calidad estándar"}``.
 * - **Entonces**
   - Responde 200 OK con ``{monitor_session_id, mode="silent", call_id, started_at}``.
   - ``MonitorSession`` creada con ``state=ACTIVE``, ``mode=silent``.
   - Bridge de audio establecido en TelephonyClient (solo escucha).
   - Tono audible emitido al agente.
   - ``AuditEvent(CALL_MONITORED)`` creado con
     ``{call_id, agent_id, mode="silent", reason, monitor_session_id}``.

----

CA-02 — Activar monitor en modo whisper
-----------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Mismas condiciones que CA-01.
 * - **Cuando**
   - Envía con ``{"mode": "whisper", "reason": "Coaching en tiempo real al agente"}``.
 * - **Entonces**
   - Responde 200 OK con ``mode="whisper"``.
   - Bridge de audio bidireccional supervisor→agente (cliente no oye al supervisor).
   - Tono audible emitido al agente.
   - ``AuditEvent(CALL_MONITORED)`` con ``mode="whisper"``.

----

CA-03 — Switch de modo en vivo (FA-01)
----------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Sesión de monitoreo activa en modo ``silent``.
 * - **Cuando**
   - Supervisor envía ``PATCH /api/supervisor/monitor/{session_id}/``
     con ``{"mode": "whisper"}``.
 * - **Entonces**
   - Responde 200 OK con ``{"session_id", "mode": "whisper"}``.
   - ``MonitorSession.mode`` actualizado a ``whisper``.
   - TelephonyClient reconfigura el bridge sin interrumpir la llamada.
   - Tono audible re-emitido al agente.
   - ``AuditEvent(MONITOR_MODE_SWITCHED)`` creado.

----

CA-04 — Stop monitor explícito (FA-02)
----------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Sesión de monitoreo activa.
 * - **Cuando**
   - Supervisor envía ``DELETE /api/supervisor/monitor/{session_id}/``
     con ``{"reason": "Monitoreo finalizado según protocolo"}``.
 * - **Entonces**
   - Responde 200 OK con ``{"session_id", "state": "ENDED", "ended_at"}``.
   - ``MonitorSession.state = ENDED``, ``ended_at = NOW()``.
   - Bridge de audio desconectado. La llamada continúa sin el supervisor.
   - ``AuditEvent(MONITOR_ENDED)`` creado.

----

CA-05 — Tono audible obligatorio
----------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Cualquier activación de sesión de monitoreo (CA-01, CA-02, CA-03).
 * - **Cuando**
   - El flujo principal completa el PASO 9 (bridge establecido).
 * - **Entonces**
   - TelephonyClient SIEMPRE emite el tono audible al canal del agente.
   - El tono se emite ANTES de que el supervisor reciba el 200 OK.
   - Si el tono falla, la sesión NO se activa y se retorna EX-07.

----

CA-06 — Rechazo por segmento cruzado (EX-03)
----------------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Supervisor con segmento A intenta monitorear una llamada
     cuyo agente pertenece al segmento B.
 * - **Cuando**
   - Envía ``POST /api/supervisor/monitor/{call_id}/`` con datos válidos.
 * - **Entonces**
   - Responde 403 con ``{"error": "SEGMENT_VIOLATION"}``.
   - No se crea ``MonitorSession``.
   - No se activa bridge de audio.
   - ``AuditEvent(MONITOR_SEGMENT_BLOCKED)`` creado.

----

CA-07 — Rechazo por reason inválido (EX-06)
---------------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Supervisor con JWT válido y ``SUP-001`` sobre llamada activa en su segmento.
 * - **Cuando**
   - Envía con ``{"mode": "silent", "reason": "corto"}`` (5 chars).
 * - **Entonces**
   - Responde 400 con ``{"error": "REASON_TOO_SHORT", "actual_length": 5, "required_length": 20}``.
   - No se crea ``MonitorSession`` ni ``AuditEvent``.

----

CA-08 — AuditEvent CALL_MONITORED con datos completos
-------------------------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Flujo principal completado exitosamente (CA-01 o CA-02).
 * - **Cuando**
   - Se consulta la tabla ``audit_events`` por ``event_type=CALL_MONITORED``.
 * - **Entonces**
   - El registro contiene:
     ``actor_user_id`` = supervisor_id,
     ``payload.call_id``,
     ``payload.agent_id``,
     ``payload.mode``,
     ``payload.reason``,
     ``payload.monitor_session_id``.
   - ``occurred_at`` coincide con ``MonitorSession.started_at`` (misma transacción).
   - El registro no puede modificarse ni borrarse (inmutable — BR-010).

9.2 Criterios de rechazo — sin función RBAC
=============================================

CA-09 — Rechazo sin SUP-001
-----------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Usuario con JWT válido pero sin ``SUP-001 monitor_live_calls``
     (por ejemplo, solo posee ``AGR-011 call_center_operator_group``).
 * - **Cuando**
   - Envía ``POST /api/supervisor/monitor/{call_id}/``.
 * - **Entonces**
   - Responde 403 con ``{"error": "FUNCTION_MISSING",
     "detail": "Se requiere función SUP-001 monitor_live_calls"}``.
   - No se crea ningún registro en BD.

9.3 Criterios de auto-cierre
==============================

CA-10 — Auto-cierre por fin de llamada (FA-03)
------------------------------------------------

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Dado**
   - Sesión de monitoreo ``ACTIVE`` sobre llamada ``CALL-001``.
 * - **Cuando**
   - TelephonyClient emite evento ``CALL_ENDED`` para ``CALL-001``.
 * - **Entonces**
   - ``MonitorSession.state = AUTO_ENDED``, ``ended_at = NOW()``,
     ``end_reason = CALL_ENDED``.
   - ``AuditEvent(MONITOR_AUTO_ENDED)`` creado.
   - Frontend del supervisor recibe notificación WebSocket con
     ``{"type": "MONITOR_SESSION_AUTO_ENDED"}``.
   - La llamada misma NO se ve afectada (ya terminó).
