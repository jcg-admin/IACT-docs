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
 component "DispositionService\n(enter_call_disposition)" as DISPOSICION_LLAMADA
 component "PerformanceDashboard\n(view_own_performance_dashboard)" as DASHBOARD_IVR
 component "InternalMailbox\n(read_own_mailbox)" as Internalmailbox

 database "auth_session\n(PostgreSQL)" as BASE_SESIONES
 database "audit_log\n(PostgreSQL)" as audit_log
 database "agent_state\n(cache)" as ESTADO_AGENTE_CACHE

 manage_own_agent_state --> Agentpanel : HTTP requests
 Agentpanel --> Telephonybridge : control llamadas
 Agentpanel --> DISPOSICION_LLAMADA : registro disposicion
 Agentpanel --> DASHBOARD_IVR : estadisticas propias
 Agentpanel --> Internalmailbox : buzon mensajes
 Agentpanel --> BASE_SESIONES : validar sesion JWT
 Agentpanel --> audit_log : emitir AuditEvent
 Agentpanel --> ESTADO_AGENTE_CACHE : leer/escribir estado agente

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/operator/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
