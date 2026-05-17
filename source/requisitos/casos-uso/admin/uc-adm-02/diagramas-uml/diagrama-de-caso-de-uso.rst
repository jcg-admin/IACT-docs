.. _uc-adm-02-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_function_catalog" as manage_function_catalog
 actor "view_functions" as view_functions <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "PermissionService" as PermissionService <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_02\nGestionar Catalogo\nde Funciones" as UC_ADM_02
   usecase "Verificar capability" as VERIFICAR_CAP
   usecase "Validar codename unico\n(snake_case STD-008)" as VALIDAR_CODENAME
   usecase "Validar module valido" as VALIDAR_MODULE
   usecase "Validar scope" as VALIDAR_SCOPE
   usecase "Persistir Function\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nFUNCTION_*" as AUDITAR
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "EvaluatorReloader\n.reload_catalog()" as RELOAD
 }

 manage_function_catalog --> UC_ADM_02
 view_functions --> UC_ADM_02

 UC_ADM_02 ..> VERIFICAR_CAP : <<include>>
 UC_ADM_02 ..> VALIDAR_CODENAME : <<include>>
 UC_ADM_02 ..> VALIDAR_MODULE : <<include>>
 UC_ADM_02 ..> VALIDAR_SCOPE : <<include>>
 UC_ADM_02 ..> PERSISTIR : <<include>>
 UC_ADM_02 ..> AUDITAR : <<include>>
 UC_ADM_02 ..> INVALIDAR : <<include>>
 UC_ADM_02 ..> RELOAD : <<include>>

 VERIFICAR_CAP --> AuthorizationGuard
 PERSISTIR --> FunctionRepo
 AUDITAR --> AuditService
 INVALIDAR --> PermissionCache
 RELOAD --> EvaluatorReloader
 RELOAD --> PermissionService
 AuditService --> view_audit_log

 note bottom of VALIDAR_CODENAME
   STD-008: snake_case obligatorio.
   Codename inmutable tras creacion.
 end note

 note bottom of AUDITAR
   FUNCTION_CREATED / UPDATED /
   DEACTIVATED. No modifica
   is_critical (gobernanza separada,
   ADR-BACK-010).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function`.
 - :doc:`/arquitectura-tecnica/domain-model/function-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
 - :doc:`/backend/adr-back-010-function-is-critical-governance`.
