.. meta::
   :artefacto: TAREAS-RESOLVER-RAMAS-PENDIENTES
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T21:37:24
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-resolver-ramas-pendientes:

==================================================
Tareas: Resolver Ramas Pendientes
==================================================

Lista de tareas
===============

.. list-table::
   :header-rows: 1
   :widths: 8 46 28 18

   * - ID
     - Tarea
     - Producto
     - Estado
   * - T-001
     - Analisis del estado de las 5 ramas (inventario,
       clasificacion por hash).
     - ``analisis-estado-ramas-pendientes.rst``
     - Completada
   * - T-002
     - R1: verificar ``.thyrox/`` por hash; rescatar el unico
       archivo nuevo.
     - ``analisis-rescate-thyrox-r1.rst`` +
       ``wp-tmp/architecture-constraints.md``
     - Completada
   * - T-003
     - R2: analisis profundo (fechas + contenido sustantivo
       vs trivial).
     - ``analisis-profundo-r2.rst``
     - Completada
   * - T-004
     - R2: rescatar 12 archivos (grupo B + C) a ``wp-tmp/``.
     - ``wp-tmp/r2-uc-sup-01/`` (12 + PROCEDENCIA)
     - Completada
   * - T-005
     - R3: analisis profundo (patron inverso, verificacion de
       modelo RBAC y relacion PR #20).
     - ``analisis-profundo-r3.rst``
     - Completada
   * - T-006
     - R3: rescate masivo de los 79 cambiados a ``wp-tmp/``.
     - ``wp-tmp/r3-backup-20260517/`` (79 + PROCEDENCIA)
     - Completada
   * - T-007
     - Estructura PROC-GOB-013: alcance, tareas, progreso,
       decisiones, index del directorio.
     - 5 RST de la iniciativa
     - Completada
   * - T-008
     - Enlazar la iniciativa en ``pm/iniciativas/index.rst``
       (seccion activas).
     - ``pm/iniciativas/index.rst``
     - Completada

Resoluciones de rama (no son tareas de archivo)
================================================

.. list-table::
   :header-rows: 1
   :widths: 14 86

   * - Rama
     - Resolucion
   * - R1
     - Resuelta. ``architecture-constraints.md`` rescatado;
       7 ``.thyrox/`` identicos ya en develop; ``now.md``
       ignorado (incremental); ``source/`` descartado
       (nomenclatura antigua). Rama borrable.
   * - R2
     - Resuelta. 12 archivos de la spec UC-SUP-01 rescatados
       a ``wp-tmp/``. Grupo A y ``logs/`` descartados con
       justificacion. Rama borrable.
   * - R3
     - Resuelta (preservacion). 79 cambiados rescatados a
       ``wp-tmp/``. Analisis de integracion de los 68 que
       difieren = fase posterior. Rama borrable.
   * - R4
     - Borrar: ahead=0, no aporta (contenido ya en develop
       via PR #20). Sin riesgo.
   * - R5
     - Borrar **tras** integrar la iniciativa
       ``sanear-deuda-ci-y-normativa`` (su contenido D-01 ya
       esta absorbido alli). Dependencia explicita.

DAG de dependencias
===================

* T-001 precede a T-002..T-006 (el inventario define que
  rescatar).
* T-002..T-006 son independientes entre si (ramas disjuntas).
* T-007 depende de que T-001..T-006 esten completas (las
  tareas se documentan con su estado real).
* T-008 depende de que exista el ``index.rst`` del directorio
  (creado en T-007).
* R5 (resolucion) depende de la integracion de la iniciativa
  ``sanear-deuda-ci-y-normativa`` (cross-iniciativa).

Tabla de cobertura
==================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Rama
     - Tarea
     - Evidencia
   * - R1
     - T-002
     - Tabla de hashes en ``analisis-rescate-thyrox-r1``;
       1 de 9 unico real.
   * - R2
     - T-003/T-004
     - Diff de magnitud en ``analisis-profundo-r2``; stub
       14 lineas vs 358 en R2.
   * - R3
     - T-005/T-006
     - ``analisis-profundo-r3``; 68 R3-mas-reciente, 8
       nuevos, modelo v5.4.0 vigente.
   * - R4
     - (resolucion)
     - ahead=0 verificado.
   * - R5
     - (resolucion)
     - Contenido D-01 absorbido en
       ``sanear-deuda-ci-y-normativa``.
