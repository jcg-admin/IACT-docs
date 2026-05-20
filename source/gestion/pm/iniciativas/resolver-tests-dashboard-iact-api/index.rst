.. meta::
   :artefacto: INICIATIVA-RESOLVER-TESTS-DASHBOARD-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:42:40
   :ultimo_cambio: 2026-05-19T19:57:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-resolver-tests-dashboard-iact-api:

==============================================================
Iniciativa: Resolver Tests Dashboard IACT-api (router gap)
==============================================================

Octava iniciativa de la sesion. Ataca el bucket dashboard (17
fallas pytest registradas en
``resolver-tests-fallidos-pytest-iact-api`` decisiones).
Diagnostico revelo causa raiz unitaria: ``apps.dashboard.urls``
existe con router DRF completo pero ``config/urls.py`` nunca
lo incluyo.

Fix de una linea: ``path('api/dashboard/',
include('apps.dashboard.urls'))`` en ``config/urls.py``.

Resultado: 17 -> 10 fallas dashboard (7 resueltas). Suite
global 30 -> 22 (8 resueltas neto). Pass rate global
97.85% -> 98.43%.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-resolver-tests-dashboard-iact-api

Alcance
=======

* Diagnosticar la causa de las 17 fallas en
  ``apps/dashboard/tests/test_viewsets.py``.
* Aplicar fix si la causa es comun y bloqueante.
* Documentar fallas residuales con su causa.

In-scope: registro de URL del router DRF.
Out-of-scope: fallas residuales con causas individuales
(pagination contract mismatch, assertion deltas) — quedan
para iniciativa dedicada ``resolver-tests-dashboard-residual``.

Resultado
=========

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Snapshot
     - Fallas
     - Notas
   * - Pre-fix
     - 17 dashboard / 30 global
     - 404 != 200 / Not Found
   * - Post-fix URLs
     - 10 dashboard / 22 global
     - Las 10 son por test logic
       (pagination, assertions
       sobre count, etc.)
   * - Resueltas
     - 7 dashboard / 8 global
     - El +1 global es porque
       test_signals.py tambien
       dependia del routing.

Diagnostico
============

``apps/dashboard/urls.py`` declara router con 4 ViewSets:

* ``DashboardConfigViewSet`` -> dashboards/
* ``WidgetConfigViewSet`` -> widgets/
* ``SavedFilterViewSet`` -> filters/
* ``UserDashboardPreferenceViewSet`` -> preferences/

``config/urls.py`` listaba 9 apps (navigation, authentication,
users, access, audit, alerts, pipeline, reports, logs) pero
no dashboard. Los tests intentaban
``GET /api/dashboard/dashboards/`` y Django respondia 404
(Not Found) — la URL no existia en el dispatcher.

Causa de la omision: el commit historico
"B-03 fix: todas las apps conectadas al router raiz" omitio
dashboard (probablemente porque la app era nueva en una
rama no integrada o por simple miss). Sin un test de
contract de URLs, el gap quedo invisible hasta correr
pytest con cobertura de viewsets.

Fix
====

.. code-block:: python

   # callcentersite/config/urls.py (post-fix)
   urlpatterns = [
       # ... apps previas ...
       path('api/logs/', include('apps.logs.urls')),

       # Dashboard (UC_DSH_01..04) — registrado tras detectar
       # 404 != 200 en apps/dashboard/tests/test_viewsets.py
       path('api/dashboard/', include('apps.dashboard.urls')),
   ]

Commit ``a85d942`` en
``feature/resolver-tests-dashboard-iact-api`` de IACT-api.

Fallas residuales (diferidas)
==============================

10 fallas en apps/dashboard/ con causa individual:

* **Pagination contract mismatch**: tests asumen que
  ``response.data`` es ``list`` pero DRF retorna
  ``OrderedDict(count/next/previous/results)`` por
  pagination default. ~6 tests.
* **Assertion deltas**: el test esperaba 200 cuando la
  respuesta real es 201 (CREATED) o 400 (validation). ~3
  tests. test_create_dashboard, test_clone_action,
  test_update_other_dashboard, etc.
* **Multipart vs JSON**: 1 test usa ``format='multipart'``
  con ``config_data`` dict (no soportado en multipart).

Cada una requiere edit del test correspondiente o
ajuste de la view para alinear el contract. Iniciativa
hermana: ``resolver-tests-dashboard-residual-iact-api``.

Conclusion
==========

Causa raiz dominante eliminada (URL router gap). De las 17
fallas dashboard, 7 eran consecuencia directa del 404; las
10 restantes son test logic separada. Suite global mejora
de 97.85% a 98.43% pass rate con un commit de 6 lineas.
