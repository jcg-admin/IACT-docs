8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "initiate_outbound_call" as INVOKER
 actor "Caller (target)" as TARGET <<externo>>
 actor "Call" as CALL <<sistema>>
 actor "Campaign" as CAMP <<sistema>>
 actor "RuleValidator" as RV <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_03\nRealizar Llamada\nSaliente" as UC_OPR_03
   usecase "Validar mode\n(manual | preview | auto)" as VALIDAR_MODE
   usecase "Verificar AntiFraud\n(numero en lista permitida)" as VERIFY_AF
   usecase "Asociar campaign_id\no callback_id" as ASOCIAR
   usecase "Iniciar Call outbound" as INICIAR
   usecase "Emitir AuditEvent\nOUTBOUND_INITIATED" as AUDIT
 }

 INVOKER --> UC_OPR_03
 UC_OPR_03 ..> VALIDAR_MODE : <<include>>
 UC_OPR_03 ..> VERIFY_AF : <<include>>
 UC_OPR_03 ..> ASOCIAR : <<include>>
 UC_OPR_03 ..> INICIAR : <<include>>
 UC_OPR_03 ..> AUDIT : <<include>>

 VERIFY_AF --> RV
 ASOCIAR --> CAMP
 INICIAR --> CALL
 INICIAR --> TARGET
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VERIFY_AF
   Politica anti-fraud: numero NO en
   lista permitida → bloqueado.
   CNST-009/013/025.
 end note

 note bottom of VALIDAR_MODE
   Modes: manual (agente teclea),
   preview (agente acepta),
   auto-dial (sistema marca y asigna
   agente al contestar).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con type=outbound, mode, dispositions.
 - :doc:`/arquitectura-tecnica/domain-model/campaign` —
   Campaign asociada (anti-fraud whitelist por campana).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que valida anti-fraud.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent OUTBOUND_INITIATED.
