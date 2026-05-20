.. meta::
   :artefacto: TAREAS-Y-PROGRESO-RESOLVER-TESTS-DASHBOARD-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-dashboard-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:42:40
   :ultimo_cambio: 2026-05-19T19:57:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-resolver-tests-dashboard-iact-api:

==============================================================
Tareas y Progreso: Resolver Tests Dashboard IACT-api
==============================================================

Iniciativa ultra-compacta (un solo cambio de 6 lineas).
Documento todo en el index + esta tabla.

.. list-table::
   :header-rows: 1
   :widths: 6 6 38 50

   * - ID
     - Repo
     - Descripcion
     - Resultado / Evidencia
   * - T-001
     - IACT-api
     - Diagnosticar causa de 17
       fallas dashboard.
     - Completada. AssertionError
       404 != 200 +
       "Not Found: /api/dashboard/dashboards/"
       => URL router gap.
   * - T-002
     - IACT-api
     - Anadir
       ``path('api/dashboard/',
       include('apps.dashboard.urls'))``
       a ``config/urls.py``.
     - Completada. Commit
       ``a85d942``. 6 lineas
       insertadas (path +
       comentario justificativo).
   * - T-003
     - IACT-api
     - Verificar reduccion: pytest
       full + apps/dashboard.
     - Completada.
       apps/dashboard: 17 -> 10
       failed (7 resueltas).
       Suite global: 30 -> 22
       failed (1375 passed,
       98.43% pass rate).
   * - T-004
     - IACT-docs
     - Documentar la iniciativa.
     - Completada. Esta iniciativa.
   * - T-005
     - IACT-db
     - Aplicar a ``ivr_legacy``:
       ``sp_etl_pipeline.sql`` (5 SPs ETL) +
       ``sp_rpt_reportes.sql`` (7 SPs reporte) +
       ``schema_historico.sql`` + ``seed_historico.sql``.
       Originalmente declarados out-of-scope por
       ``preparar-entorno-mariadb-ivr-legacy``; el
       sponsor corrigio: "integration es integration,
       las tablas hay que provisionarlas".
     - Completada. 19 routines en ivr_legacy (7 funciones
       + 12 SPs). ``tbl_historico_t1_2025..t1_2026`` con
       ~13k filas seed. ``sp_etl_maestro()`` invocado:
       234 filas en base_ivr_detalle (Q02_26).
   * - T-006
     - IACT-db
     - Clonar ``ivr_legacy`` -> ``test_ivr_legacy`` con
       ``mysqldump --routines`` para que las pruebas tengan
       los SPs disponibles. Aplicar grants
       (DDL+DML+EXECUTE).
     - Completada. ``test_ivr_legacy`` tiene 7 funciones
       + 12 SPs + 13 tablas + grants completos.
   * - T-007
     - IACT-db
     - Detectar causa raiz de 4 fallas pipeline residuales
       (TestIVRClientsReport, TestIVRMenuRedirected,
       TestIVRMenuCenter): EXECUTE denied al invocar SPs.
     - Completada. ``mysql -u django_user -e "CALL
       sp_rpt_menu_redirigidos('Q01_25')"`` retorna
       "ERROR 1370 execute command denied". Causa
       identificada.
   * - T-008
     - IACT-db
     - Anadir grant EXECUTE en setup.sh para
       ``ivr_legacy`` (SELECT+EXECUTE) y
       ``test_ivr_legacy`` (DDL+DML+EXECUTE).
     - Completada. Commit IACT-db ``83e22e8``. Suite full
       22 -> 19 failed (3 resueltas: ivr-clients,
       menu-redirected, menu-center).

Conteo
=======

* Total: 8 tareas.
* Completadas: 8/8.

Inicio: 2026-05-19T19:42:40

Cierre: 2026-05-19T20:02:00

Resultados acumulados
======================

.. list-table::
   :header-rows: 1
   :widths: 30 18 52

   * - Snapshot
     - Fallas
     - Causa raiz dominante
   * - Antes de la iniciativa (cierre #7)
     - 30 failed / 97.85%
     - Bucket dashboard 17, alerts 6,
       pipeline 5, otros 2.
   * - Tras T-002 (config/urls dashboard)
     - 22 failed / 98.43%
     - 8 resueltas (dashboard URL routing).
   * - Tras T-005-T-007 (SPs en BD)
     - 22 failed / 98.43%
     - SPs cargados; tests no usaban SPs
       prod directamente (fixtures
       reemplazan SPs con test versions),
       pero esto preparo T-008.
   * - Tras T-008 (EXECUTE grant)
     - 19 failed / 98.64%
     - 3 resueltas (ivr-clients,
       menu-redirected, menu-center).
   * - Acumulado sesion
     - 19 (vs 67 inicial) / 98.64%
     - **48 de 67 resueltas (72%)**.
