8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_SUP_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "monitor_live_calls" as INVOKER
 actor "Operator (target)" as OPERATOR <<beneficiario>>
 actor "Caller" as CALLER <<externo>>
 actor "TelephonyClient" as TELEPHONY <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada\n(silent | whisper)" as UC_SUP_01
   usecase "Validar reason ≥ 20" as VALIDAR_REASON
   usecase "Validar mode\n(silent | whisper)" as VALIDAR_MODE
   usecase "Conectar al call_id" as CONECTAR
   usecase "Notificar tono\naudible al Operator" as NOTIFICAR
   usecase "AuditEvent\nMONITOR_STARTED\n(P-39 reforzado)" as AUDIT
 }

 INVOKER --> UC_SUP_01
 UC_SUP_01 ..> VALIDAR_REASON : <<include>>
 UC_SUP_01 ..> VALIDAR_MODE : <<include>>
 UC_SUP_01 ..> CONECTAR : <<include>>
 UC_SUP_01 ..> NOTIFICAR : <<include>>
 UC_SUP_01 ..> AUDIT : <<include>>

 CONECTAR --> TELEPHONY
 NOTIFICAR --> OPERATOR
 Sistema --> AUDIT
 AUDIT --> view_audit_log

 note bottom of NOTIFICAR
   Compliance legal: tono audible
   obligatorio al Operator. Caller
   no oye. Whisper permite
   instruir al Operator.
 end note

 note bottom of AUDIT
   P-39 audit reforzado:
   reason + mode + supervisor +
   call_id + Operator afectado.
   Operacion muy sensitiva.
 end note

 @enduml
