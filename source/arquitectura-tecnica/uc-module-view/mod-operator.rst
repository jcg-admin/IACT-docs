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
   usecase "UC_OPR_01\nCambiar Estado\ndel Agente" as O01
   usecase "UC_OPR_02\nAtender Llamada\nEntrante" as O02
   usecase "UC_OPR_03\nIniciar Llamada\nOutbound" as O03
   usecase "UC_OPR_04\nHold/Unhold\nLlamada" as O04
   usecase "UC_OPR_05\nTransferir\nLlamada" as O05
   usecase "UC_OPR_06\nDisposicion\npost-Llamada" as O06
   usecase "UC_OPR_07\nTomar Break" as O07
   usecase "UC_OPR_08\nVer Dashboard\nde Desempeno" as O08
   usecase "UC_OPR_09\nVer Historial\nde Llamadas" as O09
   usecase "UC_OPR_10\nVer Buzon\nde Mensajes" as O10
 }

 manage_own_agent_state --> O01
 answer_inbound_calls --> O02
 make_outbound_calls --> O03
 hold_calls --> O04
 transfer_calls --> O05
 enter_call_disposition --> O06
 request_break --> O07
 view_own_performance_dashboard --> O08
 view_own_call_history --> O09
 read_own_mailbox --> O10

 O02 ..> O01 : <<include>>
 O06 ..> O02 : <<include>>
 O04 ..> O02 : <<include>>
 O05 ..> O02 : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
