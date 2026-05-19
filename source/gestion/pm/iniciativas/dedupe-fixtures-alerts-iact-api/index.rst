.. meta::
   :artefacto: INICIATIVA-DEDUPE-FIXTURES-ALERTS-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:30:00
   :ultimo_cambio: 2026-05-19T22:30:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-dedupe-fixtures-alerts-iact-api:

==============================================================
Iniciativa: Dedupe Fixtures Alerts IACT-api
==============================================================

P3 plan #8. Crea fixture pytest ``module_alerts`` en
``apps/alerts/tests/conftest.py`` para evitar la
duplicacion de
``Module.objects.get_or_create(code='MOD_Alerts')``
detectada en 3 setUp distintos del archivo
test_viewsets.py.

Cambio aplicado
================

* Archivo nuevo ``apps/alerts/tests/conftest.py`` con
  fixture ``module_alerts(db)``.

Commit IACT-api ``c3e69c2``. Verificacion: pytest sin
regresion (38 passed + 1 skipped).

Limitacion conocida
=====================

Los tests existentes usan ``django.test.TestCase``
(unittest) que NO consume pytest fixtures via
parameters. La fixture queda **disponible para tests
NUEVOS** pero los 3 setUp duplicados existentes
permanecen sin refactorizar.

Iniciativa candidata derivada:
``migrar-tests-alerts-a-pytest-style`` que convierta
los 3 TestCase a clases pytest-style permitiendo
consumir la fixture y eliminar la duplicacion real.
