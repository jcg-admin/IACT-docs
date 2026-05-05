8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "initiate_outbound_call" as INVOKER
 actor "Caller (target)" as TARGET <<externo>>
 actor "TelephonyChannel" as CHANNEL <<sistema>>
 actor "CampaignRepo" as CAMP <<sistema>>
 actor "CallbackQueue" as CBQUEUE <<sistema>>
 actor "AntiFraudList" as ANTIFRAUD <<sistema>>
 actor "Sistema" as Sistema <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_03\nRealizar Llamada\nSaliente" as UC_OPR_03
   usecase "Validar mode\n(manual | preview | auto)" as VALIDAR_MODE
   usecase "Verificar AntiFraud\n(numero en lista permitida)" as VERIFY_AF
   usecase "Asociar campaign_id\no callback_id" as ASOCIAR
   usecase "Iniciar llamada\nvia TelephonyChannel" as INICIAR
   usecase "AuditEvent\nOUTBOUND_INITIATED" as AUDIT
 }

 INVOKER --> UC_OPR_03
 UC_OPR_03 ..> VALIDAR_MODE : <<include>>
 UC_OPR_03 ..> VERIFY_AF : <<include>>
 UC_OPR_03 ..> ASOCIAR : <<include>>
 UC_OPR_03 ..> INICIAR : <<include>>
 UC_OPR_03 ..> AUDIT : <<include>>

 VERIFY_AF --> ANTIFRAUD
 ASOCIAR --> CAMP
 ASOCIAR --> CBQUEUE
 INICIAR --> CHANNEL
 INICIAR --> TARGET
 Sistema --> AUDIT
 AUDIT --> view_audit_log

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
