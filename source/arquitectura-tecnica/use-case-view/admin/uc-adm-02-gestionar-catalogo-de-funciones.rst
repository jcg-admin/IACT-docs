.. meta::
 :artefacto: AT_UC_ADM_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_adm_02_gestionar_catalogo_de_funciones:

==============================================
UC_ADM_02 — Gestionar Catalogo de Funciones
==============================================

Administra el catalogo de **funciones atomicas** del sistema RBAC.
74+ funciones actuales se administran via migraciones Django; este UC
formaliza la capacidad UI para crear, actualizar metadata, desactivar
y consultar funciones sin redespliegue. P-44 codename inmutable tras
creacion. PermissionsEngine recarga catalogo activo al cambio.

.. uml::
 :caption: UC_ADM_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "create_function" as create_function
 actor "update_function" as update_function
 actor "deactivate_function" as deactivate_function
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
   usecase "Verificar AGR-010" as VERIFICAR_AGR
   usecase "Validar codename\nunico (snake_case)" as VALIDAR_CODENAME
   usecase "Validar module valido\n(MOD_Auth, MOD_RBAC, ...)" as VALIDAR_MODULE
   usecase "Validar scope" as VALIDAR_SCOPE
   usecase "Persistir Function\n(BR-009 baja logica)" as PERSISTIR
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "EvaluatorReloader\n.reload_catalog()" as RELOAD
   usecase "Emitir AuditEvent\nFUNCTION_*" as AUDITAR
 }

 create_function --> UC_ADM_02
 update_function --> UC_ADM_02
 deactivate_function --> UC_ADM_02
 view_functions --> UC_ADM_02

 UC_ADM_02 ..> VERIFICAR_AGR : <<include>>
 UC_ADM_02 ..> VALIDAR_CODENAME : <<include>>
 UC_ADM_02 ..> VALIDAR_MODULE : <<include>>
 UC_ADM_02 ..> VALIDAR_SCOPE : <<include>>
 UC_ADM_02 ..> PERSISTIR : <<include>>
 UC_ADM_02 ..> INVALIDAR : <<include>>
 UC_ADM_02 ..> RELOAD : <<include>>
 UC_ADM_02 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 PERSISTIR --> FunctionRepo
 INVALIDAR --> PermissionCache
 RELOAD --> EvaluatorReloader
 RELOAD --> PermissionService
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_CODENAME
   P-44: codename inmutable tras
   creacion. update solo modifica
   description, scope, is_active.
 end note

 note bottom of AUDITAR
   FUNCTION_CREATED / UPDATED /
   DEACTIVATED. CNST-025 alta
   criticidad — define catalogo RBAC.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function` —
   Function entity persistida.
 - :doc:`/arquitectura-tecnica/domain-model/function-repo` —
   repositorio CRUD del catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/function-group` —
   FunctionGroup que consume catalogo activo (UC_ADM_03).
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   consume catalogo activo en runtime.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada al cambiar catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   notificado para refrescar catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica AGR-010.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de FUNCTION_*.
 - :doc:`/requisitos/casos-uso/admin/uc-adm-02/index` — Parte 1-12.
