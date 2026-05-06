8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "create_separation_rule" as F_CREATE
 actor "update_separation_rule" as F_UPDATE
 actor "disable_separation_rule" as F_DISABLE
 actor "view_separation_rules" as F_VIEW <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "EvaluatorReloader" as EE <<sistema>>
 actor "RuleValidator" as RV <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nGestionar Ciclo de Vida\nde Reglas SoD" as UC_ADM_01
   usecase "Validar conjuntos\ndisjuntos (CNST-030)" as VALIDAR_CONJUNTOS
   usecase "Validar funciones\nen catalogo activo\n(UC_ADM_02)" as VALIDAR_FUNCIONES
   usecase "Validar nombre\nunico" as VALIDAR_NOMBRE
   usecase "Persistir SeparationRule\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nSOD_RULE_*" as AUDIT
   usecase "EvaluatorReloader\n.reload()" as RELOAD
 }

 F_CREATE --> UC_ADM_01
 F_UPDATE --> UC_ADM_01
 F_DISABLE --> UC_ADM_01
 F_VIEW --> UC_ADM_01

 UC_ADM_01 ..> VALIDAR_CONJUNTOS : <<include>>
 UC_ADM_01 ..> VALIDAR_FUNCIONES : <<include>>
 UC_ADM_01 ..> VALIDAR_NOMBRE : <<include>>
 UC_ADM_01 ..> PERSISTIR : <<include>>
 UC_ADM_01 ..> AUDIT : <<include>>
 UC_ADM_01 ..> RELOAD : <<include>>

 VALIDAR_CONJUNTOS --> RV
 VALIDAR_FUNCIONES --> RV
 AUDIT --> AS
 RELOAD --> EE
 AS --> view_audit_log

 note bottom of VALIDAR_CONJUNTOS
   CNST-030: group_a y group_b
   disjuntos (sin interseccion)
   en create y update.
 end note

 note bottom of AUDIT
   SOD_RULE_CREATED / UPDATED /
   DISABLED. CNST-025 alta
   criticidad — cambios al
   modelo RBAC.
 end note

 note right of F_VIEW
   AGR-010 system_admin agrupa
   las 4 funciones. view_separation_rules
   es read-only y se reutiliza desde
   UC_ACC_05.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   entidad SeparationRule (CNST-030, persistida por este UC).
 - :doc:`/arquitectura-tecnica/domain-model/function` — catalogo
   de funciones validado por VALIDAR_FUNCIONES (UC_ADM_02 backing).
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   componente que ejecuta VALIDAR_CONJUNTOS / VALIDAR_FUNCIONES.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   notificado en RELOAD para refrescar reglas activas.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent SOD_RULE_*.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento emitido (CNST-025).
