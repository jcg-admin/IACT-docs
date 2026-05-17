.. meta::
 :artefacto: AT_IMPL_MOD_ACCESS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_access_index:

============================================================
Implementation View — MOD_Access: Vista de Implementacion
============================================================

Caja del modulo **MOD_Access** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Materializa los UCs UC_ACC_01..09 documentados en
:doc:`/arquitectura-tecnica/use-case-view/access/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/access/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Access — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Access" {
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
   Coordina verificacion de SeparationRule
   antes de cualquier cambio en Assignment.
   CNST-030 enforcement en tiempo de asignacion.
   Componentes especificos en :doc:`layer-structure`.
 end note

 @enduml

Lectura del diagrama
====================

- **API endpoints** exponen las operaciones del modulo
  (asignar/revocar funciones, consultar permisos efectivos,
  gestionar reglas de separacion).
- **Service layer** orquesta la logica del bounded context
  RBAC: verifica separation-of-duties antes de mutar
  asignaciones, emite AuditEvents.
- **Repository layer** abstrae acceso al Almacen de Datos
  para entidades del modulo (Assignment, SeparationRule,
  AccessGroup).
- **ORM mapping** traduce los modelos del dominio a
  representacion persistida.
- El detalle de componentes especificos (con sus nombres
  de clase reales) vive en :doc:`layer-structure`.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo

 layer-structure
 interaction-pattern
 rbac-enforcement-pattern

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/access/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/access/index` —
   estructura de diseño del modulo (clases, secuencias,
   ciclo de vida).
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/assignment` —
   entidad central.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   entidad de separation-of-duties.
