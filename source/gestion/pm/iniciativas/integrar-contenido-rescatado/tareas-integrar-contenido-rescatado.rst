.. meta::
   :artefacto: TAREAS-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
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

Grupo R2 — spec UC-SUP-01 (ejecutado)
======================================

Planificado: 12 archivos (T-003..T-014). **Ejecutado: 11.**
``diagramas-uml.rst`` (T-014) se excluyo: develop ya tiene
``uc-sup-01/diagramas-uml/`` como subdirectorio mas completo
(integrar el plano seria huerfano + retroceso). Registrado
como DEBT-015.

Origen: R2 ``feature/arquitectura-tecnica-content``
(``43250b49``). Reemplazo de stub por contenido completo,
hash verificado contra la rama origen.

.. list-table::
   :header-rows: 1
   :widths: 10 50 20 20

   * - ID
     - Archivo
     - Verif. hash
     - Estado
   * - T-003
     - ``actores-precondiciones.rst``
     - = R2
     - Completada
   * - T-004
     - ``criterios-aceptacion.rst``
     - = R2
     - Completada
   * - T-005
     - ``datos-involucrados.rst``
     - = R2
     - Completada
   * - T-006
     - ``excepciones.rst``
     - = R2
     - Completada
   * - T-007
     - ``flujo-principal.rst``
     - = R2
     - Completada
   * - T-008
     - ``flujos-alternos.rst``
     - = R2
     - Completada
   * - T-009
     - ``implementacion-tecnica.rst``
     - = R2
     - Completada
   * - T-010
     - ``informacion-general.rst``
     - = R2
     - Completada
   * - T-011
     - ``patrones-diseno.rst``
     - = R2
     - Completada
   * - T-012
     - ``requisitos-no-funcionales.rst``
     - = R2
     - Completada
   * - T-013
     - ``testing.rst``
     - = R2
     - Completada
   * - T-014
     - ``diagramas-uml.rst`` — NO integrado (develop tiene
       subdirectorio mejor)
     - —
     - Excluida -> DEBT-015
   * - T-015
     - Verificar toctree ``uc-sup-01/index`` (los 11 ya
       listados) y build 0 warnings
     - —
     - Preparada (build: usuario)

Grupo R3 — archivos nuevos (no integrable)
===========================================

Planificado: 8 archivos (T-016..T-022). **Ejecutado: 0.** La
auditoria estatica de referencias y estructura (H-EJ1 de
decisiones) determino que ninguno es integrable sin
reintroducir deuda:

* ``cnst-030-sod.rst``: referencia cnst-029/031 inexistentes
  en develop (``:doc:`` rotos).
* ``modelo-rbac-iact.rst`` (plano) y los 6
  ``diagramas-uml.rst`` (planos): develop ya tiene esas rutas
  como subdirectorios mas completos. Integrar los planos =
  huerfano + retroceso.

.. list-table::
   :header-rows: 1
   :widths: 10 60 30

   * - ID
     - Archivo planificado
     - Resolucion
   * - T-016
     - ``modelo-rbac-iact.rst``
     - No integrable -> DEBT-014
   * - T-017
     - ``cnst-030-...-sod.rst``
     - No integrable -> DEBT-014
   * - T-018..T-021
     - 6 ``diagramas-uml.rst`` (access/permissions)
     - No integrables -> DEBT-014
   * - T-022
     - Cierre de grupo R3
     - N/A (grupo no integrado; deuda registrada)

DAG de dependencias (real)
===========================

* T-001 -> T-002 -> Grupo R2 (ejecutado) -> Grupo R3
  (auditado, no integrado).
* Dentro de R2: T-003..T-013 independientes; T-014 excluida;
  T-015 (verificacion build) depende de las 11 y la ejecuta
  el usuario.
* Grupo R3: la auditoria (parte de T-002/analisis) precedio a
  cualquier intento de integracion y lo bloqueo correctamente.

Tabla de cobertura (real)
==========================

.. list-table::
   :header-rows: 1
   :widths: 22 22 56

   * - Deuda
     - Tareas
     - Resultado
   * - DEBT-008 (R2)
     - T-003..T-013, T-015
     - 11 archivos integrados, hash verificado. Resolucion
       sujeta a build 0 warnings (usuario). DEBT-008 vive en
       ``deuda-integracion-wp-tmp`` (rama
       ``resolver-ramas-pendientes``): se marca resuelta
       alli al integrarse esa rama (dependencia cross-rama).
   * - DEBT-009 (R3 nuevos)
     - T-016..T-022
     - No integrados; reclasificados a DEBT-014
       (residuales R3) en esta rama.
   * - DEBT-014/015/016
     - (esta iniciativa los genera)
     - Registrados en
       ``deuda-integracion-r3-residual``.
   * - DEBT-010 (R3 difieren) / DEBT-011 (R1)
     - (ninguna)
     - Cross-rama (``resolver-ramas-pendientes``); fuera
       de alcance, siguen activas.
