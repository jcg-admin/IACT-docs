.. meta::
   :artefacto: TAREAS-Y-PROGRESO-IMPLEMENTAR-UC-RPT-05-06-PROGRAMACION-REPORTES
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/implementar-uc-rpt-05-06-programacion-reportes
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-implementar-uc-rpt-05-06-programacion-reportes:

==============================================================
Tareas y Progreso: Implementar UC_RPT_05/06 (discovery)
==============================================================

Lista de tareas
================

.. list-table::
   :header-rows: 1
   :widths: 6 6 38 50

   * - ID
     - Repo
     - Descripcion
     - Resultado
   * - T-001
     - IACT-api
     - Fase 1 DISCOVER: inspeccionar
       ``apps/reports/`` buscando scaffolding
       existente para programacion de reportes.
     - Completada. Encontrado
       ``schedule_views.py`` (202 lineas) +
       ``schedule_service.py`` (67 lineas).
   * - T-002
     - IACT-api
     - Verificar markers UC en el scaffolding.
     - Completada.
       ``schedule_views.py`` declara
       ``UC_RPT_07 — Programar Reporte`` y
       ``UC_RPT_08 — Ver Reportes Programados``.
   * - T-003
     - IACT-api
     - Confirmar que UC_RPT_05/06 no existen en
       codigo.
     - Completada. ``grep -E "UC_RPT_05|UC_RPT_06"``
       en apps/reports/ retorna 0 hits.
   * - T-004
     - IACT-docs
     - Producir mapping correcto docs <-> codigo
       para el dominio reports.
     - Completada. Documentado en deep-analysis:
       uc-036 -> UC_RPT_07, uc-037 -> UC_RPT_08;
       UC_RPT_05/06 son gaps de numeracion.
   * - T-005
     - IACT-docs
     - Identificar el gap real del dominio
       reports.
     - Completada. UC_RPT_02 (uc-033) declarado
       STUB explicito por CNST-004 (no es
       implementable bajo restricciones vigentes).
   * - T-006
     - IACT-docs
     - Cerrar la iniciativa documentando que NO
       requiere codigo nuevo.
     - Completada. Esta iniciativa.

Conteo
=======

* Total: 6 tareas.
* Completadas: 6/6.

Inicio: 2026-05-19T20:13:49

Cierre: 2026-05-19T20:25:00

Tareas que NO se ejecutaron y por que
========================================

Originalmente planificadas pero descartadas tras T-002:

* Implementar ``ScheduledReport`` model + migration.
  **No se ejecuto** — el modelo ya existia (linea en
  schedule_views.py: ``from apps.reports.models import
  ScheduledReport``).
* Implementar ScheduleService con APScheduler.
  **No se ejecuto** — ``schedule_service.py`` (67 lineas)
  ya contiene ``ScheduleValidator`` y ``ScheduleService``.
* Implementar 4 endpoints REST.
  **No se ejecuto** — las views (POST/PATCH/DELETE/GET)
  ya estan declaradas en ``schedule_views.py`` con
  ``extend_schema``.
* Tests pytest end-to-end.
  **No se ejecuto** — esta fuera de scope verificar
  ahora la cobertura de tests del scaffolding existente
  (iniciativa hermana
  ``auditar-conformidad-fr-tests-aceptacion`` lo cubrira).
* UI nueva en ``IACT-ui/src/pages/reports/``.
  **No se ejecuto** — pendiente de verificar si existe
  pagina UI sin marker (iniciativa hermana
  ``auditar-componentes-ui-sin-marker``).
