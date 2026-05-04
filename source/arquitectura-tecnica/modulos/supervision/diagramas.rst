.. _arq-mod-010-diagramas:

================================================
ARQ_MOD_010 — Diagramas de Comportamiento
================================================


Flujo de Monitoreo en Tiempo Real
====================================

.. uml::
 :caption: Secuencia UC_SUP_01 — monitor_live_calls en modo silent/whisper con tono de supervision.

 @startuml

 actor "monitor_live_calls" as monitor_live_calls
 participant "SupervisionEndpoint\n(/api/v1/supervision/)" as Supervisionendpoint
 participant "TelephonyBridge\n(SIP/WebRTC)" as Telephonybridge
 participant "AuditLog" as Auditlog
 actor "answer_inbound_calls" as answer_inbound_calls

 monitor_live_calls -> Supervisionendpoint : POST /supervision/monitor {call_id, mode}
 Supervisionendpoint -> Supervisionendpoint : JWT + RBAC (monitor_live_calls)
 Supervisionendpoint -> Telephonybridge : conectar canal supervision\n(mode: silent|whisper)
 Telephonybridge -> answer_inbound_calls : emitir tono de supervision\n(compliance obligatorio)
 Telephonybridge --> Supervisionendpoint : canal activo
 Supervisionendpoint -> Auditlog : INSERT SupervisionEvent {tipo, supervisor, call_id}
 Supervisionendpoint --> monitor_live_calls : 200 OK

 note over monitor_live_calls, answer_inbound_calls
   En modo silent: supervisor escucha,
   agente y cliente no escuchan al supervisor.
   En modo whisper: supervisor habla al agente,
   cliente no escucha al supervisor.
 end note

 @enduml

----

Barge-In — Intervencion Tripartita
======================================

.. uml::
 :caption: Estado de canal en barge-in — supervisor, agente y cliente conectados.

 @startuml

 [*] --> canal_agente_cliente : llamada activa\n(answer_inbound_calls)

 canal_agente_cliente --> supervision_activa : monitor_live_calls\n(silent/whisper)

 supervision_activa --> canal_tripartito : barge_in_calls
 canal_tripartito --> canal_agente_cliente : supervisor abandona\n(barge_in_calls off)
 supervision_activa --> canal_agente_cliente : supervisor abandona\nmonitoreo

 canal_agente_cliente --> [*] : llamada finalizada
 canal_tripartito --> [*] : llamada finalizada

 note right of canal_tripartito
   Los tres canales estan activos.
   Tono de supervision emitido
   en cada transicion (compliance).
 end note

 @enduml

----

Diagrama de componentes — MOD_Supervision
==========================================

.. uml::
 :caption: Componentes de MOD_Supervision y sus dependencias.

 @startuml

 actor "monitor_live_calls\nbarge_in_calls\nbroadcast_team_messages" as monitor_live_calls

 component "SupervisionEndpoint\n(/api/v1/supervision/)" as Supervisionendpoint
 component "TelephonyBridge\n(SIP/WebRTC barge-in)" as Telephonybridge
 component "ComplianceToneEmitter\n(tono obligatorio)" as TONE
 component "InternalMailbox\n(broadcast_team_messages)" as Internalmailbox

 database "audit_log\n(PostgreSQL)" as audit_log
 database "agent_state\n(Redis — estados activos)" as STATE

 monitor_live_calls --> Supervisionendpoint : HTTP requests
 Supervisionendpoint --> Telephonybridge : activar canal supervision/barge
 Supervisionendpoint --> TONE : emitir tono compliance
 Supervisionendpoint --> Internalmailbox : INSERT broadcast message
 Supervisionendpoint --> audit_log : INSERT SupervisionEvent
 Supervisionendpoint --> STATE : leer estado agentes activos

 @enduml
