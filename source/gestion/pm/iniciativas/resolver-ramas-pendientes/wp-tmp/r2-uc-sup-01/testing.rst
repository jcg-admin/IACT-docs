.. _uc-sup-01-parte-12:

==========================================
Parte 12 — Testing
==========================================

12.1 Estrategia de testing
===========================

UC_SUP_01 es clasificado como **CRÍTICO** (impacto legal + compliance).
La cobertura mínima requerida es **100% de los criterios de aceptación**
más los casos de seguridad obligatorios.

.. list-table::
 :widths: 20 20 60
 :header-rows: 1

 * - Nivel
   - Cobertura requerida
   - Qué valida
 * - **Unit Tests (UT)**
   - 100% de validaciones
   - Validadores de ``reason``, ``mode``,
     guard clauses del handler.
 * - **Integration Tests (IT)**
   - 100% de CAs (CA-01..CA-10)
   - Flujo completo con BD real y
     TelephonyClient mockeado.
 * - **Security Tests (SEC)**
   - 100% de casos de seguridad
   - RBAC, segmento, ownership.
 * - **Compliance Tests (COMP)**
   - Obligatorio — tono audible
   - Verificación de emisión del tono
     en cada activación.

12.2 Unit Tests
================

UT-01 — Validador de reason
-----------------------------

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Caso
   - Resultado esperado
 * - ``reason = None``
   - ``ReasonTooShortError``
 * - ``reason = ""``
   - ``ReasonTooShortError``
 * - ``reason = "corto"`` (5 chars)
   - ``ReasonTooShortError`` con ``actual_length=5``
 * - ``reason = "exactamente veinte ch"`` (20 chars)
   - OK (pasa validación)
 * - ``reason = "Justificación de supervisión estándar"``
   - OK

----

UT-02 — Validador de mode
---------------------------

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Caso
   - Resultado esperado
 * - ``mode = "silent"``
   - OK
 * - ``mode = "whisper"``
   - OK
 * - ``mode = "barge"``
   - ``InvalidModeError``
 * - ``mode = ""``
   - ``InvalidModeError``
 * - ``mode = None``
   - ``InvalidModeError``

----

UT-03 — Guard clause: RBAC
----------------------------

Verificar que el decorador ``@require_function("SUP-001")``
retorna 403 cuando el usuario no tiene la función.

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Usuario
   - Resultado
 * - Con ``SUP-001`` directo
   - Pasa al siguiente middleware
 * - Con ``AGR-012`` (contiene SUP-001)
   - Pasa al siguiente middleware
 * - Solo con ``AGR-011`` (no contiene SUP-001)
   - 403 FUNCTION_MISSING

12.3 Integration Tests
=======================

IT-01 — Flujo silent exitoso (CA-01)
--------------------------------------

::

 GIVEN: supervisor con SUP-001, llamada ACTIVE en su segmento
 WHEN:  POST /api/supervisor/monitor/{call_id}/ {mode=silent, reason="Verificación de calidad estándar"}
 THEN:  status=200
        body.monitor_session_id es UUID válido
        body.mode == "silent"
        MonitorSession en BD con state=ACTIVE
        AuditEvent CALL_MONITORED con payload completo
        TelephonyClient.bridge_listen llamado 1 vez
        TelephonyClient.emit_tone llamado 1 vez con tone_type=MONITOR_ON

----

IT-02 — Flujo whisper exitoso (CA-02)
---------------------------------------

::

 GIVEN: mismas condiciones que IT-01
 WHEN:  POST con mode=whisper
 THEN:  status=200, body.mode == "whisper"
        TelephonyClient.bridge_listen(session_id, "whisper") llamado
        AuditEvent con payload.mode == "whisper"

----

IT-03 — Switch de modo (CA-03 / FA-01)
----------------------------------------

::

 GIVEN: sesión ACTIVE en modo silent
 WHEN:  PATCH /api/supervisor/monitor/session/{session_id}/ {mode=whisper}
 THEN:  status=200, body.mode == "whisper"
        MonitorSession.mode actualizado en BD
        TelephonyClient.switch_mode llamado
        TelephonyClient.emit_tone re-emitido
        AuditEvent MONITOR_MODE_SWITCHED creado

----

IT-04 — Stop explícito (CA-04 / FA-02)
-----------------------------------------

::

 GIVEN: sesión ACTIVE
 WHEN:  DELETE /api/supervisor/monitor/session/{session_id}/
 THEN:  status=200, body.state == "ENDED"
        MonitorSession.state=ENDED, ended_at=NOW()
        TelephonyClient.bridge_unlisten llamado
        AuditEvent MONITOR_ENDED creado

----

IT-05 — Auto-cierre por fin de llamada (CA-10 / FA-03)
---------------------------------------------------------

::

 GIVEN: sesión ACTIVE sobre CALL-001
 WHEN:  TelephonyClient emite evento CALL_ENDED para CALL-001
 THEN:  MonitorSession.state=AUTO_ENDED, end_reason=CALL_ENDED
        AuditEvent MONITOR_AUTO_ENDED creado
        WebSocket notificado al supervisor

----

IT-06 — Fallo de telefonía (EX-07)
-------------------------------------

::

 GIVEN: supervisor válido, llamada ACTIVE en segmento
        TelephonyClient.bridge_listen lanza TelephonyError
 WHEN:  POST monitor
 THEN:  status=503, error=TELEPHONY_UNAVAILABLE
        MonitorSession creada pero con state=FAILED
        AuditEvent MONITOR_FAILED creado
        body incluye monitor_session_id con state=FAILED

----

IT-07 — Idempotencia: segunda sesión sobre misma llamada
----------------------------------------------------------

::

 GIVEN: sesión ACTIVE sobre CALL-001
 WHEN:  POST /api/supervisor/monitor/CALL-001/ (segunda vez)
 THEN:  status=409 CONFLICT
        body incluye monitor_session_id de la sesión existente
        No se crea segunda MonitorSession

12.4 Security Tests
====================

SEC-01 — Tono audible obligatorio (CA-05)
-------------------------------------------

::

 GIVEN: cualquier activación de monitoreo
 THEN:  TelephonyClient.emit_tone SIEMPRE es llamado
        Si emit_tone falla → sesión NO se activa
        Verificar: imposible tener MonitorSession.state=ACTIVE
                   sin registro de emit_tone exitoso

----

SEC-02 — Rechazo sin SUP-001 (CA-09)
--------------------------------------

::

 GIVEN: usuario con solo AGR-011 (OPR-001..009, sin SUP-001)
 WHEN:  POST /api/supervisor/monitor/{call_id}/
 THEN:  status=403, error=FUNCTION_MISSING
        detail menciona "SUP-001 monitor_live_calls"
        No hay MonitorSession en BD

----

SEC-03 — Rechazo por segmento cruzado (CA-06)
-----------------------------------------------

::

 GIVEN: supervisor con segmento A, llamada de agente en segmento B
 WHEN:  POST monitor
 THEN:  status=403, error=SEGMENT_VIOLATION
        AuditEvent MONITOR_SEGMENT_BLOCKED creado
        No se crea MonitorSession

----

SEC-04 — Ownership de sesión (EX-08)
--------------------------------------

::

 GIVEN: supervisor B intenta PATCH/DELETE sobre sesión de supervisor A
 WHEN:  PATCH /api/supervisor/monitor/session/{session_id_A}/
 THEN:  status=403, error=SESSION_OWNERSHIP_VIOLATION
        AuditEvent MONITOR_OWNERSHIP_VIOLATION creado

12.5 Compliance Tests
======================

COMP-01 — AuditEvent inmutable
--------------------------------

::

 GIVEN: AuditEvent(CALL_MONITORED) creado durante IT-01
 WHEN:  Intento de UPDATE o DELETE en tabla audit_events
 THEN:  Operación rechazada por BD (constraint o trigger)
        El registro permanece intacto

----

COMP-02 — Transaccionalidad session + audit
---------------------------------------------

::

 GIVEN: MonitorSession e INSERT de AuditEvent en transacción
 WHEN:  Simular error después de INSERT MonitorSession y antes
        de INSERT AuditEvent (forzar rollback)
 THEN:  Ningún registro creado en ninguna tabla
        Estado consistente: ni MonitorSession ni AuditEvent existen

----

COMP-03 — Payload de AuditEvent sin PII del cliente
-----------------------------------------------------

::

 GIVEN: AuditEvent(CALL_MONITORED) creado con llamada real
 THEN:  payload NO contiene: número de teléfono del cliente,
        nombre del cliente, contenido de la conversación
        payload SÍ contiene: call_id, agent_id, supervisor_id,
        mode, reason, monitor_session_id

12.6 Matriz de cobertura
=========================

.. list-table::
 :widths: 15 35 15 15 20
 :header-rows: 1

 * - CA
   - Descripción
   - UT
   - IT
   - SEC/COMP
 * - CA-01
   - Monitor silent exitoso
   - UT-01, UT-02
   - IT-01
   - COMP-02, COMP-03
 * - CA-02
   - Monitor whisper exitoso
   - UT-01, UT-02
   - IT-02
   -
 * - CA-03
   - Switch de modo
   -
   - IT-03
   -
 * - CA-04
   - Stop explícito
   -
   - IT-04
   -
 * - CA-05
   - Tono audible obligatorio
   -
   -
   - SEC-01
 * - CA-06
   - Rechazo segmento cruzado
   -
   -
   - SEC-03
 * - CA-07
   - Rechazo reason corto
   - UT-01
   -
   -
 * - CA-08
   - AuditEvent completo
   -
   - IT-01
   - COMP-01, COMP-03
 * - CA-09
   - Rechazo sin SUP-001
   - UT-03
   -
   - SEC-02
 * - CA-10
   - Auto-cierre por llamada
   -
   - IT-05
   -

**Cobertura total: 100% de los 10 criterios de aceptación.**
