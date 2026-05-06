.. meta::
 :artefacto: AT_DESIGN_SEQ_OPERATOR
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: operator
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_operator:

============================================================
Design View — MOD_Operator: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Operator: el agente acepta
una llamada en cola, atiende, registra ``Action`` por cada
operacion y finalmente disposition (cierre con codigo).

.. uml::
 :caption: MOD_Operator — atencion de llamada con disposition.

 @startuml

 actor "answer_call" as answer_call
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "Action" as Action <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 answer_call -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> answer_call : OK
 deactivate AuthorizationGuard

 answer_call -> Call : answer()
 activate Call
 Call --> answer_call : Call{state=answered}

 answer_call -> Action : create(answer, call_id)
 activate Action
 Action -> AuditService : emit(AuditEvent)
 Action --> answer_call : OK
 deactivate Action

 ' Operacion durante la llamada
 answer_call -> Call : hold()
 Call --> answer_call : Call{state=on_hold}
 answer_call -> Action : create(hold, call_id)
 Action -> AuditService : emit(AuditEvent)

 answer_call -> Call : unhold()
 Call --> answer_call : Call{state=answered}
 answer_call -> Action : create(unhold, call_id)

 ' Cierre con disposition
 answer_call -> Call : disposition(code, notes)
 Call -> AuditService : emit(AuditEvent\ntype=call_closed)
 Call --> answer_call : Call{state=closed}
 deactivate Call
 deactivate AuditService

 note right of Call
   Call FSM: answered -> on_hold ->
   answered -> wrap -> closed.
   Ver state-call.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-operator`
 - :doc:`/arquitectura-tecnica/design-view/state-call`
 - :doc:`/arquitectura-tecnica/use-case-view/operator/index`
 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/call`
 - :doc:`/arquitectura-tecnica/domain-model/action`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
