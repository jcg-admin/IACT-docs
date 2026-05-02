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

 actor "answer_inbound_calls" as OPR
 participant "AgentPanel\n(/api/v1/operator/)" as EP
 participant "TelephonyRouter\n(ACD/IVR)" as TEL
 participant "DispositionEndpoint\n(/api/v1/disposition/)" as DISP
 database "audit_log\n(PostgreSQL)" as AUD

 TEL -> EP : llamada entrante asignada al agente
 EP -> OPR : notificacion de llamada
 OPR -> EP : POST /answer
 EP -> EP : JWT + RBAC (answer_inbound_calls)
 EP -> TEL : conectar canal audio
 TEL --> OPR : canal de voz activo

 note over OPR, TEL
   Operador atiende la llamada.
   Estado del agente = busy.
 end note

 OPR -> EP : POST /disposition {code, notes}
 EP -> EP : JWT + RBAC (enter_call_disposition)
 EP -> DISP : INSERT disposition record
 EP -> AUD : INSERT AuditEvent CALL_DISPOSED
 EP -> TEL : liberar canal
 TEL --> EP : agente disponible
 EP --> OPR : 200 OK, estado = available

 @enduml

----

Diagrama de componentes — MOD_Operator
==========================================

.. uml::
 :caption: Componentes de MOD_Operator y sus dependencias.

 @startuml

 actor "manage_own_agent_state\nanswer_inbound_calls\nmake_outbound_calls" as OPR

 component "AgentPanel\n(DRF views)" as AP
 component "TelephonyBridge\n(SIP/WebRTC)" as TEL
 component "DispositionService\n(enter_call_disposition)" as DISP
 component "PerformanceDashboard\n(view_own_performance_dashboard)" as DASH
 component "InternalMailbox\n(read_own_mailbox)" as MB

 database "auth_session\n(PostgreSQL)" as SESS
 database "audit_log\n(PostgreSQL)" as AUD
 database "agent_state\n(Redis/cache)" as STATE

 OPR --> AP : HTTP requests
 AP --> TEL : control llamadas
 AP --> DISP : registro disposicion
 AP --> DASH : estadisticas propias
 AP --> MB : buzon mensajes
 AP --> SESS : validar sesion JWT
 AP --> AUD : emitir AuditEvent
 AP --> STATE : leer/escribir estado agente

 @enduml
