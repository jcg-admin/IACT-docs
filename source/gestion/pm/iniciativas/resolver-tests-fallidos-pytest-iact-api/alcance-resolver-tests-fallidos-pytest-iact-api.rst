.. meta::
   :artefacto: ALCANCE-RESOLVER-TESTS-FALLIDOS-PYTEST-IACT-API
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-fallidos-pytest-iact-api
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:42:40
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-resolver-tests-fallidos-pytest-iact-api:

==============================================================
Alcance: Resolver Tests Fallidos pytest IACT-api + UI Build
==============================================================

Por que existe
==============

La iniciativa hermana ``sanear-deuda-runtime-multirepo`` T-005
cuantifico la brecha pytest IACT-api en 67 failed + 4 errors
sobre 1397 tests colectados (95% pass), pero defirio el fix
de cada una. En paralelo, una verificacion proactiva de
``npm run build`` en IACT-ui revelo deuda no documentada:
44 errores "Module not found" + 4 errores SCSS — el bundle
de produccion estaba roto desde antes de la sesion (jest
pasaba 2381 por moduleNameMapper, webpack no resolvia
aliases).

Esta iniciativa ataca **ambas brechas en paralelo** segun
instruccion del sponsor: "no enfocar solo en docs; api y ui
en paralelo, tomar las mejores decisiones". El criterio es
"no dejar deuda tecnica observable".

Criterio de completitud verificable
=====================================

* ``npm run build`` en IACT-ui termina con 0 errores
  (warnings de deprecacion Sass tolerados, registrados como
  deuda futura).
* ``npm test`` en IACT-ui sigue verde tras los fixes
  (250 suites / 2381 tests / 0 failures).
* La causa raiz de cada bucket de fallas pytest queda
  identificada y registrada en
  ``decisiones-*``.
* Las fallas que tienen causa raiz comun y fixable en
  bloque (DML grants, cryptography, fixture Module FK) se
  resuelven en esta iniciativa.
* Las 30 fallas residuales quedan listadas con su file y
  bucket, diferidas a iniciativas individuales o
  dedicadas por bucket.
* Iniciativa ``:repo_objetivo: multiple`` cross-repo:
  IACT-api (test fixture), IACT-db (provisioner),
  IACT-ui (webpack + scss + package.json).

In-scope
========

* Fix de IACT-db ``provisioners/mariadb/setup.sh``:
  ampliar grants a DML sobre ``test_ivr_legacy``. Resuelve
  ~29 fallas de integracion del pipeline IVR
  (OperationalError 1142 "DELETE command denied").
* Reinstalar ``cryptography`` en el venv de IACT-api con
  ``--force-reinstall`` para evitar el mix system/venv
  que disparaba ``pyo3_runtime.PanicException``. Resuelve
  ~8 fallas de auth JWT y middleware audit.
* Fix de fixture en
  ``apps/alerts/tests/test_viewsets.py``: pasar instance
  Module en lugar de string ``'MOD_Alerts'`` al campo
  ForeignKey ``Function.module``. Resuelve parcialmente
  el bucket alerts viewsets.
* Fix de IACT-ui ``webpack.config.js``: anadir aliases
  ``@store``, ``@lib``, ``@facades``, ``@utils``, ``@/``
  que vivian solo en jest. Anadir ``react-select`` como
  dependencia.
* Fix de IACT-ui SCSS: reemplazar invocaciones
  ``@include transition-medium(width, background)`` y
  ``@include transition-long(width, height)`` por
  transiciones expandidas (los mixins solo aceptan 1
  argumento).
* Documentacion compacta de la iniciativa en IACT-docs.

Out-of-scope
============

* Cualquier trabajo sobre ``uc-opr-*``, ``uc-sup-*`` y
  ``uc-cli-01..05``.
* Las 30 fallas residuales pytest (dashboard 14+2+1=17,
  alerts 4+1+1=6, pipeline 5 + 2, otros): cada una es
  individual y requiere investigacion separada.
  Diferidas a iniciativas hermanas (una por bucket).
* Warnings de deprecacion Sass (``@import``, ``darken()``):
  deuda futura ``sanear-sass-deprecations-iact-ui``.
* Las 204 warnings de eslint (``react/prop-types``,
  ``no-unused-vars``): deuda
  ``sanear-eslint-warnings-iact-ui``.
* Implementacion de UCs in-scope.
