.. _uc-sup-01-parte-04:

==========================================
Parte 4 — Flujos alternos
==========================================

4.1 Resumen de flujos alternos
===============================

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Nombre
   - Descripción corta
 * - FA-01
   - Switch de modo en vivo
   - Supervisor cambia de ``silent`` a ``whisper`` (o viceversa)
     sin terminar la sesión de monitoreo activa.
 * - FA-02
   - Stop monitor — cierre explícito
   - Supervisor termina voluntariamente la sesión de monitoreo
     antes de que la llamada concluya.
 * - FA-03
   - Llamada termina durante monitor
   - La llamada monitoreada finaliza (por el agente o el cliente)
     mientras la sesión de monitoreo está activa.
 * - FA-04
   - Notificación UI al agente
   - El agente recibe un badge/indicador visual en su interfaz
     confirmando que está siendo monitoreado.

4.2 Detalle de flujos alternos
================================

FA-01 — Switch de modo en vivo
--------------------------------

**Punto de inserción:** Post-PASO 9 (bridge activo).

**Trigger:** Supervisor invoca ``PATCH /api/supervisor/monitor/session/{session_id}/``
con ``{"mode": "whisper"}`` (o ``"silent"``).

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Precondición**
   - ``MonitorSession.state = ACTIVE``. El supervisor posee
     la misma sesión activa que inició.
 * - **Paso FA-01-1**
   - AuthGuard verifica JWT + ``SUP-001 monitor_live_calls``
     (igual que el flujo principal).
 * - **Paso FA-01-2**
   - Verificar que ``session_id`` pertenece al invocante
     (no puede cambiar sesión de otro supervisor).
 * - **Paso FA-01-3**
   - ``TelephonyClient.switch_mode(session_id, new_mode)`` —
     reconfigura el bridge de audio sin interrumpir la llamada.
 * - **Paso FA-01-4**
   - ``MonitorSession.objects.filter(id=session_id).update(mode=new_mode)``.
 * - **Paso FA-01-5**
   - ``AuditEvent.objects.create(event_type='MONITOR_MODE_SWITCHED',
     payload={session_id, old_mode, new_mode, switched_at})``.
 * - **Paso FA-01-6**
   - Response ``200 OK`` con ``{"session_id", "mode": new_mode}``.
 * - **Errores**
   - EX-02 si no posee ``SUP-001``; EX-08 si ``session_id``
     no pertenece al invocante (403 SESSION_OWNERSHIP_VIOLATION);
     EX-07 si el switch de telefonía falla (503).

**Restricción de compliance:** El tono audible al agente se
re-emite con cada switch de modo. Esta emisión NO es omitible.

----

FA-02 — Stop monitor — cierre explícito
-----------------------------------------

**Punto de inserción:** Cualquier momento post-PASO 9.

**Trigger:** Supervisor invoca
``DELETE /api/supervisor/monitor/session/{session_id}/``
con body ``{"reason": "<min 20 chars>"}`` (justificación de cierre).

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Precondición**
   - ``MonitorSession.state = ACTIVE``. El bridge de audio está
     establecido en TelephonyClient.
 * - **Paso FA-02-1**
   - AuthGuard verifica JWT + ``SUP-001 monitor_live_calls``.
 * - **Paso FA-02-2**
   - ``TelephonyClient.bridge_unlisten(session_id)`` — desconecta
     el supervisor del canal de audio. La llamada entre agente
     y cliente continúa sin interrupción.
 * - **Paso FA-02-3**
   - Dentro de transacción:

     .. code-block:: sql

        BEGIN
          UPDATE monitor_sessions
            SET state = 'ENDED', ended_at = NOW()
            WHERE id = session_id;
          INSERT INTO audit_events
            (event_type, actor_user_id, payload, occurred_at)
            VALUES ('MONITOR_ENDED', supervisor_id,
                    '{session_id, ended_at, end_reason}', NOW());
        COMMIT

 * - **Paso FA-02-4**
   - Response ``200 OK`` con ``{"session_id", "state": "ENDED",
     "ended_at": "<iso8601>"}``.
 * - **Errores**
   - EX-07 si ``bridge_unlisten`` falla; en ese caso el estado
     de la sesión se marca ``FAILED`` y se crea
     ``AuditEvent(MONITOR_STOP_FAILED)``.

----

FA-03 — Llamada termina durante monitor
-----------------------------------------

**Punto de inserción:** Cualquier momento post-PASO 9.

**Trigger:** TelephonyClient emite evento ``CALL_ENDED``
(WebSocket o callback) al Backend mientras ``MonitorSession.state = ACTIVE``.

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Precondición**
   - La llamada ``call_id`` termina por cualquier razón (agente
     cuelga, cliente cuelga, timeout, error de red).
 * - **Paso FA-03-1**
   - El Backend recibe el evento ``CALL_ENDED`` de TelephonyClient.
 * - **Paso FA-03-2**
   - ``ActiveCallRepository.mark_ended(call_id)`` — el estado
     de la llamada pasa a ``ENDED`` en el sistema de telefonía.
 * - **Paso FA-03-3**
   - Backend consulta ``MonitorSession.objects.filter(call_id=call_id,
     state='ACTIVE')`` — obtiene todas las sesiones activas sobre
     esa llamada (puede haber más de una si se permitió).
 * - **Paso FA-03-4**
   - Por cada sesión activa, dentro de transacción:

     .. code-block:: sql

        BEGIN
          UPDATE monitor_sessions
            SET state = 'AUTO_ENDED',
                ended_at = NOW(),
                end_reason = 'CALL_ENDED'
            WHERE id = session_id;
          INSERT INTO audit_events (event_type, payload)
            VALUES ('MONITOR_AUTO_ENDED',
                    '{session_id, call_id, ended_at,
                      end_reason=CALL_ENDED}');
        COMMIT

 * - **Paso FA-03-5**
   - Frontend del supervisor recibe notificación vía WebSocket:
     ``{"type": "MONITOR_SESSION_AUTO_ENDED", "session_id": ...,
     "reason": "CALL_ENDED"}``. El badge de monitoreo desaparece.
 * - **Postcondiciones**
   - ``MonitorSession.state = AUTO_ENDED``. Bridge de audio ya
     no existe (la llamada terminó). Audit trail completo.

----

FA-04 — Notificación UI al agente (badge)
-------------------------------------------

**Punto de inserción:** Post-PASO 10 (tono audible emitido).

**Descripción:** Además del tono audible (PASO 10, obligatorio por
compliance), el sistema envía una notificación visual al agente en
su interfaz.

.. list-table::
 :widths: 20 80
 :header-rows: 0

 * - **Trigger**
   - Backend emite evento WebSocket a la sesión del agente
     identificado por ``agent_id`` de la llamada activa.
 * - **Payload**
   - ``{"type": "SUPERVISOR_MONITORING", "mode": "silent"|"whisper",
     "started_at": "<iso8601>"}``. Sin revelar el ID del supervisor
     (privacidad del supervisado).
 * - **Estado UI**
   - El agente ve un indicador visual persistente mientras dure
     la sesión. Se actualiza al hacer FA-01 (switch de modo).
     Desaparece al FA-02 (stop) o FA-03 (llamada termina).
 * - **Modo whisper**
   - En modo ``whisper``, el badge indica adicionalmente que el
     supervisor puede hablarle. El agente puede ver el canal
     activo de whisper en su UI.
 * - **Fallo de entrega**
   - Si el WebSocket al agente no está disponible, el tono audible
     ya fue emitido (PASO 10) y es suficiente para el requisito
     de compliance. El badge es adicional, no obligatorio
     por la misma norma.
