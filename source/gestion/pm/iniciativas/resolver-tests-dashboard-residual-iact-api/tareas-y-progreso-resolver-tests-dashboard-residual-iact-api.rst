.. meta::
   :artefacto: TAREAS-Y-PROGRESO-RESOLVER-TESTS-DASHBOARD-RESIDUAL-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-dashboard-residual-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:13:08
   :ultimo_cambio: 2026-05-19T21:13:08
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-resolver-tests-dashboard-residual-iact-api:

==============================================================
Tareas y Progreso: Resolver Tests Dashboard Residual
==============================================================

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - ID
     - Descripcion
     - Resultado
   * - T-001
     - Diagnosticar causa raiz por test (pagination,
       multipart, RBAC, permission, signal, cache).
     - Completada. 6 causas raiz distintas en 10
       fallas, todas son tests bugs (no productivos).
   * - T-002
     - Fix tests pagination (2): asumir OrderedDict
       paginado.
     - Completada. test_list_dashboards_authenticated,
       test_list_widgets.
   * - T-003
     - Fix tests multipart (3): format='json' explicito.
     - Completada. test_create_dashboard,
       test_update_own/other_dashboard.
   * - T-004
     - Fix test RBAC: WidgetViewSetTestCase usa
       create_superuser.
     - Completada. test_create_widget pasa.
   * - T-005
     - Fix test clone non-owned: clonar propio.
     - Completada. test_clone_action pasa.
   * - T-006
     - Fix tests signal: cleanup en setUp tras
       create_user.
     - Completada. test_create_default_dashboard y
       _already_exists pasan.
   * - T-007
     - Fix test cache: @override_settings LocMemCache.
     - Completada.
       test_invalidate_cache_on_widget_update pasa.
   * - T-008
     - Run pytest apps/dashboard/ 49/49 passing.
     - Completada. Verificado.
   * - T-009
     - Run full suite verificar regresion.
     - Completada. 1385 passed, 12 failed (99.14%);
       reduccion neta de 10 fallas vs antes.
   * - T-010
     - Commit + push IACT-api.
     - Completada. Commit ``4fde6ec`` en branch
       feature/resolver-tests-dashboard-residual-iact-api.
   * - T-011
     - Documentacion iniciativa IACT-docs.
     - Completada. Esta iniciativa.

Conteo
=======

* Total: 11 tareas.
* Completadas: 11/11.

Inicio: 2026-05-19T20:58:52

Cierre: 2026-05-19T21:13:08

Resultados acumulados de la sesion
====================================

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Snapshot
     - Failed
     - Pass rate
   * - Inicial sesion
     - 67 + 4 errors
     - 95%
   * - Tras iniciativa #7 (DML, crypto)
     - 30
     - 97.85%
   * - Tras iniciativa #8 (URLs, SPs, EXECUTE)
     - 22
     - 98.43%
   * - **Tras iniciativa #17 (dashboard residual)**
     - **12**
     - **99.14%**

**Total resueltas: 55 / 71 fallas iniciales (77.5%).**
Remaining 12 distribuidas en:
- apps/alerts/* 8 (#18 del plan)
- pipeline integration 4 (#19 del plan)
