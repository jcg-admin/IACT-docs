.. meta::
 :artefacto: AT_UC_PERM_08_USECASE
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

.. _at_uc_perm_08_generar_menu_dinamico:

==========================================
UC_PERM_08 — Generar Menu Dinamico
==========================================

Genera el menu de navegacion personalizado para el User segun su
``effective_set`` de funciones. Cada nodo del menu (Domain → Section →
Action) se filtra por las funciones que el User posee. Funcion implicita
``view_own_navigation`` (auto-otorgada a usuarios autenticados).

.. uml::
 :caption: UC_PERM_08 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_own_navigation" as view_own_navigation
 actor "PermissionService" as PermissionService <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "NavDomain" as NavDomain <<sistema>>
 actor "Menu" as Menu <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_08\nGenerar Menu Dinamico" as UC_PERM_08
   usecase "Cargar effective_set\ndel User" as LOAD_EFFECTIVE
   usecase "Cargar arbol NavDomain\n(catalogo de menu)" as LOAD_NAV
   usecase "Filtrar nodos por\nfunciones disponibles" as FILTRAR
   usecase "Construir Menu\n(Domain → Section → Action)" as CONSTRUIR
   usecase "Cache lookup TTL corto" as CACHE_LOOKUP
 }

 view_own_navigation --> UC_PERM_08

 UC_PERM_08 ..> CACHE_LOOKUP : <<include>>
 UC_PERM_08 ..> LOAD_EFFECTIVE : <<include>>
 UC_PERM_08 ..> LOAD_NAV : <<include>>
 UC_PERM_08 ..> FILTRAR : <<include>>
 UC_PERM_08 ..> CONSTRUIR : <<include>>

 LOAD_EFFECTIVE --> PermissionService
 LOAD_EFFECTIVE --> PermissionCache
 LOAD_NAV --> NavDomain
 CONSTRUIR --> Menu

 note bottom of UC_PERM_08
   GET /api/me/menu/ — cada User
   ve su menu segun su effective_set.
   Sin RBAC explicito (auto a
   usuarios autenticados).
 end note

 note bottom of FILTRAR
   Menu filter respeta P-15:
   nodo visible solo si User tiene
   AL MENOS UNA funcion del nodo.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/menu` —
   Menu generado por User.
 - :doc:`/arquitectura-tecnica/domain-model/nav-domain` —
   catalogo de nodos del menu.
 - :doc:`/arquitectura-tecnica/domain-model/section` —
   nodos intermedios del menu.
 - :doc:`/arquitectura-tecnica/domain-model/action` —
   acciones (hojas del menu).
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   provee effective_set.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache TTL corto.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index` —
   spec textual.
