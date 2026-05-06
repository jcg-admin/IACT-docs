.. meta::
 :artefacto: AT_UC_OPR_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Reservado
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_opr_03_realizar_llamada_saliente:

============================================================
UC_OPR_03 — Realizar Llamada Saliente
============================================================

Agente inicia llamada a cliente desde campana o callback solicitado.
Modos: manual, preview, auto-dial. AntiFraud check obligatorio (lista
permitida). ``initiate_outbound_call``. P-15.

.. uml::
 :caption: UC_OPR_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "initiate_outbound_call" as initiate_outbound_call
 actor "Caller (target)" as Caller <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "Campaign" as Campaign <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_03\nRealizar Llamada\nSaliente" as UC_OPR_03
   usecase "Verificar\ninitiate_outbound_call" as VERIFICAR_AGR
   usecase "Validar mode\n(manual | preview | auto)" as VALIDAR_MODE
   usecase "Verificar AntiFraud\n(lista permitida)" as VERIFY_AF
   usecase "Asociar campaign_id\no callback_id" as ASOCIAR
   usecase "Iniciar Call outbound" as INICIAR
   usecase "Emitir AuditEvent\nOUTBOUND_INITIATED" as AUDITAR
 }

 initiate_outbound_call --> UC_OPR_03

 UC_OPR_03 ..> VERIFICAR_AGR : <<include>>
 UC_OPR_03 ..> VALIDAR_MODE : <<include>>
 UC_OPR_03 ..> VERIFY_AF : <<include>>
 UC_OPR_03 ..> ASOCIAR : <<include>>
 UC_OPR_03 ..> INICIAR : <<include>>
 UC_OPR_03 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VERIFY_AF --> RuleValidator
 ASOCIAR --> Campaign
 INICIAR --> Call
 INICIAR --> Caller
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFY_AF
   Politica anti-fraud: numero NO en
   lista permitida → bloqueado.
   CNST-009/013/025.
 end note

 note bottom of VALIDAR_MODE
   Modes: manual (agente teclea),
   preview (agente acepta),
   auto (sistema marca y asigna).
   DispatchModeStrategy.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con type=outbound + mode.
 - :doc:`/arquitectura-tecnica/domain-model/campaign` —
   Campaign asociada (anti-fraud whitelist).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   anti-fraud validation.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   DispatchModeStrategy.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-03/index` —
   spec textual.
