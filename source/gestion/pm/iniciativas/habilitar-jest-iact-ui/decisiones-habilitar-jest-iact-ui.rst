.. meta::
   :artefacto: DECISIONES-HABILITAR-JEST-IACT-UI
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/habilitar-jest-iact-ui
   :repo_objetivo: IACT-ui
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:52:11
   :ultimo_cambio: 2026-05-19T18:52:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-habilitar-jest-iact-ui:

==============================================================
Decisiones: Habilitar jest en IACT-ui
==============================================================

Decisiones de diseno
=====================

D1 — Warnings de transitivas no se atacan en esta iniciativa
--------------------------------------------------------------

``npm install`` emite 3 warnings:
``inflight@1.0.6``, ``glob@7.2.3``, ``fstream@1.0.12``,
todas dependencias transitivas (no aparecen en
``package.json`` directo). El consejo de npm es actualizar a
``lru-cache``, ``glob@10+`` y desupporting ``fstream``.

Considerado: forzar resolutions/overrides en
``package.json`` para silenciar las warnings. Se descarto:
implica cambios versionados en ``package.json`` /
``package-lock.json``, fuera del scope runtime de esta
iniciativa. Las warnings no bloquean tests (2381 pasan).

Decision tomada: registrar como deuda nueva
(`DEBT-FUTURE-NPM-DEPS`) y dejar el `package.json` intacto.
Si los warnings molestan en CI, una iniciativa de
saneamiento de dependencias puede atacarlas en bloque.

D2 — npm install con --no-audit y --no-fund
---------------------------------------------

Por defecto ``npm install`` ejecuta audit (peticion HTTP a
``registry.npmjs.org``) y muestra mensajes de fund. Ambos
generan ruido durante la sesion runtime y no aportan a la
iniciativa.

Decision tomada: ``--no-audit --no-fund`` en T-001. Se
documenta para reproducibilidad.

D3 — Patron Modelo C-runtime sin re-justificar
------------------------------------------------

Iniciativas hermanas ya establecieron el patron
(``:repo_objetivo: <repo>`` sin commit en el repo objetivo;
documentacion en IACT-docs por D3 Modelo C de PROC-GOB-013
v2.0.0). Esta iniciativa lo aplica sin duplicar la
justificacion. Las decisiones D1, D2, D3 de
``preparar-entorno-mariadb-ivr-legacy`` y la D2 de
``preparar-entorno-postgresql-iact-analytics`` aplican aqui
por referencia.

Hallazgos durante la ejecucion
================================

H-E1 — Tres deprecaciones de transitivas
------------------------------------------

Detectadas en T-001 (npm install). No accionadas (D1).

H-E2 — Sin warnings de "ERR" — instalacion limpia
---------------------------------------------------

Pese a 1357 paquetes, no hay un solo error duro durante
``npm install``. Es estado saludable que debe preservarse
en futuras actualizaciones de ``package.json``.

H-E3 — 250 test suites en una sola ejecucion (no paralelizadas explicitamente)
-------------------------------------------------------------------------------

Jest ejecuta los 250 suites con configuracion default
(workers automatico) en 29.88 segundos. La iniciativa no
forza ``--maxWorkers`` ni ``--runInBand``. Es velocidad
saludable para un contenedor.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - node_modules/ poblado
     - PASA
     - "added 1357 packages in 16s" tras
       ``npm install``.
   * - npm test sin fallas
     - PASA
     - "Test Suites: 250 passed, 250 total";
       "Tests: 2381 passed, 2381 total";
       "Time: 29.88 s".

Deuda nueva registrada
========================

* **DEBT-FUTURE-NPM-DEPS**: 3 warnings de deprecacion
  (inflight, glob@7, fstream) en transitivas. Iniciativa
  candidata: ``sanear-deuda-deps-npm-iact-ui``.
* **DEBT-FUTURE-UI-LINT**: ``npm run lint`` no se ejecuto
  en esta iniciativa. Candidato a iniciativa propia.
* **DEBT-FUTURE-UI-E2E**: tests E2E que integren con
  IACT-api real (no mocks) no existen aun. Necesita
  pensarse — la arquitectura de tests E2E depende de como
  se levante el stack.
* **DEBT-FUTURE-UI-BUILD-PROD**: ``npm run build`` no se
  ejecuto. Verifica que el bundle production-ready
  funcione.

Conclusion
==========

La cadena ``db -> api -> ui`` esta completa. Cada eslabon
tiene su iniciativa cerrada con evidencia ejecutable:

* db (par MariaDB + PostgreSQL): ``preparar-entorno-mariadb-ivr-legacy``,
  ``preparar-entorno-postgresql-iact-analytics``.
* api: ``habilitar-pytest-iact-api`` (223 unit tests pass).
* ui: esta iniciativa (2381 jest tests pass).

Mas la iniciativa estructural
``evolucionar-proc-gob-013-multirepo`` (PROC-GOB-013 v2.0.0,
campo ``:repo_objetivo:`` formal) que habilito el Modelo C
runtime para que estas iniciativas pudieran existir
trazablemente sin commits en el repo objetivo.

Cinco iniciativas cerradas en una sesion. El sistema IACT
esta operativo para validar cambios futuros con tests reales.
