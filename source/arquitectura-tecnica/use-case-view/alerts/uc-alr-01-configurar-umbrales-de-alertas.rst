.. meta::
 :artefacto: AT_UC_ALR_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_alr_01_configurar_umbrales_de_alertas:

==================================================
UC_ALR_01 — Configurar Umbrales de Alertas
==================================================

Define ``AlertRule``: metric + scope + condition + window + severity +
actions. ``configure_team_alerts`` con CNST-008 isolation por segmento.
``AlertHook`` (evaluator continuo) recarga reglas activas tras cambio.

.. uml::
 :caption: UC_ALR_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "configure_team_alerts" as configure_team_alerts
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "AlertRule" as AlertRule <<sistema>>
 actor "Threshold" as Threshold <<sistema>>
 actor "AlertHook" as AlertHook <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales\nde Alertas" as UC_ALR_01
   usecase "Verificar\nconfigure_team_alerts" as VERIFICAR_AGR
   usecase "Validar metric\n(SL, abandon_rate, ...)" as VALIDAR_METRIC
   usecase "Validar scope ⊆\nsegmentos User (CNST-008)" as VALIDAR_SCOPE
   usecase "Validar window\n+ severity + actions" as VALIDAR_CONFIG
   usecase "Persistir AlertRule\n+ Threshold" as PERSISTIR
   usecase "Reload AlertHook\nconfig" as RELOAD
   usecase "Emitir AuditEvent\nALERT_RULE_*" as AUDITAR
 }

 configure_team_alerts --> UC_ALR_01

 UC_ALR_01 ..> VERIFICAR_AGR : <<include>>
 UC_ALR_01 ..> VALIDAR_METRIC : <<include>>
 UC_ALR_01 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_01 ..> VALIDAR_CONFIG : <<include>>
 UC_ALR_01 ..> PERSISTIR : <<include>>
 UC_ALR_01 ..> RELOAD : <<include>>
 UC_ALR_01 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_SCOPE --> SegmentResolver
 PERSISTIR --> AlertRule
 PERSISTIR --> Threshold
 RELOAD --> EvaluatorReloader
 RELOAD --> AlertHook
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_SCOPE
   CNST-008: scope debe estar
   en segmentos del User. No
   se puede crear regla
   cross-segment.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla persistida.
 - :doc:`/arquitectura-tecnica/domain-model/threshold` —
   umbral asociado.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   evaluator continuo.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   recarga config.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor.
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index` —
   spec textual.
