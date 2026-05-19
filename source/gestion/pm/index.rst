.. meta::
   :artefacto: INDEX-GESTION-PM
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm
   :estado: Vigente
   :version: 2.0.0
   :fecha_creacion: 2026-04-28
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm:

==================
Project Management
==================

Proposito
=========

Este subdominio contiene la documentacion de gestion del proyecto IACT,
incluyendo iniciativas activas, planificacion, auditorias, lecciones
aprendidas y matrices de trazabilidad.

Estructura
==========

La gestion vertical por submodulo del sistema IACT (api, db, docs,
server, ui) se rige por
:doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.
Cada submodulo tiene un indice propio con roadmap, iniciativas,
decisiones, riesgos e indicadores.

.. toctree::
   :maxdepth: 2
   :caption: Gestion por submodulo

   api/index
   db/index
   docs/index
   server/index
   ui/index

.. toctree::
   :maxdepth: 2
   :caption: Iniciativas

   iniciativas/index

.. toctree::
   :maxdepth: 1
   :caption: Auditorias y seguimiento

   audits/index
   lecciones-aprendidas/index
   matrices/index

.. toctree::
   :maxdepth: 1
   :caption: Planificacion

   planificacion-releases-frontend
   deployment-plan

.. toctree::
   :maxdepth: 1
   :caption: Procesos operativos

   checklists/index

Trazabilidad
============

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Procedimiento rector (iniciativas)**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Procedimiento rector (gestion por submodulo)**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Skills documentales**
     - ``workflow-discover`` · ``workflow-scope`` · ``workflow-implement`` ·
       ``workflow-track`` · ``workflow-standardize``
   * - **Skills de proyecto**
     - ``pm-initiating`` · ``pm-planning`` · ``pm-executing`` ·
       ``pm-monitoring`` · ``pm-closing``
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming` — kebab-lowercase
