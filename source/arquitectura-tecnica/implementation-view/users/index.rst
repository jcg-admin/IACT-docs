.. meta::
 :artefacto: AT_IMPL_MOD_USERS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_users_index:

============================================================
Implementation View — MOD_Users: Vista de Implementacion
============================================================

Caja del modulo **MOD_Users** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Gestion de usuarios. Cubre el ciclo de vida del User: creacion con onboarding, modificacion administrativa, edicion self-service, baja logica, bloqueo, desbloqueo.

Materializa los UCs UC_USR_01..07 documentados en
:doc:`/arquitectura-tecnica/use-case-view/users/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/users/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Users — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Users" {
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
   UserOnboardingService orquesta provisioning completo (UC_USR_01).
   UserRepo aplica BR-009 (bajas logicas, no DELETE fisico).
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

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/users/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/users/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver` —
   clase canonica.