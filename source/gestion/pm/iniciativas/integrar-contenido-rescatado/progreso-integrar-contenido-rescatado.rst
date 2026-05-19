.. meta::
   :artefacto: PROGRESO-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Progreso
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _progreso-integrar-contenido-rescatado:

==================================================
Progreso: Integrar el contenido rescatado a source/
==================================================

Estado de tareas
=================

.. list-table::
   :header-rows: 1
   :widths: 14 50 18 18

   * - Grupo
     - Descripcion
     - Estado
     - Commit
   * - T-001
     - Analisis
     - Completada
     - ``a607ebd0``
   * - T-002
     - Estructura PROC-GOB-013
     - En ejecucion
     - (este commit)
   * - T-003..T-015
     - Integrar R2 (12 archivos)
     - Pendiente
     - —
   * - T-016..T-022
     - Integrar R3 nuevos (8 archivos)
     - Pendiente
     - —

Conteo
======

* Total de tareas: 22
* Completadas: 1
* En ejecucion: 1 (T-002)
* Pendientes: 20 (ejecucion de integracion)
* Bloqueadas: 0

Nota sobre el estado "Pendiente" de la integracion
====================================================

Las tareas de integracion (T-003..T-022) estan pendientes
porque su ejecucion incluye verificacion de build
``sphinx-build -W -j 2`` por grupo, que se realiza en el local
del usuario (el clon no completa el build PlantUML). La
preparacion (copia con hash verificado + enlace de toctree) se
hace en el clon; el cierre de cada grupo depende de la
confirmacion de build 0 warnings del usuario.

Inicio
======

* Inicio: 2026-05-18T23:37:34
* Cierre: (pendiente)

Este documento se actualiza tras cada tarea y antes de cada
commit.
