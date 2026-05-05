.. meta::
 :artefacto: AT_UC_MOD_OPERATOR
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_operator:

================================================
MOD_Operator — Panel del Operador: UC por Modulo
================================================

MOD_Operator — Panel del Operador
====================================

Funcionalidades del agente de call center: cambio de estado,
atencion y transferencia de llamadas, disposicion, breaks y
consulta de estadisticas personales.

.. uml::
 :caption: Figura 25 — MOD_Operator: casos de uso

 @startuml
 left to right direction

 actor "manage_own_agent_state" as manage_own_agent_state
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "make_outbound_calls" as make_outbound_calls
 actor "hold_calls" as hold_calls
 actor "transfer_calls" as transfer_calls
 actor "enter_call_disposition" as enter_call_disposition
 actor "request_break" as request_break
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 actor "view_own_call_history" as view_own_call_history
 actor "read_own_mailbox" as read_own_mailbox

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado\ndel Agente" as CAMBIAR_ESTADO_AGENTE
   usecase "UC_OPR_02\nAtender Llamada\nEntrante" as ATENDER_LLAMADA
   usecase "UC_OPR_03\nIniciar Llamada\nOutbound" as INICIAR_LLAMADA_OUTBOUND
   usecase "UC_OPR_04\nHold/Unhold\nLlamada" as HOLD_UNHOLD_LLAMADA
   usecase "UC_OPR_05\nTransferir\nLlamada" as TRANSFERIR_LLAMADA
   usecase "UC_OPR_06\nDisposicion\npost-Llamada" as DISPOSICION_POST_LLAMADA
   usecase "UC_OPR_07\nTomar Break" as TOMAR_BREAK
   usecase "UC_OPR_08\nVer Dashboard\nde Desempeno" as VER_DASHBOARD_DESEMPENO
   usecase "UC_OPR_09\nVer Historial\nde Llamadas" as VER_HISTORIAL_LLAMADAS
   usecase "UC_OPR_10\nVer Buzon\nde Mensajes" as VER_BUZON_MENSAJES
 }

 manage_own_agent_state --> CAMBIAR_ESTADO_AGENTE
 answer_inbound_calls --> ATENDER_LLAMADA
 make_outbound_calls --> INICIAR_LLAMADA_OUTBOUND
 hold_calls --> HOLD_UNHOLD_LLAMADA
 transfer_calls --> TRANSFERIR_LLAMADA
 enter_call_disposition --> DISPOSICION_POST_LLAMADA
 request_break --> TOMAR_BREAK
 view_own_performance_dashboard --> VER_DASHBOARD_DESEMPENO
 view_own_call_history --> VER_HISTORIAL_LLAMADAS
 read_own_mailbox --> VER_BUZON_MENSAJES

 ATENDER_LLAMADA ..> CAMBIAR_ESTADO_AGENTE : <<include>>
 DISPOSICION_POST_LLAMADA ..> ATENDER_LLAMADA : <<include>>
 HOLD_UNHOLD_LLAMADA ..> ATENDER_LLAMADA : <<include>>
 TRANSFERIR_LLAMADA ..> ATENDER_LLAMADA : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
