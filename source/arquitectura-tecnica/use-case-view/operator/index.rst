.. meta::
 :artefacto: AT_UC_MOD_OPERATOR
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_operator:

================================================
MOD_Operator — Panel del Operador: UC por Modulo
================================================

Funcionalidades del agente de call center: cambio de estado,
atención y transferencia de llamadas, disposición, breaks y
consulta de estadísticas personales.

.. uml::
 :caption: MOD_Operator — Operator es actor único; Caller
           es origen externo de llamadas.

 @startuml
 left to right direction

 actor Operator
 actor "Caller\n<<external>>" as Caller

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

 Operator --> CAMBIAR_ESTADO_AGENTE
 Operator --> ATENDER_LLAMADA
 Operator --> INICIAR_LLAMADA_OUTBOUND
 Operator --> HOLD_UNHOLD_LLAMADA
 Operator --> TRANSFERIR_LLAMADA
 Operator --> DISPOSICION_POST_LLAMADA
 Operator --> TOMAR_BREAK
 Operator --> VER_DASHBOARD_DESEMPENO
 Operator --> VER_HISTORIAL_LLAMADAS
 Operator --> VER_BUZON_MENSAJES

 Caller --> ATENDER_LLAMADA

 ATENDER_LLAMADA ..> CAMBIAR_ESTADO_AGENTE : <<include>>
 DISPOSICION_POST_LLAMADA ..> ATENDER_LLAMADA : <<include>>
 HOLD_UNHOLD_LLAMADA ..> ATENDER_LLAMADA : <<include>>
 TRANSFERIR_LLAMADA ..> ATENDER_LLAMADA : <<include>>

 note right of MOD_Operator
   Codenames RBAC:
     Operator (AGR-001) →
       manage_own_agent_state,
       answer_inbound_calls,
       make_outbound_calls,
       hold_calls, transfer_calls,
       enter_call_disposition,
       request_break,
       view_own_performance_dashboard,
       view_own_call_history,
       read_own_mailbox
     Caller: actor externo (no autenticado)
       que origina ATENDER_LLAMADA.
 end note

 @enduml

Lectura del diagrama
====================

- ``Operator`` (AGR-001) ejecuta todas las operaciones
  del panel del agente.
- ``Caller`` es el actor **externo** que dispara
  ``UC_OPR_02``: el caller llama, el operador atiende.
  El caller no se autentica en IACT — solo origina la
  llamada vía el conmutador IVR.
- ``UC_OPR_02 Atender Llamada`` es ``<<include>>`` por
  los UCs de gestión de llamadas activas
  (``UC_OPR_04/05/06``): no se puede transferir, hold
  ni disponer si no hay una llamada atendida primero.

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
