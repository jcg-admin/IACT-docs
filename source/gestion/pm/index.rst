.. meta::
   :artefacto: INDEX-GESTION-PM
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm
   :estado: Vigente
   :version: 2.0.0
   :fecha_creacion: 2026-04-28
   :ultimo_cambio: 2026-05-16T23:01:11
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

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Skills documentales**
     - ``workflow-discover`` · ``workflow-scope`` · ``workflow-implement`` ·
       ``workflow-track`` · ``workflow-standardize``
   * - **Skills de proyecto**
     - ``pm-initiating`` · ``pm-planning`` · ``pm-executing`` ·
       ``pm-monitoring`` · ``pm-closing``
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming` — kebab-lowercase
