.. meta::
 :artefacto: ARQ_MOD_009_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/operator/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_009_componentes_mod_operator:

======================================
Diagrama de componentes — MOD_Operator
======================================

.. uml::
 :caption: Componentes de MOD_Operator y sus dependencias.

 @startuml

 actor "manage_own_agent_state\nanswer_inbound_calls\nmake_outbound_calls" as manage_own_agent_state

 component "AgentPanel\n(API views)" as Agentpanel
 component "TelephonyBridge\n(SIP/WebRTC)" as Telephonybridge
 component "DispositionService\n(enter_call_disposition)" as DISP
 component "PerformanceDashboard\n(view_own_performance_dashboard)" as DASH
 component "InternalMailbox\n(read_own_mailbox)" as Internalmailbox

 database "auth_session\n(PostgreSQL)" as SESS
 database "audit_log\n(PostgreSQL)" as audit_log
 database "agent_state\n(cache)" as STATE

 manage_own_agent_state --> Agentpanel : HTTP requests
 Agentpanel --> Telephonybridge : control llamadas
 Agentpanel --> DISP : registro disposicion
 Agentpanel --> DASH : estadisticas propias
 Agentpanel --> Internalmailbox : buzon mensajes
 Agentpanel --> SESS : validar sesion JWT
 Agentpanel --> audit_log : emitir AuditEvent
 Agentpanel --> STATE : leer/escribir estado agente

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/operator/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
