.. _arq-mod-009-diagramas:

================================================
ARQ_MOD_009 — Diagramas de Comportamiento
================================================


Ciclo de Vida del Estado del Agente
======================================

.. uml::
 :caption: Estado del agente de call center — transiciones gestionadas por manage_own_agent_state.

 @startuml

 [*] --> offline : login exitoso

 offline --> available : manage_own_agent_state
 available --> busy : answer_inbound_calls\no make_outbound_calls
 available --> on_break : request_break aprobado
 busy --> available : llamada finalizada\n+ enter_call_disposition
 busy --> hold : hold_calls
 hold --> busy : hold_calls (resume)
 busy --> transfer_pending : transfer_calls
 transfer_pending --> available : transferencia completada
 on_break --> available : fin de break
 available --> offline : logout (UC_AUTH_02)

 note right of busy
   En estado busy el operador
   puede poner en hold o
   transferir la llamada.
 end note

 @enduml

----

Secuencia de Atencion de Llamada Entrante
==========================================

.. uml::
 :caption: Secuencia UC_OPR_02 — atencion de llamada entrante con disposicion post-llamada.

 @startuml

 actor "answer_inbound_calls" as answer_inbound_calls
 participant "AgentPanel\n(/api/v1/operator/)" as Agentpanel
 participant "TelephonyRouter\n(ACD/IVR)" as Telephonyrouter
 participant "DispositionEndpoint\n(/api/v1/disposition/)" as DISP
 database "audit_log\n(PostgreSQL)" as audit_log

 Telephonyrouter -> Agentpanel : llamada entrante asignada al agente
 Agentpanel -> answer_inbound_calls : notificacion de llamada
 answer_inbound_calls -> Agentpanel : POST /answer
 Agentpanel -> Agentpanel : JWT + RBAC (answer_inbound_calls)
 Agentpanel -> Telephonyrouter : conectar canal audio
 Telephonyrouter --> answer_inbound_calls : canal de voz activo

 note over answer_inbound_calls, Telephonyrouter
   Operador atiende la llamada.
   Estado del agente = busy.
 end note

 answer_inbound_calls -> Agentpanel : POST /disposition {code, notes}
 Agentpanel -> Agentpanel : JWT + RBAC (enter_call_disposition)
 Agentpanel -> DISP : INSERT disposition record
 Agentpanel -> audit_log : INSERT AuditEvent CALL_DISPOSED
 Agentpanel -> Telephonyrouter : liberar canal
 Telephonyrouter --> Agentpanel : agente disponible
 Agentpanel --> answer_inbound_calls : 200 OK, estado = available

 @enduml

----

Diagrama de componentes — MOD_Operator
==========================================

.. uml::
 :caption: Componentes de MOD_Operator y sus dependencias.

 @startuml

 actor "manage_own_agent_state\nanswer_inbound_calls\nmake_outbound_calls" as manage_own_agent_state

 component "AgentPanel\n(DRF views)" as Agentpanel
 component "TelephonyBridge\n(SIP/WebRTC)" as Telephonybridge
 component "DispositionService\n(enter_call_disposition)" as DISP
 component "PerformanceDashboard\n(view_own_performance_dashboard)" as DASH
 component "InternalMailbox\n(read_own_mailbox)" as Internalmailbox

 database "auth_session\n(PostgreSQL)" as SESS
 database "audit_log\n(PostgreSQL)" as audit_log
 database "agent_state\n(Redis/cache)" as STATE

 manage_own_agent_state --> Agentpanel : HTTP requests
 Agentpanel --> Telephonybridge : control llamadas
 Agentpanel --> DISP : registro disposicion
 Agentpanel --> DASH : estadisticas propias
 Agentpanel --> Internalmailbox : buzon mensajes
 Agentpanel --> SESS : validar sesion JWT
 Agentpanel --> audit_log : emitir AuditEvent
 Agentpanel --> STATE : leer/escribir estado agente

 @enduml
