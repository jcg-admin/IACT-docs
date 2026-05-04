.. meta::
 :artefacto: INDEX_AT_UC_USECASEVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-usecaseview-index:

=====================================
Use Case View — Vista de Casos de Uso
=====================================

Diagramas de casos de uso a nivel módulo, con actores RBAC, relaciones
``<<include>>`` y ``<<extend>>``. Cada archivo cubre un módulo funcional
del sistema IACT con sus UCs agrupados por actor principal.

El sistema IACT tiene 80 UCs distribuidos en 13 módulos. Esta vista
usa granularidad módulo: un diagrama canónico por módulo, no uno por UC.

.. toctree::
 :maxdepth: 1
 :caption: Módulos

 mod-auth
 mod-users
 mod-access
 mod-permissions
 mod-reports
 mod-alerts
 mod-pipeline
 mod-audit
 mod-logs
 mod-operator
 mod-supervision
 mod-caller
 mod-admin
