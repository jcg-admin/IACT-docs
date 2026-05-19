.. meta::
   :artefacto: TAREAS-Y-PROGRESO-RESOLVER-TESTS-PIPELINE-RESIDUAL-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-pipeline-residual-iact-api
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:35:00
   :ultimo_cambio: 2026-05-19T21:35:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-resolver-tests-pipeline-residual-iact-api:

==============================================================
Tareas y Progreso: Resolver Tests Pipeline Residual
==============================================================

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - ID
     - Descripcion
     - Resultado
   * - T-001
     - Diagnosticar 4 fallas pipeline iniciales:
       TestIVRClientsReport (3 tests),
       TestIVRMenuRedirected/Center.
     - Completada. Causa raiz observable:
       503 Service Unavailable en endpoints
       que consultan SPs MariaDB.
   * - T-002
     - Re-clone test_ivr_legacy con
       mysqldump --routines --triggers --events
       desde ivr_legacy.
     - Completada. 16 tablas + 19 routines
       restauradas.
   * - T-003
     - Run pipeline tests con clone — sigue
       fallando con "table doesn't exist".
     - Completada. Hallazgo: test_ivr_legacy
       se vacia entre runs (pytest --create-db).
   * - T-004
     - Loud-fail en _sql() de fixtures/ivr.py.
     - Completada. Commit
       IACT-api ``29259c3``. Sin esto, errores
       de fixture se enmascaraban.
   * - T-005
     - Diagnostico con loud fail: descubre
       "alter routine command denied" en
       DROP PROCEDURE de fixture ivr_schema.
     - Completada. Causa raiz #1
       identificada: falta CREATE/ALTER ROUTINE.
   * - T-006
     - Anadir GRANT CREATE ROUTINE +
       ALTER ROUTINE en setup.sh de IACT-db
       para test_ivr_legacy.
     - Completada. Commit IACT-db
       ``c50eafe``.
   * - T-007
     - Aplicar grants runtime + run pipeline
       tests sin --create-db.
     - Completada. 25/25 pipeline pass.
   * - T-008
     - Run full suite sin --create-db.
     - Completada. **1396 passed + 1 skipped,
       0 failed. 100% pass scope ejecutable.**
   * - T-009
     - Documentar deuda separada
       ``sanear-pytest-config-iact-api``
       (--create-db NO usar con tests pipeline).
     - Completada. Plan maestro ya tiene #4
       que cubre esto.
   * - T-010
     - Documentacion iniciativa.
     - Completada. Esta iniciativa.

Conteo
=======

* Total: 10 tareas.
* Completadas: 10/10.

Inicio: 2026-05-19T21:25:00

Cierre: 2026-05-19T21:35:00

Iniciativa candidata derivada
==============================

* **sanear-pytest-config-iact-api** (ya en plan maestro
  #4): documentar oficialmente que ``--create-db`` no
  debe usarse con tests que tengan TEST DBs con
  ``CREATE_DB: False`` (que Django ignora pero el
  proyecto interpretaba como autoritativo). Actualizar
  README o procedimiento ``proc-doc-013-validacion-sphinx``
  con el caveat.

Cierre del bloque P1 fix tests del plan maestro
=================================================

Esta iniciativa cierra la sub-secuencia P1 fix tests del
plan maestro (#1 dashboard, #2 alerts, #3 pipeline).

Total acumulado de la sesion:

* **19 iniciativas cerradas**.
* 71/71 fallas pytest resueltas (100%).
* Pass rate pytest IACT-api: **100% del scope ejecutable**.
* Pass rate jest IACT-ui: **100%** (2381/2381).
* 5 repos clean, todas las ramas pusheadas.

Siguiente bloque del plan maestro: P2 saneamiento
estructural alto-impacto (#4 pytest config, #9 docs UCs
faltantes, #12 UI sin marker).
