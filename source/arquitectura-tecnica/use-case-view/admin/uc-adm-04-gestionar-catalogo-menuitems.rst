.. meta::
 :artefacto: AT_UC_ADM_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_adm_04_gestionar_catalogo_menuitems:

==============================================
UC_ADM_04 — Gestionar Catalogo de MenuItems
==============================================

UC v5.6.x extension. Administra el catalogo de ``MenuItem``
(wrapper UX 1:1 sobre ``Function``) — alta, edicion, listado.
Capability ``manage_menu_catalog`` con ``is_critical=True``
(bypass de cache, AP-2b). NO modifica estado del item (eso es
UC_ADM_05).

.. uml::
 :caption: UC_ADM_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_menu_catalog" as manage_menu_catalog
 actor "view_menu_catalog" as view_menu_catalog <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "FunctionRepo" as FunctionRepo <<sistema>>
 actor "MenuItemRepo" as MenuItemRepo <<sistema>>
 actor "UserCapabilityResolver" as UserCapabilityResolver <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_04\nGestionar Catalogo\nde MenuItems" as UC_ADM_04
   usecase "Verificar AGR-010\n(bypass cache AP-2b)" as VERIFICAR_AGR
   usecase "Validar Function\nactiva (I-1)" as VALIDAR_FN
   usecase "Validar I-1\n(Function sin\nMenuItem previo)" as VALIDAR_I1
   usecase "Validar parent\nNOT ARCHIVED" as VALIDAR_PARENT
   usecase "Validar jerarquia DAG\n(no ciclos)" as VALIDAR_DAG
   usecase "Persistir MenuItem\n(status=DRAFT default)" as PERSISTIR
   usecase "Invalidar cache\nmenu:user:{id}" as INVALIDAR
   usecase "Emitir AuditEvent\nMENU_ITEM_*" as AUDITAR
 }

 manage_menu_catalog --> UC_ADM_04
 view_menu_catalog --> UC_ADM_04

 UC_ADM_04 ..> VERIFICAR_AGR : <<include>>
 UC_ADM_04 ..> VALIDAR_FN : <<include>>
 UC_ADM_04 ..> VALIDAR_I1 : <<include>>
 UC_ADM_04 ..> VALIDAR_PARENT : <<include>>
 UC_ADM_04 ..> VALIDAR_DAG : <<extend>>
 UC_ADM_04 ..> PERSISTIR : <<include>>
 UC_ADM_04 ..> INVALIDAR : <<include>>
 UC_ADM_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VERIFICAR_AGR --> UserCapabilityResolver
 VALIDAR_FN --> FunctionRepo
 VALIDAR_I1 --> MenuItemRepo
 VALIDAR_PARENT --> MenuItemRepo
 PERSISTIR --> MenuItemRepo
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VERIFICAR_AGR
   AP-2b: is_critical=True
   fuerza consulta DB sin
   pasar por cache.
   Strong consistency.
 end note

 note bottom of VALIDAR_I1
   I-1: OneToOneField —
   Function tiene a lo sumo
   un MenuItem. Si ya tiene,
   responder 409 con
   existing_menu_item_id.
 end note

 note bottom of INVALIDAR
   Falla del Servicio de Cache
   no aborta el UC (degraded
   mode, ADR-BACK-009).
   Audit + telemetria.
 end note

 note bottom of AUDITAR
   MENU_ITEM_CREATED /
   UPDATED / BULK_REORDERED /
   CACHE_INVALIDATION_FAILED.
 end note

 @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/admin/uc-adm-04/index` — spec
   completa (12 partes).
 - :doc:`/arquitectura-tecnica/domain-model/menu-item` — entidad
   MenuItem persistida (v5.6.x extension).
 - :doc:`/arquitectura-tecnica/domain-model/menu-item-repo` —
   repositorio + queryset (visible, for_user).
 - :doc:`/arquitectura-tecnica/domain-model/function` — Function
   wrapped (con campo ``is_critical``).
 - :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver`
   — resolver con ``has_capability`` que decide cache vs DB.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada al cambiar catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de MENU_ITEM_*.
 - :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
 - :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
   v2.0.0.
