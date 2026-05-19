.. meta::
   :artefacto: INDEX-PM-UI
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm-ui
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-ui:

==============================
Gestion del submodulo ``ui``
==============================

.. warning::

   Submodulo en bootstrap. Las secciones marcadas ``Pendiente``
   se completan a medida que el trabajo se acumula. Ver criterios
   de madurez en
   :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.

Proposito
=========

Gestion vertical del submodulo ``ui`` (frontend React): roadmap
de versiones, iniciativas con impacto en cliente, decisiones
arquitectonicas, riesgos abiertos e indicadores de calidad.

Alcance
=======

Entra
-----

- Componentes React, estado, routing.
- Empaquetado, bundle size, performance de carga.
- Politica de releases del cliente (ver
  :doc:`/gestion/pm/planificacion-releases-frontend`).
- Accesibilidad, internacionalizacion, telemetria de cliente.
- Consumo de la API: contratos, manejo de errores, retry.

No entra
--------

- Implementacion de los endpoints (ver
  :doc:`/gestion/pm/api/index`).
- Hosting del bundle estatico en runtime (ver
  :doc:`/gestion/pm/server/index`).

Roadmap
=======

Ver :doc:`/gestion/pm/planificacion-releases-frontend` como
roadmap actual del submodulo. Cuando se promueva un roadmap
propio en este indice, se reemplazara la referencia.

Iniciativas activas
===================

Sin entradas. Pendiente.

Decisiones recientes
====================

Sin entradas. Pendiente.

Riesgos abiertos
================

Sin entradas. Pendiente.

Indicadores
===========

Pendiente. Candidatos a definir baseline:

- Bundle size (kB gzipped) por release.
- Cobertura de tests de componentes.
- p95 de Time-to-Interactive en navegadores objetivo.

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Plan de releases**
     - :doc:`/gestion/pm/planificacion-releases-frontend`
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice padre**
     - :doc:`/gestion/pm/index`
