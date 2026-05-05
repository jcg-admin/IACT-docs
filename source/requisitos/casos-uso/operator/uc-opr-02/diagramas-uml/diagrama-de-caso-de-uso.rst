8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "answer_inbound_calls" as INVOKER
 actor "Caller" as CALLER <<externo>>
 actor "TelephonyChannel" as CHANNEL <<sistema>>
 actor "Sistema" as Sistema <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAtender Llamada\nEntrante" as UC_OPR_02
   usecase "Validar sesion\nactiva + state=available" as VALIDAR_AGENT
   usecase "Validar llamada\nofferred" as VALIDAR_OFFER
   usecase "Establecer canal\n(audio bidireccional)" as ESTABLECER
   usecase "Transicion estado\nbusy/in-call" as TRANSICION
   usecase "AuditEvent\nCALL_ANSWERED" as AUDIT
 }

 INVOKER --> UC_OPR_02
 UC_OPR_02 ..> VALIDAR_AGENT : <<include>>
 UC_OPR_02 ..> VALIDAR_OFFER : <<include>>
 UC_OPR_02 ..> ESTABLECER : <<include>>
 UC_OPR_02 ..> TRANSICION : <<include>>
 UC_OPR_02 ..> AUDIT : <<include>>

 ESTABLECER --> CHANNEL
 ESTABLECER --> CALLER
 Sistema --> AUDIT
 AUDIT --> view_audit_log

 note bottom of UC_OPR_02
   BReq-007. CNST-009 auth + CNST-013/025
   audit del answer event.
   Out of scope: hold (UC_OPR_04),
   transferir (UC_OPR_05),
   disposition (UC_OPR_06).
 end note

 @enduml
