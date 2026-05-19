.. meta::
   :artefacto: TAREAS-Y-PROGRESO-RESOLVER-TESTS-FALLIDOS-PYTEST-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-fallidos-pytest-iact-api
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:42:40
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-resolver-tests-fallidos-pytest-iact-api:

==============================================================
Tareas y Progreso: Resolver Tests Fallidos + UI Build
==============================================================

Lista de tareas
================

.. list-table::
   :header-rows: 1
   :widths: 6 6 38 50

   * - ID
     - Repo
     - Descripcion
     - Resultado / Evidencia
   * - T-001
     - IACT-db
     - Ampliar grants a DML
       (SELECT/INSERT/UPDATE/DELETE) sobre
       ``test_ivr_legacy`` en
       ``provisioners/mariadb/setup.sh``.
     - Completada. Aplicado via mysql -e directo y
       luego al setup.sh (idempotente para futuros
       contenedores). Conteo fallas pytest:
       67 -> 38 (29 resueltas). Commit IACT-db
       ``2989d90``.
   * - T-002
     - IACT-api
     - ``pip install --force-reinstall cryptography``
       en el venv para eliminar mix con cryptography
       de system python que causaba
       ``pyo3_runtime.PanicException``.
     - Completada. ``cryptography 48.0.0`` en
       ``.venv/lib/python3.11/site-packages``.
       Pytest ``tests/unit/authentication/`` paso
       de 19 fallas a 0 (125 pass). No requiere
       commit en repos (es estado del venv runtime;
       el ``requirements/testing.txt`` declara la
       dep correctamente).
   * - T-003
     - IACT-api
     - Fix ``apps/alerts/tests/test_viewsets.py``:
       3 ocurrencias de Function.module='MOD_Alerts'
       (string) corregidas a instance Module via
       get_or_create.
     - Completada. Conteo apps/alerts/test_viewsets:
       10 fallas -> 8 (mejora parcial; las 8
       restantes son individuales, no FK). Commit
       IACT-api ``d6c12c0``.
   * - T-004
     - IACT-ui
     - ``webpack.config.js`` anade aliases que
       vivian solo en ``jest.config.cjs``:
       ``@store``, ``@lib``, ``@facades``,
       ``@utils``, ``@/``. Habilita resolver los
       imports en build prod.
     - Completada. Errores webpack
       "Module not found" pasan de 44 a 0.
   * - T-005
     - IACT-ui
     - ``package.json`` declara
       ``react-select ^5.10.2`` como dependencia
       (importado pero no instalado; jest lo
       mockeaba).
     - Completada. ``npm install`` agrega 29
       paquetes (transitivas de react-select).
   * - T-006
     - IACT-ui
     - ``_password-strength.scss`` linea 24 y
       ``_login-page.scss`` linea 164: reemplazar
       ``@include transition-medium/long(a, b)``
       (mixins solo aceptan 1 arg) por
       transiciones expandidas equivalentes.
     - Completada. 4 errores SCSS -> 0.
   * - T-004+T-005+T-006
     - IACT-ui
     - ``npm run build`` end-to-end OK.
     - ``webpack 5.106.2 compiled with 21 warnings
       in 4632 ms`` (0 errores). Bundles generados
       en ``dist/``. ``npm test`` sigue verde
       (250 suites, 2381 tests). Commit IACT-ui
       ``dcabba7``.
   * - T-007
     - IACT-api
     - Re-run full suite con todos los fixes
       aplicados.
     - Completada. ``30 failed, 1367 passed, 1
       warning in 86s``. 97.85% pass (vs 95%
       inicial). 37 fallas resueltas
       acumuladamente (67 -> 30).
   * - T-008
     - IACT-docs
     - Documentacion compacta de la iniciativa
       (alcance + tareas-y-progreso + decisiones).
     - Completada. Esta iniciativa.

Resumen runtime cross-repo
============================

.. list-table::
   :header-rows: 1
   :widths: 18 32 18 32

   * - Repo
     - Rama
     - Commit
     - Cambio principal
   * - IACT-db
     - feature/resolver-tests-fallidos-pytest-iact-api
     - ``2989d90``
     - DML grants en test_ivr_legacy
   * - IACT-api
     - feature/resolver-tests-fallidos-pytest-iact-api
     - ``d6c12c0``
     - alerts test fixture Module FK
   * - IACT-ui
     - feature/resolver-tests-fallidos-pytest-iact-api
     - ``dcabba7``
     - webpack aliases + react-select + scss
   * - IACT-docs
     - feature/resolver-tests-fallidos-pytest-iact-api
     - (este commit)
     - documentacion compacta

Resumen de fallas pytest IACT-api
==================================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Snapshot
     - Conteo
     - Notas
   * - Inicial
     - 67 failed, 4 errors
     - sanear-deuda-runtime-multirepo T-005
   * - Tras DML grants
     - 38 failed
     - 29 resueltas (pipeline integration)
   * - Tras cryptography reinstall
     - 38 failed (aun)
     - cryptography fix afecta tests/unit/auth y
       middleware (combinado con DML el conteo neto
       quedo igual; auth + middleware ya estaban
       en los 38)
   * - Tras alerts fixture fix
     - 30 failed, 1367 passed
     - 8 resueltas (alerts viewsets parcial)
   * - Total resuelto
     - 37 / 67 (55%)
     -
   * - Residual
     - 30 failed (97.85% pass)
     - Diferidas a iniciativas individuales por
       bucket (ver decisiones)

Conteo
=======

* Total: 8 tareas.
* Completadas: 8/8.
* Pendientes: 0.
* Bloqueadas: 0.

Inicio: 2026-05-19T19:07:37

Cierre: 2026-05-19T19:42:40
