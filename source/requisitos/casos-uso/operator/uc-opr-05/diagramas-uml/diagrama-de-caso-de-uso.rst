8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "transfer_own_call" as INVOKER
 actor "Operator destino / Cola" as TARGET <<beneficiario>>
 actor "Caller" as CALLER <<externo>>
 actor "Call" as CALL <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_05\nTransferir Llamada" as UC_OPR_05
   usecase "Validar reason\n(≥ 10 chars)" as VALIDAR_REASON
   usecase "Validar target\n(agent disponible | cola valida)" as VALIDAR_TARGET
   usecase "Validar mode\n(warm | cold)" as VALIDAR_MODE
   usecase "Conectar al target\n(warm: presentacion)" as CONECTAR
   usecase "Pasar caller" as PASAR
   usecase "Emitir AuditEvent\nCALL_TRANSFERRED\n(insumo UC_RPT_15)" as AUDIT
 }

 INVOKER --> UC_OPR_05
 UC_OPR_05 ..> VALIDAR_REASON : <<include>>
 UC_OPR_05 ..> VALIDAR_TARGET : <<include>>
 UC_OPR_05 ..> VALIDAR_MODE : <<include>>
 UC_OPR_05 ..> CONECTAR : <<include>>
 UC_OPR_05 ..> PASAR : <<include>>
 UC_OPR_05 ..> AUDIT : <<include>>

 CONECTAR --> CALL
 PASAR --> TARGET
 PASAR --> CALLER
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VALIDAR_MODE
   Warm: agente A consulta a B
   antes de pasar caller. Cold:
   pasa directo. Queue: pasa a
   cola por skill.
 end note

 note bottom of AUDIT
   Reason required + audited.
   Insumo para UC_RPT_15
   (Reporte de Transferencias)
   para identificar patrones.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con flag transferred=true + reason + target.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Sessions origen y destino.
 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service` —
   consume datos de transfers (UC_RPT_15).
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent CALL_TRANSFERRED.
