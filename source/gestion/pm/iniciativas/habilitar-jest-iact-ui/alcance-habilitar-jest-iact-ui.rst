.. meta::
   :artefacto: ALCANCE-HABILITAR-JEST-IACT-UI
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/habilitar-jest-iact-ui
   :repo_objetivo: IACT-ui
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:52:11
   :ultimo_cambio: 2026-05-19T18:52:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-habilitar-jest-iact-ui:

==============================================================
Alcance: Habilitar jest en IACT-ui
==============================================================

Por que existe
==============

IACT-ui es el ultimo eslabon de la cadena ``db -> api -> ui``.
Con db y api ya operativos (iniciativas hermanas cerradas),
queda completar ui para validar el sistema completo. Los tests
de IACT-ui usan Jest 29 + React Testing Library 16 y no
requieren conexion al backend (mock server local en
``mock-server/`` y mocks unitarios en ``src/mocks/``).

Estado inicial: contenedor tiene Node 22.22.2 + npm 10.9.7.
``IACT-ui/node_modules/`` no existe; ``package.json`` declara
1357 deps directas + transitivas.

Criterio de completitud verificable
=====================================

* ``node_modules/`` poblado tras ``npm install``.
* ``npm test`` ejecuta la suite Jest y reporta:

  - Test Suites: todos PASS, 0 fail.
  - Tests: todos PASS, 0 fail.

In-scope
========

* ``npm install`` con ``--no-audit --no-fund`` para reducir
  ruido.
* ``npm test`` como smoke test de la suite completa.
* Captura del conteo total como evidencia.

Out-of-scope
============

* Cualquier trabajo sobre ``uc-opr-*``, ``uc-sup-*`` y
  ``uc-cli-01..05``.
* ``npm run build`` (production webpack): no necesario para
  pruebas.
* ``npm run dev`` (servidor de desarrollo): no aplica al
  ciclo de tests.
* Linting / type-check (``npm run lint``): pendientes de
  iniciativa propia.
* Tests E2E o de integracion con backend real: requieren
  IACT-api corriendo como servicio, fuera de scope aqui.
* Resolucion de warnings de deprecacion de transitivas
  (``inflight``, ``glob@7``, ``fstream``): es ruido de
  ``npm install``, no bloquea tests.

Decisiones de contenido tomadas durante la lectura
====================================================

* ``package.json`` declara ``"test": "jest"``: no requiere
  cambios para invocar la suite (basta ``npm test``).
* La carpeta ``mock-server/`` (1 nivel) provee fixtures
  estaticos que jest puede leer; no se levanta como
  servicio para los tests unitarios.
