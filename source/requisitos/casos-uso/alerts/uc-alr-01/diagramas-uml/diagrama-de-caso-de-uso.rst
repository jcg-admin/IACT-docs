8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "configure_team_alerts" as INVOKER
 actor "AlertRule" as AR <<sistema>>
 actor "AlertHook" as AH <<sistema>>
 actor "EvaluatorReloader" as ER <<sistema>>
 actor "AuditService" as AS <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar\nUmbrales de Alertas" as UC_ALR_01
   usecase "Validar metric\n(SL, abandon_rate, ...)" as VALIDAR_METRIC
   usecase "Validar scope\n(segment | queue | campaign)" as VALIDAR_SCOPE
   usecase "Validar window\n+ severity" as VALIDAR_WINDOW
   usecase "Persistir AlertRule\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nALERT_RULE_*" as AUDIT
   usecase "Reloader.reload()\n(propagar a evaluator)" as RELOAD
 }

 INVOKER --> UC_ALR_01
 UC_ALR_01 ..> VALIDAR_METRIC : <<include>>
 UC_ALR_01 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_01 ..> VALIDAR_WINDOW : <<include>>
 UC_ALR_01 ..> PERSISTIR : <<include>>
 UC_ALR_01 ..> AUDIT : <<include>>
 UC_ALR_01 ..> RELOAD : <<include>>

 PERSISTIR --> AR
 RELOAD --> ER
 RELOAD --> AH
 AUDIT --> AS
 AS --> view_audit_log

 note bottom of VALIDAR_SCOPE
   CNST-008: scope debe estar en
   segmentos asignados al User.
   No se puede crear regla cross-segment.
 end note

 note right of AH
   AlertHook consume reglas activas y
   dispara alertas cuando metricas
   cruzan umbral en window definido.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   AlertRule persistida (metric, scope, condition, window).
 - :doc:`/arquitectura-tecnica/domain-model/threshold` —
   threshold definido en condition.
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
   evaluador continuo que consume reglas activas.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   coordinador del reload de configuracion.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent ALERT_RULE_*.
