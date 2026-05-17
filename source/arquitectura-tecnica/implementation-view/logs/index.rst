.. meta::
 :artefacto: AT_IMPL_MOD_LOGS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_logs_index:

============================================================
Implementation View — MOD_Logs: Vista de Implementacion
============================================================

Caja del modulo **MOD_Logs** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Consulta de logs operacionales, infraestructura y metricas tecnicas. Cubre queries con filtros, paginacion y calculo de KPIs.

Materializa los UCs UC_LOG_01..07 documentados en
:doc:`/arquitectura-tecnica/use-case-view/logs/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/logs/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Logs — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Logs" {
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
   AuditQueryService reutilizado del modulo Audit provee la maquinaria de query.
   KpiCalculator agrega TechnicalMetric a percentiles (p95/p99).
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

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/logs/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/logs/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/application-log` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric` —
   clase canonica.