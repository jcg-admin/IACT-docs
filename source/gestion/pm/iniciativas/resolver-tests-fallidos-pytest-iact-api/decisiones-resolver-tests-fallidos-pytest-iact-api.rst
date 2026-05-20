.. meta::
   :artefacto: DECISIONES-RESOLVER-TESTS-FALLIDOS-PYTEST-IACT-API
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-tests-fallidos-pytest-iact-api
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:42:40
   :ultimo_cambio: 2026-05-19T19:42:40
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-resolver-tests-fallidos-pytest-iact-api:

==============================================================
Decisiones: Resolver Tests Fallidos + UI Build
==============================================================

Decisiones de diseno
=====================

D1 — Ataque por causa raiz, no test por test
----------------------------------------------

Las 67 fallas iniciales no eran 67 bugs distintos. Tres
categorias dominantes con causa raiz comun:

* 29 fallas: DML denied en ``test_ivr_legacy`` (un fix de
  grants).
* 8 fallas: ``pyo3_runtime.PanicException`` cryptography
  mix system/venv (un fix de pip).
* Algunas fallas en alerts: Function.module FK recibia
  string (un fix de fixture, replicado en 3 setUp del
  archivo).

Considerado: investigar y arreglar test por test. Se
descarto: explora un patron, replica fix sin entender la
causa, multiplica el costo sin reducir deuda real.

Decision tomada: identificar la causa raiz dominante de
cada bucket, aplicar el fix unitario y medir reduccion.
Las fallas residuales (30) son individuales — no comparten
patron mayoritario.

D2 — UI build atacado en paralelo aunque no estaba en el alcance original
---------------------------------------------------------------------------

Sponsor pidio "api y ui en paralelo, mejor decision". La
verificacion proactiva de ``npm run build`` revelo deuda
no documentada: 44 errores. La iniciativa hermana
``habilitar-jest-iact-ui`` habia registrado
``DEBT-FUTURE-UI-BUILD-PROD`` pero sin ejecutar el build
para verificar — la registro como "no ejecutado" y la
diferio. La iniciativa anterior
``sanear-deuda-runtime-multirepo`` tampoco ejecuto el
build.

Decision tomada: incluir el fix de UI build en esta
iniciativa. Es deuda real (production bundle roto), trivial
de diagnosticar (jest vs webpack alias drift) y critica
para que IACT-ui sea deployable. No tiene sentido diferirla
mas.

D3 — Cryptography reinstall NO se persiste como cambio de codigo
------------------------------------------------------------------

``cryptography 41.0.7`` lo provee Debian (sin
RECORD file). El venv lo veia importado desde
``/usr/lib/python3/dist-packages/cryptography`` por orden
de sys.path en el entorno del contenedor.
``--force-reinstall --ignore-installed`` instalo la 48.0.0
en el venv, eliminando el panico.

Considerado: pinar ``cryptography==X`` en
``requirements/base.txt``. Se descarto: la dep ya estaba
declarada (transitiva de pyca, de psycopg2 etc.). El
problema es ambiental, no de requirements declarados. Si
otro entorno tiene cryptography limpio en venv, no necesita
el reinstall.

Decision tomada: documentar el fix como T-002 con accion
runtime (no commit). Si reaparece en otro entorno, el
runbook lo replica.

D4 — alerts test fix solo en test_viewsets.py, no global
----------------------------------------------------------

El patron ``module='MOD_Alerts'`` puede existir en otros
test files. Considerado: grep global y fixar todos los
sites de una vez.

Se descarto: solo test_viewsets.py.py estaba fallando con
ese sintoma. Otros tests de alerts (test_models.py,
test_services.py) fallan con otros sintomas. Fixar
multiples archivos en una iniciativa diluye el foco y mezcla
diagnosticos. Las fallas de los otros archivos quedan en
buckets separados.

D5 — react-select como dep prod, no devDependency
---------------------------------------------------

``react-select`` se importa en codigo de produccion
(``src/components/DateTimeInputs/SelectDropdown.jsx``).
Tiene que ir en ``dependencies``, no en
``devDependencies``. ``npm install --save`` la coloco bien
por default.

D6 — Fix SCSS por transicion expandida, no por nueva variante de mixin
------------------------------------------------------------------------

Considerado: anadir ``@mixin transition-medium-multi($p1,
$p2) { ... }`` para soportar el caso de 2 propiedades.

Se descarto: cambio en codigo compartido (variables/),
puede afectar otros consumidores. La transicion expandida
inline en los 2 archivos afectados es trivial, contextual
y no introduce nueva superficie API.

Hallazgos durante la ejecucion
================================

H-E1 — alerts test fix replica el patron 3 veces en el mismo archivo
---------------------------------------------------------------------

El mismo bug ``module='MOD_Alerts'`` aparece en 3 setUp
distintos (InternalMessage, AlertConfiguration,
AlertSubscription) del mismo archivo. Cada uno necesito
edit explicito. Sugiere refactor a fixture comun, fuera
del scope.

H-E2 — overrides de glob no afecta a inflight/fstream
------------------------------------------------------

Ya identificado en sanear-deuda-runtime-multirepo D2:
inflight y fstream subsisten como warnings. Verificacion
post-rebuild de UI tras los fixes: warnings residuales
mantenidos pero no bloqueantes.

H-E3 — dashboard 404 != 200 sugiere URL routing missing
---------------------------------------------------------

14 fallas en apps/dashboard/tests/test_viewsets.py con
patron ``AssertionError: 404 != 200``. Sugiere URL
patterns no registrados o app config faltante. Investigacion
out-of-scope; iniciativa dedicada
``resolver-tests-dashboard-iact-api``.

H-E4 — IACT-db setup.sh ahora otorga DML que CNST-003 no menciona
-------------------------------------------------------------------

CNST-003 dice "produccion read-only en ivr_legacy". El fix
otorga DML en ``test_ivr_legacy`` (no en ivr_legacy). No
viola CNST-003 — son BDs distintas. Pero el reporter del
setup.sh paso de "SELECT en ivr_legacy + CREATE/DROP en
test_ivr_legacy" a "SELECT en ivr_legacy + DDL+DML en
test_ivr_legacy" para reflejar la realidad.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 40 12 48

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - npm run build 0 errores
     - PASA
     - "webpack 5.106.2 compiled with 21 warnings
       in 4632 ms" (0 errors).
   * - npm test sigue verde
     - PASA
     - "Test Suites: 250 passed; Tests: 2381
       passed; 18.9s".
   * - DML grants aplicados
     - PASA
     - setup.sh ahora otorga
       SELECT/INSERT/UPDATE/DELETE en
       test_ivr_legacy.* a django_user.
   * - cryptography venv consistente
     - PASA
     - import path
       /home/user/IACT-api/.venv/lib/python3.11/site-packages/cryptography
       version 48.0.0.
   * - alerts fixture FK corregida
     - PASA
     - Function.module ahora recibe instance
       Module en 3 setUp del archivo
       test_viewsets.py.
   * - Conteo total fallas pytest
     - 30 (vs 67 inicial)
     - 1367 passed, 30 failed, 97.85% pass.
   * - Fallas resueltas
     - 37 (55%)
     - 29 (DML) + 8 (cryptography) +
       2 (alerts FK parcial).

Deuda residual y nuevas iniciativas candidatas
================================================

Las 30 fallas residuales pytest son individuales y no
comparten causa raiz dominante. Buckets:

* **resolver-tests-dashboard-iact-api**:
  apps/dashboard/tests/* 17 fallas (test_viewsets 14,
  test_dashboard_service 2, test_signals 1). Causa
  predominante: AssertionError 404 != 200 (URL routing).
* **resolver-tests-alerts-residual-iact-api**:
  apps/alerts/tests/* 14 - 2 = 6 fallas residuales
  (test_viewsets 6, test_models 4, test_services 1,
  test_scheduler 1). Causas individuales.
* **resolver-tests-pipeline-ivr-iact-api**:
  tests/integration/pipeline/* 5 fallas residuales.
  Tras el fix DML, las restantes son test logic
  (quarter validation, heartbeat timeout).

Adicional registrada:

* **sanear-sass-deprecations-iact-ui**: warnings de
  ``@import`` y ``darken()`` deprecadas en Dart Sass
  3.0.0. ~63 deprecation warnings en build.
* **sanear-eslint-warnings-iact-ui**: 204 eslint
  warnings (todas ``react/prop-types`` o
  ``no-unused-vars``).
* **dedupe-fixtures-alerts-iact-api**: 3 setUp
  identicos en test_viewsets.py de alerts comparten el
  mismo fixture Module. Refactor a conftest.py o
  fixture base.

Conclusion
==========

Pasa de 67 fallas pytest a 30 (55% reducidas) +
restauracion completa de UI build prod (deuda no
documentada eliminada). Tres commits cross-repo en
IACT-api / IACT-db / IACT-ui mas documentacion en
IACT-docs.

La deuda restante esta cuantificada por bucket con causa
raiz identificada, lista para iniciativas individuales del
sponsor. No queda deuda observable sin contorno.
