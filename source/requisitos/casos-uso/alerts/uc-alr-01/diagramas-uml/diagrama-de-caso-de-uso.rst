8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "configure_team_alerts" as INVOKER
 actor "AlertEvaluator" as EVALUATOR <<sistema>>
 actor "AlertRuleRepo" as REPO <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar\nUmbrales de Alertas" as UC_ALR_01
   usecase "Validar metric\n(SL, abandon_rate, ...)" as VALIDAR_METRIC
   usecase "Validar scope\n(segment | queue | campaign)" as VALIDAR_SCOPE
   usecase "Validar window\n+ severity" as VALIDAR_WINDOW
   usecase "Persistir AlertRule\n(BR-009 baja logica)" as PERSISTIR
   usecase "AuditEvent\nALERT_RULE_*" as AUDIT
   usecase "AlertEvaluator\n.reload_config()" as RELOAD
 }

 INVOKER --> UC_ALR_01
 UC_ALR_01 ..> VALIDAR_METRIC : <<include>>
 UC_ALR_01 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_01 ..> VALIDAR_WINDOW : <<include>>
 UC_ALR_01 ..> PERSISTIR : <<include>>
 UC_ALR_01 ..> AUDIT : <<include>>
 UC_ALR_01 ..> RELOAD : <<include>>

 PERSISTIR --> REPO
 RELOAD --> EVALUATOR
 Sistema --> AUDIT
 AUDIT --> view_audit_log

 note bottom of VALIDAR_SCOPE
   CNST-008: scope debe estar en
   segmentos asignados al User.
   No se puede crear regla cross-segment.
 end note

 note right of EVALUATOR
   AlertEvaluator es UC interno —
   consume reglas activas y dispara
   alertas cuando metricas cruzan
   umbral en window definido.
 end note

 @enduml
