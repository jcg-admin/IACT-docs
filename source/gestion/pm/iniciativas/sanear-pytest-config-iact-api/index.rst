.. meta::
   :artefacto: INICIATIVA-SANEAR-PYTEST-CONFIG-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:45:00
   :ultimo_cambio: 2026-05-19T21:45:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-sanear-pytest-config-iact-api:

==============================================================
Iniciativa: Sanear pytest Config IACT-api
==============================================================

P2 del plan maestro #4. Cierra la deuda metodologica
identificada en
``resolver-tests-pipeline-residual-iact-api`` causa raiz #3:
el flag ``--create-db`` invalida silenciosamente la fixture
``ivr_schema`` porque pytest-django ignora
``TEST['CREATE_DB'] = False`` (no es setting reconocido por
Django).

Entregable
============

Comentario extenso en ``callcentersite/pytest.ini``
documentando el gotcha + marker ``tst_fr`` registrado.
Commit IACT-api ``eb8f3e8``.

No se cambio:

* ``--reuse-db`` default (ya estaba correcto).
* ``manage.py`` default a ``development`` (cambiar rompe
  flujo de devs locales — el override
  ``DJANGO_SETTINGS_MODULE=config.settings.testing_local``
  es estandar para tests).

Resultado: pytest sigue 1396 passed + 1 skipped, sin
regresion. Cualquier desarrollador futuro que abra
pytest.ini vera el warning sobre --create-db.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-sanear-pytest-config-iact-api
