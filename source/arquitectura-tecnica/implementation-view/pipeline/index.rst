.. meta::
 :artefacto: AT_IMPL_MOD_PIPELINE_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_pipeline_index:

============================================================
Implementation View — MOD_Pipeline: Vista de Implementacion
============================================================

Caja del modulo **MOD_Pipeline** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Orquestacion del ETL nocturno desde el sistema operacional IVR hacia el Almacen analitico. Cubre extract-transform-load, errores, reintentos y supervision.

Materializa los UCs UC_PIP_01..04 documentados en
:doc:`/arquitectura-tecnica/use-case-view/pipeline/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/pipeline/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Pipeline — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Pipeline" {
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
   DisparadorETL lanza el ETL nocturno (BR-002 02:00 AM).
   Metric producido se publica incrementalmente al MetricsCache.
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

 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/disparador-etl` —
   clase canonica.