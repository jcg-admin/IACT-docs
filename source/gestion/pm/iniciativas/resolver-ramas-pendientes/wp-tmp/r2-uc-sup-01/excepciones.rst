.. _uc-sup-01-parte-05:

==========================================
Parte 5 — Excepciones y errores
==========================================

5.1 Tabla de excepciones
=========================

.. list-table::
 :widths: 10 20 15 55
 :header-rows: 1

 * - ID
   - Nombre
   - HTTP
   - Descripción
 * - EX-01
   - TOKEN_INVALID
   - 401
   - JWT ausente, expirado o malformado.
 * - EX-02
   - FUNCTION_MISSING
   - 403
   - El invocante no posee la función
     ``SUP-001 monitor_live_calls``.
 * - EX-03
   - SEGMENT_VIOLATION
   - 403
   - El agente de la llamada no pertenece
     al segmento del supervisor.
 * - EX-04
   - CALL_NOT_FOUND
   - 404
   - No existe llamada con el ``call_id``
     proporcionado.
 * - EX-05
   - CALL_NOT_ACTIVE
   - 400
   - La llamada existe pero su estado no
     es ``ACTIVE`` (ya terminó o está en pausa).
 * - EX-06
   - REASON_TOO_SHORT
   - 400
   - El campo ``reason`` tiene menos de
     20 caracteres.
 * - EX-07
   - TELEPHONY_UNAVAILABLE
   - 503
   - El servicio de telefonía no responde
     al intento de establecer el bridge.
 * - EX-08
   - SESSION_OWNERSHIP_VIOLATION
   - 403
   - El supervisor intenta operar sobre
     una sesión que no le pertenece (FA-01/FA-02).

5.2 Detalle de excepciones
===========================

EX-01 — TOKEN_INVALID
-----------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - CNST-009 — Autenticación JWT.
 * - **Cuándo ocurre**
   - El header ``Authorization: Bearer <token>`` está ausente,
     el token expiró, la firma no es válida, o el ``sub``
     no corresponde a ningún usuario activo.
 * - **Response body**
   - ``{"error": "TOKEN_INVALID", "detail": "JWT inválido o expirado"}``
 * - **Logging**
   - ``WARN`` — incluye IP de origen, User-Agent, timestamp.
     No incluye el token en el log (dato sensible).
 * - **Acción del cliente**
   - Renovar sesión vía ``POST /api/auth/refresh/`` y reintentar.

----

EX-02 — FUNCTION_MISSING
--------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - RBAC — función ``SUP-001 monitor_live_calls`` no asignada.
 * - **Cuándo ocurre**
   - El usuario tiene JWT válido pero no posee
     ``SUP-001 monitor_live_calls`` ni directamente ni
     vía ``AGR-012 call_center_supervisor_group``.
 * - **Response body**
   - ``{"error": "FUNCTION_MISSING",
     "detail": "Se requiere función SUP-001 monitor_live_calls"}``
 * - **Logging**
   - ``WARN`` — incluye ``user_id``, función requerida,
     funciones efectivas del usuario.
 * - **Acción del cliente**
   - Contactar al administrador de permisos para obtener
     la función ``SUP-001`` o el grupo ``AGR-012``.

----

EX-03 — SEGMENT_VIOLATION
---------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - CNST-008 — Data segmentation. SegmentFilter.
 * - **Cuándo ocurre**
   - El agente de la llamada ``call_id`` pertenece a un
     segmento distinto al del supervisor invocante.
 * - **Response body**
   - ``{"error": "SEGMENT_VIOLATION",
     "detail": "Llamada fuera de segmento supervisable"}``
 * - **Nota de privacidad**
   - El mensaje NO revela a qué segmento pertenece el agente
     ni el ID del agente (CNST-026 — sin PII innecesaria).
 * - **Logging**
   - ``WARN`` — incluye ``supervisor_id``, ``call_id``,
     segmento del supervisor, segmento del agente.
     Este log es de auditoría (CNST-025).

----

EX-04 — CALL_NOT_FOUND
------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - ``ActiveCallRepository.get(call_id)`` retorna nulo.
 * - **Cuándo ocurre**
   - El ``call_id`` no existe en el sistema de telefonía activo.
     Puede ocurrir si la llamada ya cerró y fue archivada,
     o si el ID es incorrecto.
 * - **Response body**
   - ``{"error": "CALL_NOT_FOUND",
     "detail": "No existe llamada activa con ese ID"}``
 * - **Acción del cliente**
   - Verificar el ``call_id`` en el dashboard de llamadas activas.

----

EX-05 — CALL_NOT_ACTIVE
-------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - ``ActiveCallRepository.get(call_id).state != 'ACTIVE'``.
 * - **Cuándo ocurre**
   - La llamada existe pero su estado es ``HELD``, ``ENDED``,
     ``FAILED``, o cualquier estado distinto a ``ACTIVE``.
     Race condition típica: la llamada terminó entre que el
     supervisor la seleccionó y envió el request.
 * - **Response body**
   - ``{"error": "CALL_NOT_ACTIVE",
     "detail": "La llamada no está activa",
     "call_state": "<estado_actual>"}``
 * - **Atomicidad**
   - No se crea ``MonitorSession`` ni se emite ``AuditEvent``
     si la llamada no está activa.

----

EX-06 — REASON_TOO_SHORT
--------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - Validación de ``len(reason) >= 20``.
 * - **Cuándo ocurre**
   - El campo ``reason`` del body está ausente, es ``null``,
     es string vacío, o tiene menos de 20 caracteres.
 * - **Response body**
   - ``{"error": "REASON_TOO_SHORT",
     "detail": "El campo reason debe tener al menos 20 caracteres",
     "actual_length": <n>,
     "required_length": 20}``
 * - **Justificación del requisito**
   - El ``reason`` es obligatorio por política de compliance
     interno. Una justificación menor a 20 caracteres no provee
     contexto suficiente para auditoría.

----

EX-07 — TELEPHONY_UNAVAILABLE
-------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - ``TelephonyClient.bridge_listen()`` lanza excepción o
     retorna error después de agotar reintentos.
 * - **Cuándo ocurre**
   - El servicio de telefonía no responde dentro del timeout
     configurado (recomendado: 5 s con 2 reintentos).
 * - **Compensación**
   - La transacción de BD (PASOS 8+11) ya se committeó antes
     de invocar el bridge. Al recibir error de telefonía:

     .. code-block:: sql

        UPDATE monitor_sessions SET state = 'FAILED' WHERE id = session_id;
        INSERT INTO audit_events (event_type, payload)
          VALUES ('MONITOR_FAILED',
                  '{session_id, error_code=TELEPHONY_UNAVAILABLE}');

 * - **Response body**
   - ``{"error": "TELEPHONY_UNAVAILABLE",
     "detail": "El servicio de telefonía no está disponible",
     "monitor_session_id": "<uuid>",
     "session_state": "FAILED"}``
 * - **Retry**
   - El supervisor puede reintentar el monitoreo. La sesión
     ``FAILED`` queda en BD para auditoría pero no bloquea
     la creación de una nueva sesión sobre la misma llamada.

----

EX-08 — SESSION_OWNERSHIP_VIOLATION
--------------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Origen**
   - PATCH o DELETE sobre ``session_id`` cuyo ``supervisor_id``
     no coincide con el invocante autenticado.
 * - **Cuándo ocurre**
   - Solo aplica a FA-01 (switch de modo) y FA-02 (stop).
     En el flujo principal no se puede dar porque el
     ``session_id`` aún no existe al iniciar.
 * - **Response body**
   - ``{"error": "SESSION_OWNERSHIP_VIOLATION",
     "detail": "Esta sesión de monitoreo no pertenece al invocante"}``
 * - **Logging**
   - ``WARN`` de seguridad — posible acceso cruzado entre
     supervisores.

5.3 Registro de excepciones en auditoría
==========================================

Las excepciones EX-03, EX-07 y EX-08 generan entradas en la
tabla ``audit_events`` aunque el flujo principal no se complete:

.. list-table::
 :widths: 20 30 50
 :header-rows: 1

 * - Excepción
   - event_type
   - Payload mínimo
 * - EX-03
   - ``MONITOR_SEGMENT_BLOCKED``
   - supervisor_id, call_id, segmento_supervisor
 * - EX-07
   - ``MONITOR_FAILED``
   - session_id, error_code, occurred_at
 * - EX-08
   - ``MONITOR_OWNERSHIP_VIOLATION``
   - invoker_id, session_id, owner_id

Las excepciones EX-01, EX-02, EX-04, EX-05, EX-06 no generan
``AuditEvent`` — son rechazos de input que no llegan a la capa
de negocio. Se registran en logs de aplicación (nivel ``WARN``).
