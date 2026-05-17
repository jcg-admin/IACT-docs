.. meta::
 :artefacto: AT_IMPL_MOD_AUDIT_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_audit_index:

============================================================
Implementation View — MOD_Audit: Vista de Implementacion
============================================================

Caja del modulo **MOD_Audit** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Registro inmutable y consulta de eventos de seguridad (AuditEvent). Cubre emision, consulta paginada y reportes de compliance.

Materializa los UCs UC_AUD_01..04 documentados en
:doc:`/arquitectura-tecnica/use-case-view/audit/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/audit/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Audit — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Audit" {
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
   AuditService sanitiza payload via PIIScanner (CNST-026) antes de persistir.
   AuditEvent es inmutable per CNST-025.
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
 audit-capture-middleware-pattern

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/audit/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/audit/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   clase canonica.