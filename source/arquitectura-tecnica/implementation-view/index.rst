.. meta::
 :artefacto: INDEX_AT_IMPLEMENTATIONVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-implementationview-index:

=============================================
Implementation View — Vista de Implementacion
=============================================

Componentes y paquetes de codigo del sistema IACT por modulo funcional.
Cada archivo muestra el diagrama canonico del modulo: capas reales
(``<<api>>``, ``<<serializer>>``, ``<<service>>``, ``<<repository>>``,
``<<orm>>``) con nombres de clases y servicios del codigo fuente, mas
las restricciones de acceso a datos aplicables (CNST-007, CNST-025,
CNST-031).

Granularidad: un diagrama canonico por modulo funcional.

.. toctree::
 :maxdepth: 1
 :caption: Modulos funcionales

 mod-auth
 mod-users
 mod-access
 mod-permissions
 mod-admin
 mod-alerts
 mod-audit
 mod-pipeline
 mod-logs
 mod-reports
 mod-operator
 mod-caller
 mod-supervision
