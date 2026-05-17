.. meta::
 :artefacto: AT_IMPL_MOD_AUTH_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_auth_index:

============================================================
Implementation View — MOD_Auth: Vista de Implementacion
============================================================

Caja del modulo **MOD_Auth** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Autenticacion, gestion de sesiones y gateway de autorizacion runtime. Cubre login, logout, recuperacion/cambio de password, ciclo de vida de Session, verificacion de capabilities.

Materializa los UCs UC_AUTH_01..05 documentados en
:doc:`/arquitectura-tecnica/use-case-view/auth/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/auth/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Auth — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Auth" {
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
   AuthorizationGuard verifica session vigente y capability en cada request.
   BlacklistedToken invalida tokens revocados.
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
 jwt-token-lifecycle

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/auth/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/auth/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   clase canonica.