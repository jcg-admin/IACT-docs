.. _uc-sup-01-parte-06:

==========================================
Parte 6 — Requisitos no funcionales
==========================================

6.1 Performance
===============

.. list-table::
 :widths: 20 25 55
 :header-rows: 1

 * - Atributo
   - Valor objetivo
   - Justificación
 * - **Latencia end-to-end**
   - ≤ 1 000 ms (p95)
   - Desde que el supervisor envía el POST hasta recibir
     200 OK con el bridge activo. El supervisor percibe
     el monitoreo como "inmediato".
 * - **Latencia bridge de audio**
   - ≤ 500 ms
   - ``TelephonyClient.bridge_listen()`` debe completarse
     en menos de 500 ms. Si supera 1 000 ms se considera
     timeout y se activa EX-07.
 * - **Concurrencia**
   - ≥ 50 sesiones activas simultáneas
   - Un supervisor puede tener solo 1 sesión activa a la
     vez. El sistema soporta ≥ 50 supervisores monitoreando
     en paralelo sin degradación.
 * - **Throughput switch de modo**
   - ≤ 200 ms
   - FA-01 (switch silent↔whisper) debe ser perceptible
     como instantáneo para el supervisor.

6.2 Compliance y legalidad
===========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Tono audible al agente (LFPDPPP)**
   - El sistema DEBE emitir un tono audible al agente al
     activar cualquier modo de monitoreo (silent o whisper).
     Esta notificación es requerida por la Ley Federal de
     Protección de Datos Personales en Posesión de los
     Particulares (LFPDPPP) y por la política interna.
     **No es configurable ni bypasseable.** Si el tono
     falla, la sesión de monitoreo NO se activa.
 * - **Notificación al cliente**
   - La normativa vigente NO requiere notificar al cliente
     (caller) sobre el monitoreo de supervisión interna.
     Esta exención aplica exclusivamente a los modos
     silent y whisper (supervisión interna de calidad).
     Si la regulación regional varía, la política debe
     revisarse por el equipo legal antes de desplegar.
 * - **Reason obligatorio**
   - Cada monitoreo debe tener una justificación de al
     menos 20 caracteres. Requisito de auditoría interna.
     El ``reason`` se almacena en ``MonitorSession`` y en
     ``AuditEvent`` — forma parte del registro permanente.
 * - **Auditoría inmutable (CNST-025)**
   - ``AuditEvent(CALL_MONITORED)`` se crea dentro de la
     misma transacción que ``MonitorSession``. El evento
     no puede borrarse ni modificarse (BR-010 — auditoría
     inmutable).
 * - **Sin PII innecesaria (CNST-026)**
   - El payload del ``AuditEvent`` incluye IDs de sistema
     (``supervisor_id``, ``agent_id``, ``call_id``) pero
     NO nombres, números de teléfono del cliente, ni
     contenido de la conversación.

6.3 Seguridad
=============

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Autenticación (CNST-009)**
   - JWT obligatorio en cada request. Sin excepción para
     ningún endpoint de supervisión.
 * - **Autorización (RBAC — CNST-029)**
   - La función ``SUP-001 monitor_live_calls`` es la única
     llave de acceso. No existe bypass por IP, horario,
     ni flag de configuración.
 * - **Segmentación de datos (CNST-008)**
   - Un supervisor solo puede monitorear agentes de su
     segmento. La validación ocurre en cada request, no
     solo al asignar la función.
 * - **Propiedad de sesión**
   - Un supervisor solo puede operar (switch/stop) sobre
     sus propias sesiones. No existe función de
     "administrar sesiones de otros supervisores" en este UC.
 * - **Transmisión segura**
   - El audio del bridge se transmite sobre canal TLS/SRTP.
     El backend nunca procesa ni almacena el audio de la
     llamada (CNST-026).

6.4 Disponibilidad y resiliencia
==================================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **SLA del endpoint**
   - 99.9% uptime durante horario operacional del call center.
 * - **Timeout de telefonía**
   - Si ``TelephonyClient`` no responde en 1 000 ms, se
     ejecuta la compensación (EX-07): la sesión se marca
     ``FAILED`` y el bridge no se activa.
 * - **Reconexión automática**
   - Si el bridge de audio se cae por error de red después
     de estar activo (post-PASO 9), TelephonyClient
     reintenta hasta 3 veces con backoff exponencial antes
     de emitir ``MONITOR_BRIDGE_LOST`` al supervisor.
 * - **Idempotencia de activación**
   - Si el supervisor envía el POST dos veces con el mismo
     ``call_id``, el segundo request retorna 409 CONFLICT
     con el ``monitor_session_id`` de la sesión ya activa.
     No se crean sesiones duplicadas.

6.5 Mantenibilidad
==================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Logging estructurado**
   - Todos los eventos del flujo se registran con
     correlation ID para trazabilidad end-to-end.
     Formato JSON, nivel ``INFO`` en flujo nominal,
     ``WARN`` en excepciones de seguridad, ``ERROR``
     en fallos de telefonía.
 * - **Observabilidad**
   - Métricas expuestas: ``monitor_sessions_started``,
     ``monitor_sessions_failed``, ``bridge_latency_ms``,
     ``monitor_mode_switches``. Compatible con Prometheus.
 * - **Manejo de errores (CNST-013)**
   - Toda excepción incluye: código de error estandarizado,
     HTTP status correcto, mensaje legible para el cliente,
     correlation ID para soporte.
