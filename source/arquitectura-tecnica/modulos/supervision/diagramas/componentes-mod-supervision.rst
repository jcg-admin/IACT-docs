.. meta::
 :artefacto: ARQ_MOD_010_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/supervision/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_010_componentes_mod_supervision:

=========================================
Diagrama de componentes — MOD_Supervision
=========================================

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
 database "agent_state\n(cache)" as STATE

 monitor_live_calls --> Supervisionendpoint : HTTP requests
 Supervisionendpoint --> Telephonybridge : activar canal supervision/barge
 Supervisionendpoint --> TONE : emitir tono compliance
 Supervisionendpoint --> Internalmailbox : INSERT broadcast message
 Supervisionendpoint --> audit_log : INSERT SupervisionEvent
 Supervisionendpoint --> STATE : leer estado agentes activos

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/supervision/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
