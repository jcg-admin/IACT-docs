.. meta::
 :artefacto: AT_IMPL_MOD_REPORTS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_reports_index:

============================================================
Implementation View — MOD_Reports: Vista de Implementacion
============================================================

Caja del modulo **MOD_Reports** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Dashboards, reportes historicos, vistas guardadas, programadas y exportes asincronos. Cubre la jerarquia de servicios de reportes y export jobs.

Materializa los UCs UC_RPT_01..17 + UC_INC_RPT_01 documentados en
:doc:`/arquitectura-tecnica/use-case-view/reports/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/reports/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Reports — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Reports" {
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
   ReportTypeRegistry resuelve el tipo de reporte (renombrado en WP-H desde ReportFactory).
   ExportJob orquesta exportes pesados de forma asincrona.
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
 async-export-worker-pattern

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/reports/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/reports/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/report` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/saved-view` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   clase canonica.