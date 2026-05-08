.. meta::
 :artefacto: AT_IMPL_MOD_ALERTS_INDEX
 :tipo: Diagrama Arquitectonico — Implementation View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_alerts_index:

============================================================
Implementation View — MOD_Alerts: Vista de Implementacion
============================================================

Caja del modulo **MOD_Alerts** en la vista de implementacion.
Muestra los componentes y paquetes de codigo del modulo
organizados en capas: ``<<api>>``, ``<<serializer>>``,
``<<service>>``, ``<<repository>>``, ``<<orm>>``, mas la
base de datos.

Definicion, evaluacion y notificacion de alertas sobre metricas. Cubre AlertRule, evaluacion periodica, generacion de Alert y suscripciones.

Materializa los UCs UC_ALR_01..05 documentados en
:doc:`/arquitectura-tecnica/use-case-view/alerts/index` con
la estructura de diseño definida en
:doc:`/arquitectura-tecnica/design-view/alerts/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Alerts — capas del modulo en alto nivel.
           Detalle de componentes especificos en
           :doc:`layer-structure`.

 @startuml

 package "MOD_Alerts" {
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
   Evalua AlertRule contra Metric en ventanas configurables.
   EvaluatorReloader recarga reglas activas sin reiniciar.
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

 - :doc:`/arquitectura-tecnica/use-case-view/alerts/index` —
   UCs del modulo.
 - :doc:`/arquitectura-tecnica/design-view/alerts/index` —
   estructura de diseño del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   raiz de ImplementationView.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/alert` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/subscription` —
   clase canonica.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   clase canonica.