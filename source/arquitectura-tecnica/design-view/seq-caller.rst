.. meta::
 :artefacto: AT_DESIGN_SEQ_CALLER
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: caller
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_caller:

============================================================
Design View — MOD_Caller: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Caller: ingreso de una llamada
nueva, navegacion IVR (NavDomain), enrutamiento a cola/operador
y registro del Call.

.. uml::
 :caption: MOD_Caller — ingreso y enrutamiento IVR.

 @startuml

 actor Caller <<externo>>
 actor "Call" as Call <<sistema>>
 actor "Menu" as Menu <<sistema>>
 actor "NavDomain" as NavDomain <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 Caller -> Call : initiate(phone, dnis)
 activate Call
 Call -> Menu : load(dnis)
 activate Menu
 Menu --> Call : Menu{opciones}
 deactivate Menu

 loop navegacion IVR
   Call -> Caller : prompt opciones
   Caller --> Call : DTMF
   Call -> NavDomain : record(option)
   activate NavDomain
   NavDomain --> Call : OK
   deactivate NavDomain
 end

 alt opcion = transfer to operator
   Call -> Call : enqueue(queue)
 else opcion = self-service
   Call -> Call : provide info
 end

 Call -> AuditService : emit(AuditEvent\ntype=call_routed)
 activate AuditService
 AuditService --> Call : OK
 deactivate AuditService
 deactivate Call

 note right of Call
   Call FSM: initiated -> menu ->
   queued | self_service -> ...
   ver state-call.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-caller`
 - :doc:`/arquitectura-tecnica/design-view/state-call`
 - :doc:`/arquitectura-tecnica/use-case-view/caller/index`
 - :doc:`/arquitectura-tecnica/domain-model/call`
 - :doc:`/arquitectura-tecnica/domain-model/menu`
 - :doc:`/arquitectura-tecnica/domain-model/nav-domain`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
