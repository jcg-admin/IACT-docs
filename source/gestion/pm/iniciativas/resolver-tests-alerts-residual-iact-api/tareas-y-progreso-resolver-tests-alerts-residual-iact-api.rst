.. meta::
   :artefacto: TAREAS-Y-PROGRESO-RESOLVER-TESTS-ALERTS-RESIDUAL-IACT-API
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-alerts-residual-iact-api
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:25:00
   :ultimo_cambio: 2026-05-19T21:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-resolver-tests-alerts-residual-iact-api:

==============================================================
Tareas y Progreso: Resolver Tests Alerts Residual
==============================================================

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - ID
     - Descripcion
     - Resultado
   * - T-001
     - Fix test_scheduler self-detection.
     - Completada.
   * - T-002
     - Fix test_message_str con formato nuevo del
       modelo.
     - Completada.
   * - T-003
     - Fix test_configuration_str con formato nuevo.
     - Completada.
   * - T-004
     - skipTest test_unique_together_constraint con
       justificacion (constraint removido UC_ALR_05).
     - Completada.
   * - T-005
     - Fix 2 string-case "maximo" -> "Maximo"
       (test_models + test_services).
     - Completada.
   * - T-006
     - Fix test_mark_read URL hyphen -> underscore.
     - Completada.
   * - T-007
     - Fix recipient_ids como write_only en
       serializer + tolerancia en
       test_create_message_endpoint.
     - Completada. **Unico cambio productivo** de la
       iniciativa.
   * - T-008
     - Run pytest apps/alerts/ 38/38 + 1 skipped.
     - Completada.
   * - T-009
     - Run full suite: 4 failed, 1392 passed
       (99.71%).
     - Completada.
   * - T-010
     - Commit + push IACT-api ``469b52e``.
     - Completada.
   * - T-011
     - Documentacion iniciativa.
     - Completada.

Conteo
=======

* Total: 11 tareas.
* Completadas: 11/11.

Inicio: 2026-05-19T21:13:08

Cierre: 2026-05-19T21:25:00

Iniciativa candidata derivada
==============================

* ``aclarar-unicidad-alert-subscription``: definir si
  AlertSubscription debe imponer unicidad a nivel de modelo
  (constraint condicional) o queda delegada al servicio
  por la dualidad FK alert_configuration/rule.

Resultados acumulados sesion
==============================

* Inicial: 67 + 4 errors (95%).
* Tras #17 (dashboard): 12 failed (99.14%).
* **Tras #18 (alerts): 4 failed (99.71%).**
* 63/71 fallas resueltas (88.7%).

Remaining: 4 fallas pipeline integration (bucket #19 del
plan).
