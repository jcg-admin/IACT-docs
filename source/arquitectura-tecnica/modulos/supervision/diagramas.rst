.. _arq-mod-010-diagramas:

================================================
ARQ_MOD_010 — Diagramas de Comportamiento
================================================


Flujo de Monitoreo en Tiempo Real
====================================

.. uml::
 :caption: Secuencia UC_SUP_01 — monitor_live_calls en modo silent/whisper con tono de supervision.

 @startuml

 actor "monitor_live_calls" as SUP
 participant "SupervisionEndpoint\n(/api/v1/supervision/)" as EP
 participant "TelephonyBridge\n(SIP/WebRTC)" as TEL
 participant "AuditLog" as AUD
 actor "answer_inbound_calls" as OPR

 SUP -> EP : POST /supervision/monitor {call_id, mode}
 EP -> EP : JWT + RBAC (monitor_live_calls)
 EP -> TEL : conectar canal supervision\n(mode: silent|whisper)
 TEL -> OPR : emitir tono de supervision\n(compliance obligatorio)
 TEL --> EP : canal activo
 EP -> AUD : INSERT SupervisionEvent {tipo, supervisor, call_id}
 EP --> SUP : 200 OK

 note over SUP, OPR
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

 actor "monitor_live_calls\nbarge_in_calls\nbroadcast_team_messages" as SUP

 component "SupervisionEndpoint\n(/api/v1/supervision/)" as EP
 component "TelephonyBridge\n(SIP/WebRTC barge-in)" as TEL
 component "ComplianceToneEmitter\n(tono obligatorio)" as TONE
 component "InternalMailbox\n(broadcast_team_messages)" as MB

 database "audit_log\n(PostgreSQL)" as AUD
 database "agent_state\n(Redis — estados activos)" as STATE

 SUP --> EP : HTTP requests
 EP --> TEL : activar canal supervision/barge
 EP --> TONE : emitir tono compliance
 EP --> MB : INSERT broadcast message
 EP --> AUD : INSERT SupervisionEvent
 EP --> STATE : leer estado agentes activos

 @enduml
