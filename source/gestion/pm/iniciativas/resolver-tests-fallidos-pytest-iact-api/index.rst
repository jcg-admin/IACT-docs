.. meta::
   :artefacto: INICIATIVA-RESOLVER-TESTS-FALLIDOS-PYTEST-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:42:40
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-resolver-tests-fallidos-pytest-iact-api:

==============================================================
Iniciativa: Resolver Tests Fallidos pytest IACT-api + UI Build
==============================================================

Ataca las 67 fallas + 4 errors observadas en
``sanear-deuda-runtime-multirepo`` T-005 mediante diagnostico
por causa raiz, y resuelve la deuda
``DEBT-FUTURE-UI-BUILD-PROD`` detectada al ejecutar
``npm run build`` en IACT-ui (44 errores Module not found +
4 errores SCSS).

Resultado: 37 de 67 fallas pytest resueltas (55%) + UI build
production restaurado (0 errores). Las 30 fallas restantes
quedan trazadas con causa raiz identificada y diferidas a
iniciativas dedicadas — son individuales (no buckets
homogeneos atacables en bloque).

Tiene ``:repo_objetivo: multiple`` (IACT-api + IACT-db +
IACT-ui). Patron Modelo C-runtime de PROC-GOB-013 v2.0.0 D3.

.. toctree::
   :maxdepth: 1

   alcance-resolver-tests-fallidos-pytest-iact-api
   tareas-y-progreso-resolver-tests-fallidos-pytest-iact-api
   decisiones-resolver-tests-fallidos-pytest-iact-api
