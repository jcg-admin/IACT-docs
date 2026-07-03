.. meta::
   :artefacto: TAREAS-Y-PROGRESO-AUDITAR-IMPLEMENTACION-UCS-API-UI
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-implementacion-ucs-api-ui
   :repo_objetivo: multiple
   :estado: Completada
   :version: 1.0.0
   :fecha_creacion: 2026-07-03T22:15:30
   :ultimo_cambio: 2026-07-03T22:15:30
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-auditar-implementacion-ucs-api-ui:

==============================================================
Tareas y Progreso: Auditar Implementacion UCs en api y ui
==============================================================

Lista de tareas
================

.. list-table::
   :header-rows: 1
   :widths: 6 10 44 40

   * - ID
     - Repo
     - Descripcion
     - Resultado
   * - T-001
     - IACT-docs
     - Enumerar los UCs declarados en
       ``requisitos-funcionales/`` (dominio + slug).
     - Completada — 88 UCs (uc-001..091, huecos 047-049)
   * - T-002
     - IACT-api
     - Extraer markers ``UC_*`` con formas compuestas y
       rangos; clasificar evidencia fuerte vs debil.
     - Completada — 73 markers fuertes
   * - T-003
     - IACT-ui
     - Idem en ``src/**``.
     - Completada — 73 markers fuertes
   * - T-004
     - IACT-docs
     - Mapping textual UC → marker (mapping verificado
       2026-05-19 + campo ``Marker código`` de
       uc-078..090 + declaracion de uc-091).
     - Completada — 69 mapeados + uc-091 scheduler
   * - T-005
     - multiple
     - Inspeccionar buckets negativos antes de publicar
       gaps (FG-1..FG-3).
     - Completada — 3 falsos gaps evitados
   * - T-006
     - IACT-docs
     - Verificar consistencia OUT (operator/caller/
       supervision): declaracion en docs + 0 markers.
     - Completada — consistente
   * - T-007
     - IACT-docs
     - Producir matriz completa 88 filas como artefacto
       separado (umbral de tamaño del deep-analisis).
     - Completada — ``matriz-implementacion-uc-api-ui``
   * - T-008
     - IACT-docs
     - Documentar hallazgos F-01..F-07 con clasificacion
       y proponer iniciativas derivadas.
     - Completada — 5 iniciativas derivadas propuestas

Progreso
=========

Auditoria ejecutada y completada en la sesion 2026-07-03.
Artefactos: alcance, deep-analisis, matriz (88 filas) y este
registro. Evidencia de trabajo en el WP
``2026-07-03-22-15-30-auditar-implementacion-ucs-api-ui``
(``.thyrox/context/work/``).

Las iniciativas derivadas (F-03..F-07) quedan **propuestas,
no abiertas** — su apertura es decision del ejecutor.
