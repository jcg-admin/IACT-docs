.. meta::
 :artefacto: ARQ_MOD_009_DIAG_CICLO_VIDA
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/operator/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_009_ciclo_vida_estado_agente:

===================================
Ciclo de Vida del Estado del Agente
===================================

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

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/operator/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
