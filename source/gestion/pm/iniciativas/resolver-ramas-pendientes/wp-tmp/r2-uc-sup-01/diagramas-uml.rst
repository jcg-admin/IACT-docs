.. _uc-sup-01-parte-08:

==========================================
Parte 8 — Diagramas UML
==========================================

8.1 Diagrama de caso de uso
=============================

.. uml::
 :caption: UC_SUP_01 — Monitorear Llamada: actores y relaciones

 @startuml
 left to right direction

 actor "Supervisor\n(SUP-001 monitor_live_calls)" as SUP
 actor "Agente Target" as AGT
 actor "TelephonyClient\n(sistema externo)" as TEL

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada\n(Silent / Whisper)" as UC01
   usecase "Activar modo silent" as UC01A
   usecase "Activar modo whisper" as UC01B
   usecase "Switch de modo" as UC01C
   usecase "Stop monitor" as UC01D
   usecase "UC_SUP_02\nBarge-in" as UC02
 }

 SUP --> UC01
 SUP --> UC01C
 SUP --> UC01D

 UC01 ..> UC01A : <<include>>
 UC01 ..> UC01B : <<include>>
 UC01 ..> UC02 : <<extend>>\n[escalada]

 UC01 --> AGT : notificacion\ntono audible
 UC01 --> TEL : bridge_listen()

 note right of UC01
   Requiere: SUP-001 monitor_live_calls
   Restringe: segmento CNST-008
   Audita: CNST-025 (AuditEvent)
 end note
 @enduml

8.2 Diagrama de actividad — flujo principal
=============================================

.. uml::
 :caption: UC_SUP_01 — Actividad del flujo principal (camino feliz)

 @startuml
 start

 :Supervisor selecciona llamada\ndesde dashboard;

 :POST /api/supervisor/monitor/{call_id}/\n{mode, reason};

 fork
   :Validar JWT (CNST-009);
 fork again
   :Verificar SUP-001 monitor_live_calls;
 end fork

 if (JWT válido + SUP-001 presente?) then (no)
   if (JWT inválido?) then (sí)
     :401 TOKEN_INVALID;
   else (no)
     :403 FUNCTION_MISSING;
   endif
   stop
 endif

 :SegmentFilter: verificar segmento\ndel agente vs supervisor (CNST-008);

 if (Agente en segmento?) then (no)
   :403 SEGMENT_VIOLATION;
   :AuditEvent(MONITOR_SEGMENT_BLOCKED);
   stop
 endif

 :ActiveCallRepository.get(call_id);

 if (Llamada existe?) then (no)
   :404 CALL_NOT_FOUND;
   stop
 endif

 if (Estado == ACTIVE?) then (no)
   :400 CALL_NOT_ACTIVE;
   stop
 endif

 if (len(reason) >= 20?) then (no)
   :400 REASON_TOO_SHORT;
   stop
 endif

 :BEGIN TRANSACTION;
 :INSERT MonitorSession\n(state=ACTIVE, started_at=NOW());
 :INSERT AuditEvent\n(CALL_MONITORED);
 :COMMIT;

 :TelephonyClient.bridge_listen(session_id, mode);

 if (Bridge OK?) then (no)
   :UPDATE MonitorSession state=FAILED;
   :INSERT AuditEvent(MONITOR_FAILED);
   :503 TELEPHONY_UNAVAILABLE;
   stop
 endif

 :TelephonyClient: emitir tono\naudible al agente;

 :WebSocket → Frontend agente:\nbadge "siendo supervisado";

 :200 OK\n{monitor_session_id, mode, call_id, started_at};
 stop
 @enduml

8.3 Diagrama de secuencia — flujo principal
=============================================

.. uml::
 :caption: UC_SUP_01 — Secuencia detallada entre componentes

 @startuml
 actor "Supervisor" as SUP
 participant "Frontend\n(Web/App)" as FE
 participant "AuthGuard\n+ SegmentFilter" as AUTH
 participant "MonitorEndpoint\n(Backend)" as BE
 participant "ActiveCallRepo" as REPO
 database "Base de datos\n(PostgreSQL)" as BD
 participant "TelephonyClient" as TEL
 actor "Agente Target" as AGT

 SUP -> FE: Seleccionar llamada\n+ modo + reason
 FE -> BE: POST /api/supervisor/monitor/{call_id}/\nAuthorization: Bearer <token>

 BE -> AUTH: validar JWT
 AUTH --> BE: supervisor_id + funciones efectivas

 BE -> AUTH: verificar SUP-001 monitor_live_calls
 AUTH --> BE: OK (posee SUP-001)

 BE -> AUTH: SegmentFilter(supervisor.segment_id,\n call_id)
 AUTH --> BE: OK (agente en segmento)

 BE -> REPO: ActiveCallRepository.get(call_id)
 REPO --> BE: call{state=ACTIVE, agent_id}

 BE -> BE: validar len(reason) >= 20

 BD <-- BE: BEGIN TRANSACTION
 BE -> BD: INSERT MonitorSession\n(supervisor, call_id, agent_id,\nmode, reason, started_at=NOW())
 BD --> BE: monitor_session_id (UUID)

 BE -> BD: INSERT AuditEvent\n(CALL_MONITORED, actor=supervisor,\npayload={call_id, agent_id,\nmode, reason, monitor_session_id})
 BD --> BE: OK

 BE -> BD: COMMIT
 BD --> BE: OK

 BE -> TEL: bridge_listen(monitor_session_id, mode)
 TEL --> BE: bridge_established

 TEL -> AGT: tono audible "monitor on"

 BE -> FE: WebSocket: SUPERVISOR_MONITORING\n{mode, started_at}
 FE -> AGT: badge "siendo supervisado"

 BE --> FE: 200 OK\n{monitor_session_id, mode,\ncall_id, started_at}
 FE --> SUP: Interfaz de monitoreo activa
 @enduml

8.4 Diagrama de estados — MonitorSession
==========================================

.. uml::
 :caption: UC_SUP_01 — Estados de MonitorSession durante su ciclo de vida

 @startuml
 [*] --> ACTIVE : POST monitor\n(PASO 8 — INSERT)

 ACTIVE --> ACTIVE : FA-01 switch de modo\n(UPDATE mode)

 ACTIVE --> ENDED : FA-02 stop manual\n(supervisor DELETE)

 ACTIVE --> AUTO_ENDED : FA-03 llamada termina\n(CALL_ENDED event)

 ACTIVE --> FAILED : EX-07 bridge falla\n(TelephonyClient error)

 ENDED --> [*]
 AUTO_ENDED --> [*]
 FAILED --> [*] : puede reintentar\n(nueva sesión)

 note right of ACTIVE
   Bridge de audio activo.
   Tono emitido al agente.
   AuditEvent(CALL_MONITORED) existe.
 end note

 note right of FAILED
   Bridge NO activo.
   AuditEvent(MONITOR_FAILED) creado.
   MonitorSession existe en BD
   para trazabilidad.
 end note
 @enduml

8.5 Diagrama de clases — modelo de dominio
============================================

.. uml::
 :caption: UC_SUP_01 — Clases involucradas y sus relaciones

 @startuml
 class MonitorSession {
   + id : UUID
   + supervisor_id : FK(User)
   + call_id : String
   + agent_id : FK(User)
   + mode : Enum(silent, whisper)
   + reason : String
   + state : Enum(ACTIVE, ENDED, AUTO_ENDED, FAILED)
   + started_at : DateTime
   + ended_at : DateTime?
   + end_reason : String?
 }

 class AuditEvent {
   + id : UUID
   + event_type : String
   + actor_user_id : FK(User)
   + occurred_at : DateTime
   + payload : JSONB
 }

 class User {
   + id : UUID
   + segment_id : FK(Segment)
   + effective_functions : Set(String)
 }

 class ActiveCall {
   + call_id : String
   + agent_id : FK(User)
   + state : Enum(ACTIVE, HELD, ENDED)
 }

 class TelephonyClient <<external>> {
   + bridge_listen(session_id, mode)
   + bridge_unlisten(session_id)
   + switch_mode(session_id, mode)
   + emit_tone(agent_channel, tone_type)
 }

 MonitorSession "1" --> "1" User : supervisor
 MonitorSession "1" --> "1" User : agent target
 MonitorSession "1" --> "1" ActiveCall : monitored call
 MonitorSession "1" ..> "1" AuditEvent : genera >
 MonitorSession "1" ..> "1" TelephonyClient : establece bridge >

 note on link
   AuditEvent es inmutable.
   MonitorSession y AuditEvent
   se crean en la misma transacción.
 end note
 @enduml
