.. meta::
 :artefacto: AT_UC_PERM_05_USECASE
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

.. _at_uc_perm_05_crear_grupo_de_permisos:

========================================
UC_PERM_05 — Crear/Modificar/Retirar AGR
========================================

Gestiona ciclo de vida de **AGRs custom** (``is_system=False``) — los
12 AGRs del sistema (AGR-001..012) son inmutables salvo via UC_ADM_03.
3 sub-flujos: crear nuevo AGR, modificar metadata (no composicion —
eso es UC_PERM_06), retirar (state=DEPRECATED).

.. uml::
 :caption: UC_PERM_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "create_function_group" as create_function_group
 actor "update_function_group" as update_function_group
 actor "deprecate_function_group" as deprecate_function_group
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AccessGroupRepo" as AccessGroupRepo <<sistema>>
 actor "FunctionGroupRepo" as FunctionGroupRepo <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_05\nCrear/Modificar/\nRetirar AGR custom" as UC_PERM_05
   usecase "Verificar funcion\nsegun sub-flujo" as VERIFICAR_AGR
   usecase "Validar code unico" as VALIDAR_CODE
   usecase "Validar is_system=False" as VERIFICAR_CUSTOM
   usecase "Persistir AccessGroup" as PERSISTIR_AG
   usecase "Persistir composicion\ninicial (FunctionGroup)" as PERSISTIR_FG
   usecase "Recargar catalogo" as RELOAD
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nAGR_CREATED / UPDATED / DEPRECATED" as AUDITAR
 }

 create_function_group --> UC_PERM_05
 update_function_group --> UC_PERM_05
 deprecate_function_group --> UC_PERM_05

 UC_PERM_05 ..> VERIFICAR_AGR : <<include>>
 UC_PERM_05 ..> VALIDAR_CODE : <<include>>
 UC_PERM_05 ..> VERIFICAR_CUSTOM : <<include>>
 UC_PERM_05 ..> PERSISTIR_AG : <<include>>
 UC_PERM_05 ..> PERSISTIR_FG : <<include>>
 UC_PERM_05 ..> RELOAD : <<include>>
 UC_PERM_05 ..> INVALIDAR : <<include>>
 UC_PERM_05 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_CODE --> AccessGroupRepo
 PERSISTIR_AG --> AccessGroupRepo
 PERSISTIR_FG --> FunctionGroupRepo
 RELOAD --> EvaluatorReloader
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFICAR_CUSTOM
   UC_PERM_05 solo opera sobre AGRs
   custom (is_system=False).
   AGR-001..012 = UC_ADM_03.
 end note

 note bottom of UC_PERM_05
   3 sub-flujos: crear (POST),
   modificar metadata (PATCH),
   retirar (state=DEPRECATED).
   Composicion: ver UC_PERM_06.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroup custom.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/function-group` —
   FunctionGroup composicion.
 - :doc:`/arquitectura-tecnica/domain-model/function-group-repo` —
   repositorio composicion.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   recarga catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica funciones por sub-flujo.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor AGR_*.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index` —
   spec textual.
