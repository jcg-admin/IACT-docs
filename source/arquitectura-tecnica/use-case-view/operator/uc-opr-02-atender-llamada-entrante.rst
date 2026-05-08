.. meta::
 :artefacto: AT_UC_OPR_02_USECASE
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

.. _at_uc_opr_02_atender_llamada_entrante:

=====================================
UC_OPR_02 — Atender Llamada Entrante
=====================================

El agente acepta la oferta de llamada (offer ring), establece canal de
audio bidireccional con el caller y queda en estado in-call. Operacion
critica del flujo operacional inbound del call center (BReq-007).

.. uml::
 :caption: UC_OPR_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "answer_inbound_calls" as answer_inbound_calls
 actor "Caller" as Caller <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "Session" as Session <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAtender Llamada\nEntrante\n.. extension points ..\nWhisperInfo" as UC_OPR_02
   usecase "Verificar\nanswer_inbound_calls" as VERIFICAR_AGR
   usecase "Validar oferta\nvigente al agente" as VALIDAR_OFERTA
   usecase "Validar agente\nstate=available" as VALIDAR_STATE
   usecase "Establecer canal\n(Telephony.bridge)" as ESTABLECER_CANAL
   usecase "Transicion atomic\nstate=busy" as TRANSICIONAR
   usecase "Iniciar CallSession" as INICIAR_SESSION
   usecase "Emitir AuditEvent\nCALL_ANSWERED" as AUDITAR
   usecase "Mostrar whisper info\n(skill, motivo, tiempo)" as WHISPER_INFO
   usecase "Decline oferta" as DECLINE
   usecase "Auto-decline por\ntimeout" as AUTO_DECLINE
 }

 answer_inbound_calls --> UC_OPR_02
 Caller --> UC_OPR_02

 UC_OPR_02 ..> VERIFICAR_AGR : <<include>>
 UC_OPR_02 ..> VALIDAR_OFERTA : <<include>>
 UC_OPR_02 ..> VALIDAR_STATE : <<include>>
 UC_OPR_02 ..> ESTABLECER_CANAL : <<include>>
 UC_OPR_02 ..> TRANSICIONAR : <<include>>
 UC_OPR_02 ..> INICIAR_SESSION : <<include>>
 UC_OPR_02 ..> AUDITAR : <<include>>
 WHISPER_INFO ..> UC_OPR_02 : <<extend>> (WhisperInfo)
 DECLINE ..> UC_OPR_02 : <<extend>>
 AUTO_DECLINE ..> UC_OPR_02 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 ESTABLECER_CANAL --> Call
 ESTABLECER_CANAL --> Caller
 TRANSICIONAR --> Session
 INICIAR_SESSION --> Session
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of TRANSICIONAR
   Atomic: UPDATE state busy +
   CallSession started + audit
   CALL_ANSWERED en una sola
   transaccion (CNST-013).
 end note

 note bottom of AUDITAR
   CNST-009 auth + CNST-013/025
   audit del answer event.
   Out of scope: hold (UC_OPR_04),
   transferir (UC_OPR_05),
   disposition (UC_OPR_06).
 end note

 note right of Caller
   Caller no autenticado, externo
   al sistema. Establecimiento
   bidireccional via Telephony.
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   entidad Call cuyo offer es aceptado.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session del agente que cambia state a busy + CallSession started.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica answer_inbound_calls.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent CALL_ANSWERED.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento (CNST-013/025).

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/operator/uc-opr-02/index` — Parte 1-12.
