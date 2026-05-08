8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "manage_own_agent_state" as INVOKER
 actor "Session" as SESSION <<sistema>>
 actor "EvaluatorReloader" as ER <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado\ndel Agente" as UC_OPR_01
   usecase "Validar transicion\n(state machine)" as VALIDAR_TRANS
   usecase "Persistir estado\n(available | not_ready | break)" as PERSISTIR
   usecase "Notificar router\n(propagar disponibilidad)" as NOTIFY_ROUTER
   usecase "Emitir AuditEvent\nAGENT_STATE_CHANGED" as AUDIT
 }

 INVOKER --> UC_OPR_01
 UC_OPR_01 ..> VALIDAR_TRANS : <<include>>
 UC_OPR_01 ..> PERSISTIR : <<include>>
 UC_OPR_01 ..> NOTIFY_ROUTER : <<include>>
 UC_OPR_01 ..> AUDIT : <<include>>

 PERSISTIR --> SESSION
 NOTIFY_ROUTER --> ER
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of NOTIFY_ROUTER
   Router consume estado para
   routing — solo enruta a agentes
   en `available`. Cambio de
   estado debe propagarse en
   tiempo real.
 end note

 note bottom of AUDIT
   BReq-007. Cambios de estado
   afectan adherence — auditados
   para reportes UC_RPT_12.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session del agente con campo agent_state.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   User del agente.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   coordinador de propagacion de cambios al routing.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent AGENT_STATE_CHANGED.
