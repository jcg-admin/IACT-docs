.. meta::
   :artefacto: TAREAS-Y-PROGRESO-SANEAR-DEUDA-RUNTIME-MULTIREPO
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-runtime-multirepo
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:12:52
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-sanear-deuda-runtime-multirepo:

==============================================================
Tareas y Progreso: Sanear Deuda Runtime Multi-Repo
==============================================================

Iniciativa cross-repo con commits reales en tres repos:
IACT-api, IACT-ui y IACT. Esta iniciativa estrena el patron
``:repo_objetivo: multiple`` con tres ramas paralelas
``feature/sanear-deuda-runtime-multirepo``, una por repo
afectado.

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
     - IACT-api
     - Anadir ``django-extensions==3.2.3`` a
       ``requirements/testing.txt`` (H-E1).
     - Completada. ``requirements/testing.txt``
       incluye nueva linea con comentario que
       justifica la dependencia. Commit
       ``86b52cb``.
   * - T-002
     - IACT-api
     - Modificar
       ``callcentersite/config/settings/base.py``
       para crear ``PROJECT_ROOT/'logs'`` al
       cargarse (H-E3).
     - Completada. Linea
       ``(PROJECT_ROOT / 'logs').mkdir(exist_ok=True)``
       anadida tras definicion de PROJECT_ROOT.
       Comentario explica el por que.
       Verificacion: ``rm -rf logs/`` +
       ``manage.py check`` reconstruye
       ``logs/django.log`` y reporta "System check
       identified no issues (0 silenced)". Mismo
       commit ``86b52cb``.
   * - T-003
     - IACT-ui
     - Anadir bloque ``overrides`` a
       ``package.json`` forzando
       ``glob: ^10.4.5`` (DEBT-FUTURE-NPM-DEPS
       parcial).
     - Completada. ``rm -rf node_modules
       package-lock.json && npm install``
       reconstruye con 1228 paquetes (vs 1357
       previo). ``npm test`` mantiene "250 test
       suites passed, 2381 tests passed, 0
       failures" — 20.9s. Commit ``61b2155``.
   * - T-004
     - IACT
     - Anadir ``IACT-docs`` como submodulo en
       ``docs/``. Editar ``.gitignore`` para
       quitar ``docs/`` y ``.gitmodules`` para
       anadir el bloque (H-E1 cierre mariadb).
     - Completada. ``.gitignore``: regla ``docs/``
       removida. ``.gitmodules``: bloque
       ``[submodule "docs"]`` con URL canonica
       https://github.com/jcg-admin/IACT-docs.git
       (mismo patron que api/db/ui). ``git
       status`` reporta ``A  docs``
       (gitlink 160000). Commit ``00c401c6``.
   * - T-005
     - IACT-api
     - Re-ejecutar pytest sin filtro de marker
       con ``--create-db`` para medir la suite
       completa. Documenta la brecha real entre
       los 1397 tests colectados y los que pasan.
     - Completada. Ejecucion runtime:
       "67 failed, 1326 passed, 4 errors in
       93.54s". Brecha 67+4 = 71 issues a
       investigar (5.1% del total). Diferida a
       iniciativa
       ``resolver-tests-fallidos-pytest-iact-api``.
   * - T-006
     - IACT-docs
     - Documentar la iniciativa (alcance, tareas
       y progreso, decisiones) con evidencia de
       las T-001..T-005.
     - Completada. Esta iniciativa: 3 archivos
       RST en formato compacto.

Resumen runtime cross-repo
============================

.. list-table::
   :header-rows: 1
   :widths: 22 22 18 38

   * - Repo
     - Rama
     - Commit
     - Cambio principal
   * - IACT-api
     - feature/sanear-deuda-runtime-multirepo
     - ``86b52cb``
     - testing.txt + auto-mkdir logs/
   * - IACT-ui
     - feature/sanear-deuda-runtime-multirepo
     - ``61b2155``
     - package.json overrides glob ^10
   * - IACT
     - feature/sanear-deuda-runtime-multirepo
     - ``00c401c6``
     - submodulo docs + .gitignore fix
   * - IACT-docs
     - feature/sanear-deuda-runtime-multirepo
     - (este commit)
     - documentacion de la iniciativa

Conteo
=======

* Total: 6 tareas.
* Completadas: 6/6.
* Pendientes: 0.
* Bloqueadas: 0.

Inicio: 2026-05-19T19:07:37

Cierre: 2026-05-19T19:12:52

Historial
==========

.. list-table::
   :header-rows: 1
   :widths: 18 22 60

   * - Version
     - Fecha
     - Cambio
   * - 1.0.0
     - 2026-05-19T19:12:52
     - Apertura y cierre con ejecucion completa.
       Tres commits cross-repo + documentacion
       compacta. Mide brecha real pytest:
       1326/1397 (95% pass).
