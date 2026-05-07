.. _uc-adm-03-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "view_system_groups" as view_system_groups <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AccessGroupRepo" as AccessGroupRepo <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "FunctionGroupRepo" as FunctionGroupRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_03\nGestionar Catalogo\nde Agrupadores del Sistema" as UC_ADM_03
   usecase "Verificar capability\n(AGR-010)" as VERIFICAR_CAP
   usecase "Verificar AccessGroup\nis_system=True" as VERIFICAR_SISTEMA
   usecase "Verificar Function\nen catalogo activo" as VERIFICAR_FN
   usecase "Validar SoD precheck\n(BR-007)" as VALIDAR_SOD
   usecase "Persistir\nFunctionGroupMembership" as PERSISTIR
   usecase "Calcular impacto\n(preview)" as PREVIEW
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "EvaluatorReloader\n.recalculate()" as RELOAD
   usecase "Emitir AuditEvent\nAGR_*" as AUDITAR
 }

 assign_functions_to_group --> UC_ADM_03
 view_system_groups --> UC_ADM_03

 UC_ADM_03 ..> VERIFICAR_CAP : <<include>>
 UC_ADM_03 ..> VERIFICAR_SISTEMA : <<include>>
 UC_ADM_03 ..> VERIFICAR_FN : <<include>>
 UC_ADM_03 ..> VALIDAR_SOD : <<include>>
 UC_ADM_03 ..> PERSISTIR : <<include>>
 UC_ADM_03 ..> PREVIEW : <<extend>>
 UC_ADM_03 ..> INVALIDAR : <<include>>
 UC_ADM_03 ..> RELOAD : <<include>>
 UC_ADM_03 ..> AUDITAR : <<include>>

 VERIFICAR_CAP --> AuthorizationGuard
 VERIFICAR_SISTEMA --> AccessGroupRepo
 VERIFICAR_FN --> FunctionRepo
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> FunctionGroupRepo
 INVALIDAR --> PermissionCache
 RELOAD --> EvaluatorReloader
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFICAR_SISTEMA
   AGR-001..010 (predefinidos del
   sistema, is_system=True). Para
   AGRs custom (is_system=False)
   usar UC_PERM_06.
 end note

 note bottom of VALIDAR_SOD
   BR-007: la nueva Function no
   debe violar ninguna regla SoD
   activa con las Functions ya
   asignadas al AGR.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group`.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/function-group`.
 - :doc:`/arquitectura-tecnica/domain-model/function-group-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
