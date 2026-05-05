.. meta::
 :artefacto: AT_UC_PERM_06_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_perm_06_asignar_funciones_a_grupo:

================================================
UC_PERM_06 — Asignar Funciones a Grupo
================================================

Modifica composicion de un AGR custom: agrega o quita ``Function``
del ``FunctionGroup``. Cambio dispara recompute en cascada del
effective_set de TODOS los Users con AGR asignado. Validacion SoD
write-time previene violaciones (CNST-005). Para AGR del sistema
(AGR-001..012), usar UC_ADM_03.

.. uml::
 :caption: UC_PERM_06 — actores y casos asociados.

 @startuml

 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FunctionGroupRepo" as FunctionGroupRepo <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "RuleValidator" as RuleValidator <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_06\nAsignar Funciones\na Grupo (custom)\n.. extension points ..\nPreviewSoDCascade" as UC_PERM_06
   usecase "Verificar\nassign_functions_to_group" as VERIFICAR_AGR
   usecase "Validar AGR custom\n(is_system=False)" as VERIFICAR_CUSTOM
   usecase "Validar funciones\nen catalogo activo" as VALIDAR_FUNCION
   usecase "Validar SoD cascade\n(Users con AGR)" as VALIDAR_SOD
   usecase "Validar idempotencia" as IDEMP
   usecase "Persistir cambios\nFunctionGroup" as PERSISTIR
   usecase "Recompute cascade" as RECALC
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nAGR_FUNCTION_ADDED/REMOVED" as AUDITAR
   usecase "Preview SoD cascade\n(simulacion)" as PREVIEW
 }

 assign_functions_to_group --> UC_PERM_06

 UC_PERM_06 ..> VERIFICAR_AGR : <<include>>
 UC_PERM_06 ..> VERIFICAR_CUSTOM : <<include>>
 UC_PERM_06 ..> VALIDAR_FUNCION : <<include>>
 UC_PERM_06 ..> VALIDAR_SOD : <<include>>
 UC_PERM_06 ..> IDEMP : <<include>>
 UC_PERM_06 ..> PERSISTIR : <<include>>
 UC_PERM_06 ..> RECALC : <<include>>
 UC_PERM_06 ..> INVALIDAR : <<include>>
 UC_PERM_06 ..> AUDITAR : <<include>>
 PREVIEW ..> UC_PERM_06 : <<extend>> (PreviewSoDCascade)

 VERIFICAR_AGR --> AuthorizationGuard
 VERIFICAR_CUSTOM --> FunctionGroupRepo
 VALIDAR_FUNCION --> FunctionRepo
 VALIDAR_SOD --> RuleValidator
 PERSISTIR --> FunctionGroupRepo
 RECALC --> EffectivePermissionsAggregator
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_SOD
   BR-007 + CNST-005: agregar funcion
   no debe romper SoD de Users que ya
   tienen el AGR.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function-group` —
   composicion modificada.
 - :doc:`/arquitectura-tecnica/domain-model/function-group-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   tabla M:N.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   funciones validadas.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   reglas SoD.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator` —
   ejecuta SoD cascade.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   recompute cascade.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index` —
   spec textual.
