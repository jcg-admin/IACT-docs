.. meta::
   :artefacto: TAREAS-EVOLUCIONAR-PROC-GOB-013-MULTIREPO
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/evolucionar-proc-gob-013-multirepo
   :repo_objetivo: multiple
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:18:39
   :ultimo_cambio: 2026-05-19T18:18:39
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-evolucionar-proc-gob-013-multirepo:

==========================================================
Tareas: Evolucionar PROC-GOB-013 a Multi-Repo
==========================================================

Cada tarea es atomica. T-001..T-003 viven en IACT-docs.
T-004 vive en IACT (repo orquestador). El orden de commit
respeta PROC-GOB-013: la estructura de la iniciativa se
commitea antes que cualquier ejecucion.

Lista de tareas
===============

.. list-table::
   :header-rows: 1
   :widths: 6 4 44 26 20

   * - ID
     - Repo
     - Descripcion
     - Archivo
     - Estado
   * - T-001
     - IACT-docs
     - Evolucion PROC-GOB-013 a v2.0.0: anadir seccion
       Meta-modelo con ``:repo_objetivo:`` obligatorio
       (dominio enumerado), generalizar rutas por valor
       de ``:repo_objetivo:``, reformular skills como
       referencia para IACT-docs, cross-ref a
       PROC-GOB-014, entrada de historial.
     - ``source/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion.rst``
     - Pendiente
   * - T-002
     - IACT-docs
     - Marcar DEBT-012 y DEBT-013 como Resuelta con
       referencia a esta iniciativa y a la version 2.0.0
       de PROC-GOB-013.
     - ``source/risks-technical-debt/deuda-proc-gob-013-multirepo.rst``
     - Pendiente
   * - T-003
     - IACT-docs
     - Enlazar el ``index.rst`` de la iniciativa en el
       toctree de "Iniciativas activas" de
       ``iniciativas/index.rst``.
     - ``source/gestion/pm/iniciativas/index.rst``
     - Pendiente
   * - T-004
     - IACT
     - Copiar ``.claude/`` de IACT-docs al repositorio
       IACT (orquestador) como bootstrap. Demuestra
       ``:repo_objetivo: multiple`` con evidencia real.
     - ``IACT/.claude/`` (repo IACT, no IACT-docs)
     - Pendiente

DAG de dependencias
====================

* **T-001** independiente de T-002, T-003, T-004 (archivos
  disjuntos en repos posiblemente distintos).
* **T-002** depende conceptualmente de que T-001 exista
  (DEBT-012/013 se marcan Resueltas referenciando la nueva
  v2.0.0); puede commitearse antes si la referencia se
  declara como "introducida por esta iniciativa" sin
  apuntar a la version concreta. Decision: commitear
  despues de T-001.
* **T-003** depende de que existan los artefactos de la
  iniciativa (ya creados en la fase de estructura).
* **T-004** independiente de T-001..T-003 (vive en otro
  repo). Se commitea en su propia rama y push del repo
  IACT, en paralelo con la ejecucion en IACT-docs.

Verificacion por tarea
========================

Cada tarea termina con:

* ``sphinx-build -b dummy`` produce ``build succeeded`` y
  cero warnings nuevos (validacion en IACT-docs).
* El cambio queda commiteado en la rama
  ``feature/evolucionar-proc-gob-013-multirepo`` del repo
  correspondiente y pusheado a ``origin``.
* La tabla de progreso en
  ``progreso-evolucionar-proc-gob-013-multirepo.rst`` se
  actualiza marcando la tarea como Completada y
  registrando el hash de commit corto.
