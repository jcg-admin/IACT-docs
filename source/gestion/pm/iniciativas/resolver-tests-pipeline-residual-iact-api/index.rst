.. meta::
   :artefacto: INICIATIVA-RESOLVER-TESTS-PIPELINE-RESIDUAL-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:35:00
   :ultimo_cambio: 2026-05-19T21:35:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-resolver-tests-pipeline-residual-iact-api:

==============================================================
Iniciativa: Resolver Tests Pipeline Residual IACT-api
==============================================================

P1 del plan maestro #3. Cierra las **4 fallas residuales del
bucket pipeline** que quedaban tras las iniciativas anteriores
de saneamiento. Lleva el pytest full suite a **100% pass del
scope ejecutable**: 1396 passed + 1 skipped intencional sobre
1397 colectados (0 failed).

Resumen de la sesion completa
==============================

.. list-table::
   :header-rows: 1
   :widths: 50 18 32

   * - Snapshot
     - Failed
     - Pass rate
   * - Inicial sesion
     - 67 + 4 errors
     - 95%
   * - Tras #7 (DML grants + crypto)
     - 30
     - 97.85%
   * - Tras #8 (URLs, SPs, EXECUTE)
     - 22
     - 98.43%
   * - Tras #17 (dashboard residual)
     - 12
     - 99.14%
   * - Tras #18 (alerts residual)
     - 4
     - 99.71%
   * - **Tras #19 (esta — pipeline residual)**
     - **0**
     - **100% (1396/1396 ejecutables)**

**71 fallas resueltas de 71 iniciales (100%).**

3 causas raiz descubiertas
============================

1. **Faltaban grants CREATE ROUTINE + ALTER ROUTINE** en
   test_ivr_legacy para django_user. La fixture ivr_schema
   hace DROP+CREATE de SPs y fallaba con
   "ERROR 1370 alter routine command denied". Fix
   permanente en IACT-db setup.sh.
2. **_sql() en fixtures/ivr.py enmascaraba errores**:
   no levantaba RuntimeError en returncode != 0. Errores
   de schema creation se perdian silenciosamente, los tests
   fallaban "abajo" sin trazabilidad. Fix: loud fail con
   stderr.
3. **--create-db pytest-django wipea test_ivr_legacy**
   incluso con ``CREATE_DB: False`` en settings.
   Django ignora la option ``CREATE_DB`` (no existe en
   spec). pytest.ini ya tiene ``--reuse-db`` default;
   no usar --create-db con tests pipeline. Documentado
   como deuda separada
   ``sanear-pytest-config-iact-api`` (#4 del plan).

Commits
========

* IACT-db ``c50eafe``: ROUTINE grants en setup.sh.
* IACT-api ``29259c3``: loud-fail en _sql().

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-resolver-tests-pipeline-residual-iact-api
