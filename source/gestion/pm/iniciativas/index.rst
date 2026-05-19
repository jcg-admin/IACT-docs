.. meta::
   :artefacto: INDEX-PM-INICIATIVAS
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm/iniciativas
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-19T18:18:39
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-iniciativas:

=============
Iniciativas
=============

Registro de todas las iniciativas documentales y de proyecto
ejecutadas o en curso bajo ``source/gestion/pm/``.

Cada iniciativa sigue el ciclo definido en
:doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`.

Iniciativas activas
===================

.. toctree::
   :maxdepth: 1

   integrar-contenido-rescatado/index
   resolver-ramas-pendientes/index
   sanear-deuda-ci-y-normativa/index

Iniciativas cerradas
====================

.. toctree::
   :maxdepth: 1

   ampliar-devops-runbooks/index
   crear-infrastructure-skeleton/index
   evolucionar-proc-gob-013-multirepo/index
   habilitar-jest-iact-ui/index
   habilitar-pytest-iact-api/index
   preparar-entorno-mariadb-ivr-legacy/index
   preparar-entorno-postgresql-iact-analytics/index

Trazabilidad
============

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Naming**
     - ``{verbo}-{objeto}`` en kebab-lowercase.
       Ejemplo: ``integrar-infrastructure-source``
   * - **Ubicacion**
     - ``source/gestion/pm/iniciativas/{nombre-iniciativa}/``
