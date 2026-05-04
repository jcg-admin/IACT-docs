.. meta::
 :artefacto: INDEX_AT_OPERATIONAL_VIEW
 :tipo: Indice — Operational Viewpoint
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-view-index:

====================================
Operational View — Vista Operacional
====================================

Viewpoint Operational del sistema IACT segun el framework de Rozanski & Woods.
Describe como el sistema sera operado, administrado y soportado cuando este
en ejecucion en su entorno de produccion.

Este viewpoint es una contribucion original de Rozanski & Woods — no tiene
equivalente en Kruchten 4+1, Soni, Clements ni Garland. Para IACT es de
importancia ALTA por sus requisitos de auditoria regulatoria, monitoreo
del pipeline ETL y soporte en produccion.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Documento
   - Descripcion
 * - :doc:`system-administration`
   - Administracion del sistema: gestion de usuarios y RBAC por
     AGR_ADMIN, activacion/desactivacion, permisos temporales,
     separacion de funciones. Diagramas de actividad y casos de uso.
 * - :doc:`system-configuration`
   - Configuracion del sistema: variables de entorno, parametros ETL,
     umbrales de alerta, horarios APScheduler, configuracion de
     retencion de logs (CNST-024).
 * - :doc:`system-support`
   - Soporte en produccion: monitoreo del pipeline ETL, diagnostico
     de alertas, consulta de logs, dashboard de salud del sistema.
 * - :doc:`system-installation`
   - Instalacion y bootstrap: despliegue inicial, migraciones Django,
     carga de datos iniciales RBAC, verificacion del sistema.

.. toctree::
 :maxdepth: 1
 :caption: Operational View

 system-administration
 system-configuration
 system-support
 system-installation

----

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/context-view/stakeholders`
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/vistas-y-viewpoints`
