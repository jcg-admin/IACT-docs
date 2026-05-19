.. _uc-sup-01-parte-11:

==========================================
Parte 11 — Implementación técnica
==========================================

11.1 Componentes involucrados
==============================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Responsabilidad en UC_SUP_01
 * - ``MonitorEndpoint``
   - Handler del endpoint
     ``POST /api/supervisor/monitor/{call_id}/``.
     Orquesta el flujo de los PASOS 2-12.
 * - ``AuthGuard``
   - Middleware: valida JWT (CNST-009) y verifica que
     el usuario posee ``SUP-001 monitor_live_calls``.
 * - ``SegmentFilter``
   - Middleware: verifica CNST-008 — el agente de la
     llamada pertenece al segmento del supervisor.
 * - ``ActiveCallRepository``
   - Abstracción de lectura sobre el estado de llamadas
     activas en TelephonyClient (PASO 6).
 * - ``MonitorSessionRepository``
   - Escritura de ``MonitorSession`` en BD (PASO 8).
     Incluye la consulta de sesiones activas para FA-03.
 * - ``AuditService``
   - Escritura de ``AuditEvent`` en BD (PASO 11).
     Siempre dentro de la misma transacción que
     ``MonitorSessionRepository``.
 * - ``TelephonyClient``
   - Cliente del sistema externo de telefonía.
     Métodos: ``bridge_listen``, ``bridge_unlisten``,
     ``switch_mode``, ``emit_tone`` (PASOS 9-10).
 * - ``WebSocketNotifier``
   - Envío de notificaciones en tiempo real al agente
     (FA-04) y al supervisor (FA-03 auto-cierre).

11.2 Pseudocódigo del handler principal
=========================================

.. code-block:: python

 @require_function("SUP-001")
 @apply_segment_filter
 def monitor_call(request, call_id: str):
     mode = validate_mode(request.data["mode"])
     reason = validate_reason(request.data["reason"])  # >= 20 chars

     call = ActiveCallRepository.get(call_id)
     if call is None:
         raise CallNotFoundError(call_id)
     if call.state != "ACTIVE":
         raise CallNotActiveError(call_id, call.state)

     with transaction.atomic():
         session = MonitorSessionRepository.create(
             supervisor=request.user,
             call_id=call_id,
             agent_id=call.agent_id,
             mode=mode,
             reason=reason,
             started_at=now(),
         )
         AuditService.log(
             event_type="CALL_MONITORED",
             actor=request.user,
             payload={
                 "call_id": call_id,
                 "agent_id": str(call.agent_id),
                 "mode": mode,
                 "reason": reason,
                 "monitor_session_id": str(session.id),
             },
         )

     try:
         TelephonyClient.emit_tone(call.agent_channel, "MONITOR_ON")
         TelephonyClient.bridge_listen(session.id, mode)
     except TelephonyError:
         with transaction.atomic():
             session.state = "FAILED"
             session.save()
             AuditService.log(
                 event_type="MONITOR_FAILED",
                 actor=request.user,
                 payload={"session_id": str(session.id),
                          "error_code": "TELEPHONY_UNAVAILABLE"},
             )
         raise TelephonyUnavailableError()

     WebSocketNotifier.notify_agent(
         call.agent_id,
         {"type": "SUPERVISOR_MONITORING", "mode": mode, "started_at": session.started_at},
     )

     return Response({
         "monitor_session_id": str(session.id),
         "mode": mode,
         "call_id": call_id,
         "started_at": session.started_at.isoformat(),
     }, status=200)

11.3 Modelo Django — MonitorSession
=====================================

.. code-block:: python

 class MonitorSession(models.Model):
     class Mode(models.TextChoices):
         SILENT = "silent", "Silent"
         WHISPER = "whisper", "Whisper"

     class State(models.TextChoices):
         ACTIVE = "ACTIVE", "Active"
         ENDED = "ENDED", "Ended"
         AUTO_ENDED = "AUTO_ENDED", "Auto Ended"
         FAILED = "FAILED", "Failed"

     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     supervisor = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.PROTECT,
         related_name="supervised_sessions",
     )
     call_id = models.CharField(max_length=255, db_index=True)
     agent = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.PROTECT,
         related_name="monitored_sessions",
     )
     mode = models.CharField(max_length=10, choices=Mode.choices)
     reason = models.TextField()
     state = models.CharField(max_length=20, choices=State.choices, default=State.ACTIVE)
     started_at = models.DateTimeField()
     ended_at = models.DateTimeField(null=True, blank=True)
     end_reason = models.CharField(max_length=50, null=True, blank=True)

     class Meta:
         db_table = "monitor_sessions"
         indexes = [
             models.Index(fields=["call_id", "state"]),
             models.Index(fields=["supervisor", "state"]),
         ]

11.4 Endpoint — URL config
===========================

.. code-block:: python

 urlpatterns = [
     path(
         "supervisor/monitor/<str:call_id>/",
         MonitorEndpoint.as_view(),
         name="supervisor-monitor-call",
     ),
     path(
         "supervisor/monitor/session/<uuid:session_id>/",
         MonitorSessionEndpoint.as_view(),
         name="supervisor-monitor-session",
     ),
 ]

11.5 Integración con TelephonyClient
======================================

``TelephonyClient`` es un cliente HTTP/WebSocket del sistema de
telefonía externo. Su interfaz en este UC:

.. code-block:: python

 class TelephonyClient:

     def bridge_listen(self, session_id: UUID, mode: str) -> None:
         """
         Establece el bridge de audio.
         mode='silent': supervisor recibe audio agent<->client.
         mode='whisper': supervisor puede enviar audio solo al agente.
         Lanza TelephonyError si no responde en timeout.
         """

     def bridge_unlisten(self, session_id: UUID) -> None:
         """
         Desconecta el bridge. La llamada continúa sin el supervisor.
         """

     def switch_mode(self, session_id: UUID, new_mode: str) -> None:
         """
         Reconfigura el bridge sin interrumpir la llamada.
         """

     def emit_tone(self, agent_channel: str, tone_type: str) -> None:
         """
         Emite tono audible al canal del agente.
         tone_type='MONITOR_ON': compliance LFPDPPP.
         """

11.6 Manejo de errores — CNST-013
===================================

Todas las excepciones del UC mapean a respuestas HTTP estandarizadas:

.. code-block:: python

 EXCEPTION_MAP = {
     TokenInvalidError:          (401, "TOKEN_INVALID"),
     FunctionMissingError:       (403, "FUNCTION_MISSING"),
     SegmentViolationError:      (403, "SEGMENT_VIOLATION"),
     CallNotFoundError:          (404, "CALL_NOT_FOUND"),
     CallNotActiveError:         (400, "CALL_NOT_ACTIVE"),
     ReasonTooShortError:        (400, "REASON_TOO_SHORT"),
     TelephonyUnavailableError:  (503, "TELEPHONY_UNAVAILABLE"),
     SessionOwnershipError:      (403, "SESSION_OWNERSHIP_VIOLATION"),
 }

El middleware de error incluye ``correlation_id`` en cada response
para trazabilidad en soporte.
