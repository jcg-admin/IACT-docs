.. _uc-adm-01-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "create_separation_rule" as create_separation_rule
 actor "update_separation_rule" as update_separation_rule
 actor "disable_separation_rule" as disable_separation_rule
 actor "view_separation_rules" as view_separation_rules <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "AuditService" as AuditService <<sistema>>
 actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nGestionar Ciclo de Vida\nde Reglas SoD" as UC_ADM_01
   usecase "Validar conjuntos\ndisjuntos (CNST-030)" as VALIDAR_CONJUNTOS
   usecase "Validar funciones\nen catalogo activo" as VALIDAR_FUNCIONES
   usecase "Validar nombre\nunico" as VALIDAR_NOMBRE
   usecase "Persistir SeparationRule\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nSOD_RULE_*" as AUDITAR
   usecase "EvaluatorReloader\n.reload()" as RELOAD
 }

 create_separation_rule --> UC_ADM_01
 update_separation_rule --> UC_ADM_01
 disable_separation_rule --> UC_ADM_01
 view_separation_rules --> UC_ADM_01

 UC_ADM_01 ..> VALIDAR_CONJUNTOS : <<include>>
 UC_ADM_01 ..> VALIDAR_FUNCIONES : <<include>>
 UC_ADM_01 ..> VALIDAR_NOMBRE : <<include>>
 UC_ADM_01 ..> PERSISTIR : <<include>>
 UC_ADM_01 ..> AUDITAR : <<include>>
 UC_ADM_01 ..> RELOAD : <<include>>

 VALIDAR_CONJUNTOS --> RuleValidator
 VALIDAR_FUNCIONES --> RuleValidator
 VALIDAR_FUNCIONES --> FunctionRepo
 PERSISTIR --> SeparationRuleRepo
 AUDITAR --> AuditService
 RELOAD --> EvaluatorReloader
 AuditService --> view_audit_log

 note bottom of VALIDAR_CONJUNTOS
   CNST-030: group_a y group_b
   disjuntos (sin interseccion)
   en create y update.
 end note

 note bottom of AUDITAR
   SOD_RULE_CREATED / UPDATED /
   DISABLED. CNST-025 alta
   criticidad — cambios al
   modelo RBAC.
 end note

 @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
   spec completa.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
