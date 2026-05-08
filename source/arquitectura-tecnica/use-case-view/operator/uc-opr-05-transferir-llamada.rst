.. meta::
 :artefacto: AT_UC_OPR_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Fuera del scope
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_opr_05_transferir_llamada:

==============================
UC_OPR_05 — Transferir Llamada
==============================

Agente transfiere caller a otro Operator o cola. Modes: warm
(consulta antes de pasar), cold (pasa directo), queue (a cola por
skill). Reason ≥ 10 obligatoria. ``transfer_own_call``. Insumo
para UC_RPT_15.

.. uml::
 :caption: UC_OPR_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "transfer_own_call" as transfer_own_call
 actor "Operator destino / Cola" as Target <<beneficiario>>
 actor "Caller" as Caller <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Call" as Call <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_05\nTransferir Llamada" as UC_OPR_05
   usecase "Validar reason\n(≥10 chars)" as VALIDAR_REASON
   usecase "Validar target\n(agent disponible | cola valida)" as VALIDAR_TARGET
   usecase "Validar mode\n(warm | cold | queue)" as VALIDAR_MODE
   usecase "Conectar al target\n(warm: presentacion)" as CONECTAR
   usecase "Pasar caller" as PASAR
   usecase "Emitir AuditEvent\nCALL_TRANSFERRED\n(insumo UC_RPT_15)" as AUDITAR
 }

 transfer_own_call --> UC_OPR_05

 UC_OPR_05 ..> VALIDAR_REASON : <<include>>
 UC_OPR_05 ..> VALIDAR_TARGET : <<include>>
 UC_OPR_05 ..> VALIDAR_MODE : <<include>>
 UC_OPR_05 ..> CONECTAR : <<include>>
 UC_OPR_05 ..> PASAR : <<include>>
 UC_OPR_05 ..> AUDITAR : <<include>>

 CONECTAR --> Call
 PASAR --> Target
 PASAR --> Caller
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_MODE
   Warm: A consulta a B antes
   de pasar. Cold: directo.
   Queue: a cola por skill.
   RoutingStrategy.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con transferred=true + reason.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Sessions origen y destino.
 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service` —
   consume datos UC_RPT_15.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   RoutingStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-05/index` —
   spec textual.
