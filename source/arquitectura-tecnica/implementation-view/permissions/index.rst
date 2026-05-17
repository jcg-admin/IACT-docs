.. meta::
 :artefacto: AT_IMPL_MOD_PERMISSIONS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_permissions_index:

================================================================
Implementation View — MOD_Permissions: Vista de Implementacion
================================================================

Caja del modulo **MOD_Permissions** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Resolucion runtime de permisos efectivos. Calcula effective_set combinando Assignment regulares + ExceptionalPermission ad-hoc + cache.

Materializa los UCs UC_PERM_01..10 documentados en
:doc:`/arquitectura-tecnica/use-case-view/permissions/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/permissions/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Permissions — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Permissions" {
   component "API endpoints" <<api>>
   component "Service layer" <<service>>
   component "Repository layer" <<repository>>
   component "ORM mapping" <<orm>>
 }

 database "Almacen de Datos" as DB

 [API endpoints] --> [Service layer]
 [Service layer] --> [Repository layer]
 [Repository layer] --> [ORM mapping]
 [ORM mapping] --> DB

 note right of [Service layer]
   EffectivePermissionsAggregator combina dos fuentes (regulares + excepcionales).
   PermissionCache evita re-calculo en gateway checks de alta frecuencia.
   Componentes especificos en :doc:`layer-structure`.
 end note

 @enduml

Lectura del diagrama
====================

- **API endpoints** exponen las operaciones del modulo.
- **Service layer** orquesta la logica del bounded context.
- **Repository layer** abstrae acceso al Almacen de Datos.
- **ORM mapping** traduce los modelos del dominio.
- El detalle de componentes especificos (con sus nombres
  de clase reales) vive en :doc:`layer-structure`.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo

 layer-structure
 interaction-pattern
 effective-set-cache-pattern

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/permissions/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/permissions/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/rbac-repo` —
   clase canonica.