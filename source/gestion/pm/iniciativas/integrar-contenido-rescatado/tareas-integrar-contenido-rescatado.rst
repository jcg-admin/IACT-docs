.. meta::
   :artefacto: TAREAS-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-integrar-contenido-rescatado:

==================================================
Tareas: Integrar el contenido rescatado a source/
==================================================

Las tareas de integracion (T-003..T-022) preparan el contenido
en el clon con hash verificado y toctrees enlazados. La
verificacion de build de cada grupo la ejecuta el usuario en su
local (el clon no completa el build PlantUML); por eso el
"Estado" de una tarea de integracion es "Preparada" hasta que
el usuario confirma build 0 warnings.

Estructura
==========

.. list-table::
   :header-rows: 1
   :widths: 8 50 24 18

   * - ID
     - Tarea
     - Producto
     - Estado
   * - T-001
     - Analisis (origen, alcance acotado, estrategia).
     - ``analisis-integrar-...rst``
     - Completada
   * - T-002
     - Estructura PROC-GOB-013 (alcance, tareas, progreso,
       decisiones, index) + enlace en
       ``pm/iniciativas/index.rst``.
     - 5 RST + index
     - En ejecucion

Grupo R2 — spec UC-SUP-01 (riesgo bajo)
========================================

Destino: ``source/requisitos/casos-uso/supervision/uc-sup-01/``.
Origen: R2 ``feature/arquitectura-tecnica-content``
(``43250b49``). Una tarea por archivo (atomica).

.. list-table::
   :header-rows: 1
   :widths: 8 56 18 18

   * - ID
     - Archivo (reemplaza stub salvo indicado)
     - Verif. hash
     - Estado
   * - T-003
     - ``actores-precondiciones.rst``
     - Pendiente
     - Pendiente
   * - T-004
     - ``criterios-aceptacion.rst``
     - Pendiente
     - Pendiente
   * - T-005
     - ``datos-involucrados.rst``
     - Pendiente
     - Pendiente
   * - T-006
     - ``excepciones.rst``
     - Pendiente
     - Pendiente
   * - T-007
     - ``flujo-principal.rst``
     - Pendiente
     - Pendiente
   * - T-008
     - ``flujos-alternos.rst``
     - Pendiente
     - Pendiente
   * - T-009
     - ``implementacion-tecnica.rst``
     - Pendiente
     - Pendiente
   * - T-010
     - ``informacion-general.rst``
     - Pendiente
     - Pendiente
   * - T-011
     - ``patrones-diseno.rst``
     - Pendiente
     - Pendiente
   * - T-012
     - ``requisitos-no-funcionales.rst``
     - Pendiente
     - Pendiente
   * - T-013
     - ``testing.rst``
     - Pendiente
     - Pendiente
   * - T-014
     - ``diagramas-uml.rst`` (NUEVO; enlazar en
       ``uc-sup-01/index`` toctree)
     - Pendiente
     - Pendiente
   * - T-015
     - Verificar toctree ``uc-sup-01/index`` referencia los
       12; build 0 warnings (usuario).
     - —
     - Pendiente

Grupo R3 — archivos nuevos (riesgo medio)
==========================================

Origen: R3 ``integration/backup-20260517_021658``
(``bc112cfd``). Cada nuevo se crea Y se enlaza en el toctree
de su seccion en la misma tarea (prevencion de huerfano).

.. list-table::
   :header-rows: 1
   :widths: 8 60 16 16

   * - ID
     - Archivo nuevo + toctree a enlazar
     - Verif. hash
     - Estado
   * - T-016
     - ``arquitectura-tecnica/rbac/modelo-rbac-iact.rst``
       (2897 lin, v5.4.0) + toctree rbac
     - Pendiente
     - Pendiente
   * - T-017
     - ``normativa/restricciones/cnst-030-...-sod.rst`` +
       toctree restricciones
     - Pendiente
     - Pendiente
   * - T-018
     - ``casos-uso/access/uc-acc-01/diagramas-uml.rst`` +
       toctree uc-acc-01
     - Pendiente
     - Pendiente
   * - T-019
     - ``casos-uso/access/uc-acc-03/diagramas-uml.rst`` +
       ``uc-acc-04`` + ``uc-acc-05`` + toctrees
     - Pendiente
     - Pendiente
   * - T-020
     - ``casos-uso/access/uc-acc-08/diagramas-uml.rst`` +
       toctree uc-acc-08
     - Pendiente
     - Pendiente
   * - T-021
     - ``casos-uso/permissions/uc-perm-06/diagramas-uml.rst``
       + toctree uc-perm-06
     - Pendiente
     - Pendiente
   * - T-022
     - Verificar cero huerfanos; build 0 warnings (usuario);
       marcar DEBT-008/009 resueltas.
     - —
     - Pendiente

DAG de dependencias
===================

* T-001 -> T-002 -> (Grupo R2) -> (Grupo R3).
* Dentro de R2: T-003..T-014 independientes entre si; T-015
  depende de las 12.
* Dentro de R3: T-016..T-021 independientes; T-022 depende de
  todas y de T-015.
* T-022 (cierre de deuda) depende de la verificacion de build
  del usuario en ambos grupos.

Tabla de cobertura
==================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Deuda
     - Tareas
     - Criterio
   * - DEBT-008 (R2)
     - T-003..T-015
     - 12 archivos integrados, hash verificado, build 0
       warnings.
   * - DEBT-009 (R3 nuevos)
     - T-016..T-022
     - 8 archivos integrados y enlazados en toctree, build
       0 warnings.
   * - DEBT-010 (R3 difieren)
     - (ninguna)
     - Out-of-scope; sigue activa.
   * - DEBT-011 (R1)
     - (ninguna)
     - Out-of-scope; sigue activa.
