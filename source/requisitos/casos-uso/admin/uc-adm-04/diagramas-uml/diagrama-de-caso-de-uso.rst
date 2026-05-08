.. _uc-adm-04-parte-08-diagrama-caso-de-uso:

8.1 Diagrama de caso de uso
===========================

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
   usecase "Validar Function\nsin MenuItem previo" as VALIDAR_I1
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
   AP-2b: is_critical=True fuerza
   consulta DB sin pasar por cache.
   Strong consistency en cada request.
 end note

 note bottom of VALIDAR_I1
   I-1: OneToOneField — Function tiene
   a lo sumo un MenuItem. Si ya tiene,
   responder 409 con existing_menu_item_id.
 end note

 note bottom of INVALIDAR
   Falla del servicio de cache no
   aborta el UC (degraded mode).
   Audit + telemetria obligatoria.
 end note

 @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/admin/uc-adm-04/index` —
   spec completa.
 - :doc:`/arquitectura-tecnica/use-case-view/admin/uc-adm-04-gestionar-catalogo-menuitems`
   — uml-07 standalone equivalente.
 - :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
 - :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`.
