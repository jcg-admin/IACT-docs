.. meta::
   :artefacto: TAREAS-SANEAR-DEUDA-CI-Y-NORMATIVA
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-ci-y-normativa
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:21:29
   :ultimo_cambio: 2026-05-18T18:21:29
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-sanear-deuda-ci-y-normativa:

==============================================
Tareas: Sanear Deuda de CI y Normativa
==============================================

Cada tarea es atomica y toca un solo archivo. El orden de commit
respeta PROC-GOB-013: estructura independiente de ejecucion.

Lista de tareas
===============

.. list-table::
   :header-rows: 1
   :widths: 8 44 28 20

   * - ID
     - Descripcion
     - Archivo
     - Estado
   * - T-001
     - Corregir ruta en el paso 1 del orden de creacion
       (H-N1); bump version 1.0.0 -> 1.0.1; entrada de
       historial.
     - ``source/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion.rst``
     - Completada
   * - T-002
     - Rediseno: dos jobs (incremental bloqueante /
       completo), sin ``make clean`` en incremental, cache
       de doctrees, ``-j 2``, triggers sin ``feature/**``,
       guard de visibilidad publica en el job completo.
     - ``.github/workflows/validate.yml``
     - Completada
   * - T-003
     - Corregir A-01 (``parallel_write_safe`` -> False),
       A-02 (log de hit), A-06 (warning si fallan estilos);
       bump version interna 1.0.0 -> 1.1.0.
     - ``source/_ext/plantuml_cached.py``
     - Completada
   * - T-004
     - Cierre D-01 W1: cajon toctree
       ``:caption: Infraestructura`` -> ``infrastructure/index``.
     - ``source/index.rst``
     - Completada
   * - T-005
     - Cierre D-01 W2: toctree
       ``:caption: Hallazgos y Evidencia Vigente`` ->
       ``hallazgos-init-iact-docs-2026-05-16``.
     - ``source/gestion/evidencia/index.rst``
     - Completada
   * - T-006
     - Cierre D-01 W3: ``.. code-block:: cron`` ->
       ``.. code-block:: bash`` (lexer valido).
     - ``source/devops/runbooks/runbook-cron-jobs-mantenimiento.rst``
     - Completada
   * - T-007
     - Estructura de la iniciativa: enlazar el ``index.rst``
       de la iniciativa en el toctree de iniciativas activas.
     - ``source/gestion/pm/iniciativas/index.rst``
     - Completada

DAG de dependencias
===================

* T-001 .. T-006 son **independientes entre si** (archivos
  disjuntos, sin orden forzado de ejecucion).
* T-007 depende de que exista el ``index.rst`` de la iniciativa
  (creado en el commit de estructura).
* Orden de commit (PROC-GOB-013): estructura (incluye T-007 y el
  index del directorio) -> T-001 -> T-002 -> T-003 ->
  T-004..T-006 (cierre D-01 agrupado).

Tabla de cobertura analisis -> tarea
=====================================

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Hallazgo (analisis)
     - Tarea
     - Verificacion
   * - E1.1 ``make clean`` rebuild completo
     - T-002
     - ``make clean`` solo en job completo; incremental con
       cache de doctrees.
   * - E1.2 ``-j auto`` OOM
     - T-002
     - ``-j 2`` en ambos jobs; 0 ocurrencias de ``-j auto``.
   * - E1.3 trigger ``feature/**``
     - T-002
     - ``branches: [develop, main]`` en push.
   * - E2.1 / H-N1 ruta PROC-GOB-013
     - T-001
     - Paso 1 usa ``source/gestion/pm/iniciativas/{...}/``;
       historial 1.0.1.
   * - A-01 ``parallel_write_safe``
     - T-003
     - Declarado ``False``; version interna 1.1.0.
   * - A-02 hit no logueado
     - T-003
     - ``logger.info`` de hit presente.
   * - A-06 estilos silenciosos
     - T-003
     - Dos ``logger.warning`` (ilegible / no encontrado).
   * - D-01 W1/W2/W3
     - T-004/T-005/T-006
     - Build ``-W -j 2`` = ``build succeeded`` 0 warnings
       (log ``d01-verif-j2-20260518T151329``).
   * - A-03/A-04/A-05
     - (sin tarea)
     - Descartados tras verificacion; no son defectos.
   * - H-N2 / H-N3 multi-repo
     - (sin tarea)
     - Diferidos a iniciativa dedicada (out-of-scope).
