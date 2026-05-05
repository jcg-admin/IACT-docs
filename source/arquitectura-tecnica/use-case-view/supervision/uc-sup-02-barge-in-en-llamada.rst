.. meta::
 :artefacto: AT_UC_SUP_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: supervision
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_sup_02_barge_in_en_llamada:

============================================================
UC_SUP_02 — Barge-in en Llamada
============================================================

Supervisor se conecta a llamada activa en modo 3-way (audible para
Operator y Caller). Mas sensitivo que UC_SUP_01 (silent/whisper) —
caller percibe intervention. Reason ≥ 20 obligatoria. P-39 audit
reforzado.

.. uml::
 :caption: UC_SUP_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "barge_in_calls" as barge_in_calls
 actor "answer_inbound_calls" as Operator <<beneficiario>>
 actor "Caller" as Caller <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in en Llamada\n(3-way)" as UC_SUP_02
   usecase "Verificar\nbarge_in_calls" as VERIFICAR_AGR
   usecase "Validar agent target\n∈ segmento (CNST-008)" as VALIDAR_SEGMENTO
   usecase "Validar reason ≥ 20" as VALIDAR_REASON
   usecase "Telephony.bridge_audio\n(sup + caller + agent)" as ESTABLECER
   usecase "Emitir AuditEvent\nBARGE_IN (P-39 reforzado)" as AUDITAR
 }

 barge_in_calls --> UC_SUP_02

 UC_SUP_02 ..> VERIFICAR_AGR : <<include>>
 UC_SUP_02 ..> VALIDAR_SEGMENTO : <<include>>
 UC_SUP_02 ..> VALIDAR_REASON : <<include>>
 UC_SUP_02 ..> ESTABLECER : <<include>>
 UC_SUP_02 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_SEGMENTO --> SegmentResolver
 ESTABLECER --> Call
 ESTABLECER --> Operator
 ESTABLECER --> Caller
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of ESTABLECER
   3-way audible: supervisor habla
   con Operator y Caller. Mas sensitivo
   que UC_SUP_01 — caller percibe
   intervention.
 end note

 note bottom of AUDITAR
   P-39 audit reforzado.
   reason ≥ 20 chars obligatoria.
   CNST-013 + CNST-025.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con flag barged=true.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session padre.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (P-39).
 - :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index` —
   monitorear (silent/whisper).
 - :doc:`/requisitos/casos-uso/supervision/uc-sup-02/index` —
   spec textual.
