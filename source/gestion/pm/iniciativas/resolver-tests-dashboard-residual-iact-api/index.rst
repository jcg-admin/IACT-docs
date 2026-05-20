.. meta::
   :artefacto: INICIATIVA-RESOLVER-TESTS-DASHBOARD-RESIDUAL-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:13:08
   :ultimo_cambio: 2026-05-19T21:13:08
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-resolver-tests-dashboard-residual-iact-api:

==============================================================
Iniciativa: Resolver Tests Dashboard Residual IACT-api
==============================================================

P1 del plan maestro #1. Cierra las 10 fallas residuales del
bucket dashboard que quedaron tras
``resolver-tests-dashboard-iact-api`` (que solo resolvio
el URL routing — 7/17 fallas).

**Resultado:** 10 fallas resueltas. ``apps/dashboard/``
pasa de 33/49 a **49/49** pytest passing. Full suite global
22 -> 12 failed, **99.14% pass rate** (1385/1397).

Causas raiz por test:

* **Pagination contract** (2 tests): tests asumian
  ``response.data`` es list, pero DRF default paginate
  retorna OrderedDict con results.
* **Multipart vs JSON** (3 tests): POST/PUT con dict
  anidado requeria ``format='json'``.
* **RBAC granular** (1 test): CanCreateWidget exigia
  function ``dashboard.widget.create``; fix con
  ``create_superuser`` para bypass en tests del
  contrato del viewset.
* **Permiso clone non-owned** (1 test): clone POST en
  dashboard de otro denega; fix con clone propio.
* **Signal post_save crea dashboard** (2 tests):
  fix con cleanup en setUp tras ``create_user``.
* **DummyCache vs real** (1 test):
  ``@override_settings(CACHES=LocMemCache)`` local al
  test.

Commit IACT-api ``4fde6ec``. Sin cambios de codigo
productivo — solo tests.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-resolver-tests-dashboard-residual-iact-api
