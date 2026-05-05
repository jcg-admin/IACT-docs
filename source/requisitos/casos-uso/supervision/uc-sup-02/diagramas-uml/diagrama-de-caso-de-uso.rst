8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_SUP_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "barge_in_calls" as INVOKER
 actor "Operator" as OPERATOR <<beneficiario>>
 actor "Caller" as CALLER <<externo>>
 actor "Call" as CALL <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in en Llamada\n(3-way)" as UC_SUP_02
   usecase "Validar reason ≥ 20" as VALIDAR_REASON
   usecase "Conectar al call_id\n(audible para todos)" as CONECTAR
   usecase "Emitir AuditEvent\nBARGE_IN\n(P-39 reforzado)" as AUDIT
 }

 INVOKER --> UC_SUP_02
 UC_SUP_02 ..> VALIDAR_REASON : <<include>>
 UC_SUP_02 ..> CONECTAR : <<include>>
 UC_SUP_02 ..> AUDIT : <<include>>

 CONECTAR --> CALL
 CONECTAR --> OPERATOR
 CONECTAR --> CALLER
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of CONECTAR
   3-way audible: supervisor habla
   con Operator y Caller. Mas
   sensitivo que UC_SUP_01 (silent
   o whisper) — caller percibe
   intervention.
 end note

 note bottom of AUDIT
   P-39 audit reforzado.
   reason ≥ 20 chars obligatoria.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con flag barged=true durante 3-way.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session padre del Call.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent BARGE_IN (P-39).
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento.
