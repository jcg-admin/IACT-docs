.. _uc-sup-01-parte-02:

============================================
Parte 2 — Actores y precondiciones
============================================

2.1 Actores
===========

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Actor
   - Tipo
   - Rol en este UC
 * - **Supervisor**
   - Humano (iniciador)
   - Posee ``SUP-001 monitor_live_calls``. Selecciona la llamada
     a monitorear y elige el modo (silent/whisper).
 * - **Agente Target**
   - Humano (participante notificado)
   - Está en llamada activa. Recibe tono audible de notificación.
     En modo whisper puede escuchar al supervisor.
 * - **TelephonyClient**
   - Sistema externo
   - Componente de telefonía que gestiona los canales de audio.
     Crea el bridge tripartito supervisor–agente–cliente.
 * - **AuthGuard**
   - Sistema interno
   - Valida JWT + verifica que el invocante posee ``SUP-001``.
 * - **SegmentFilter**
   - Sistema interno
   - Valida que el agente target pertenece al segmento del
     supervisor (CNST-008).

2.2 Precondiciones
==================

.. list-table::
 :widths: 10 90
 :header-rows: 0

 * - P-01
   - El supervisor tiene sesión activa (JWT válido, CNST-009).
 * - P-02
   - El supervisor posee función ``SUP-001 monitor_live_calls``
     (via AGR-012 o asignación directa).
 * - P-03
   - Existe una llamada activa con el ``call_id`` especificado
     (estado ``ACTIVE`` en el sistema de telefonía).
 * - P-04
   - El agente de la llamada pertenece al segmento del supervisor
     (validación CNST-008 — solo puede monitorear a sus agentes).
 * - P-05
   - El ``reason`` tiene al menos 20 caracteres (justificación
     obligatoria para toda operación de supervisión).

2.3 Postcondiciones
===================

.. list-table::
 :widths: 10 90
 :header-rows: 0

 * - PC-01
   - Sesión de monitoreo activa (``MonitorSession.state = ACTIVE``).
 * - PC-02
   - Bridge de audio establecido en TelephonyClient.
 * - PC-03
   - Tono audible emitido al agente.
 * - PC-04
   - ``AuditEvent(CALL_MONITORED)`` creado con: supervisor_id,
     agent_id, call_id, mode, reason, started_at.
 * - PC-05
   - Response 200 con ``monitor_session_id`` al supervisor.

2.4 Endpoint
============

.. code-block:: text

 POST /api/supervisor/monitor/{call_id}/
 Authorization: Bearer <token>
 Content-Type: application/json

 {
   "mode": "silent" | "whisper",
   "reason": "string ≥ 20 caracteres"
 }
