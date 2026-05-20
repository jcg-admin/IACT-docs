.. meta::
   :artefacto: PLAN-FASES-TAREAS-INICIATIVAS-PENDIENTES
   :tipo: Plan
   :dominio: gestion
   :subdominio: pm/iniciativas/plan-maestro-iniciativas-pendientes
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:58:52
   :ultimo_cambio: 2026-05-19T20:58:52
   :autor: NestorMonroy
   :clasificacion: Interno

.. _plan-fases-tareas-iniciativas-pendientes:

==============================================================
Plan: FASES y Tareas Atomicas por Iniciativa Pendiente
==============================================================

Indice de iniciativas pendientes
==================================

.. list-table::
   :header-rows: 1
   :widths: 6 36 14 14 12 18

   * - #
     - Iniciativa
     - Repo
     - Origen
     - Prioridad
     - Categoria
   * - 1
     - resolver-tests-dashboard-residual-iact-api
     - IACT-api
     - resolver-tests-dashboard
     - P1
     - Fix tests
   * - 2
     - resolver-tests-alerts-residual-iact-api
     - IACT-api
     - resolver-tests-fallidos
     - P1
     - Fix tests
   * - 3
     - resolver-tests-pipeline-residual-iact-api
     - IACT-api
     - resolver-tests-fallidos
     - P1
     - Fix tests
   * - 4
     - sanear-pytest-config-iact-api
     - IACT-api
     - sanear-deuda-runtime
     - P2
     - Config
   * - 5
     - sanear-deuda-deps-npm-iact-ui
     - IACT-ui
     - sanear-deuda-runtime
     - P2
     - Deps
   * - 6
     - sanear-sass-deprecations-iact-ui
     - IACT-ui
     - resolver-tests-fallidos
     - P3
     - Build warnings
   * - 7
     - sanear-eslint-warnings-iact-ui
     - IACT-ui
     - resolver-tests-fallidos
     - P3
     - Lint
   * - 8
     - dedupe-fixtures-alerts-iact-api
     - IACT-api
     - resolver-tests-fallidos
     - P3
     - Refactor tests
   * - 9
     - documentar-ucs-implementados-no-declarados
     - IACT-docs
     - verificar-mapping
     - P2
     - Doc inverso
   * - 10
     - aclarar-duplicacion-perm-03-acc-08
     - IACT-api
     - verificar-mapping
     - P2
     - Refactor
   * - 11
     - alinear-numeracion-uc-api-ui
     - multiple
     - verificar-mapping
     - P3
     - Convencion
   * - 12
     - auditar-componentes-ui-sin-marker
     - IACT-ui
     - auditar-cobertura
     - P2
     - Audit
   * - 13
     - separar-ucs-inclusion-de-user-facing
     - IACT-docs
     - aclarar-uc-047
     - P3
     - Convencion docs
   * - 14
     - enumerar-otros-ucs-inclusion
     - IACT-docs
     - aclarar-uc-047
     - P2
     - Audit
   * - 15
     - documentar-stubs-en-rst-de-uc
     - IACT-docs
     - implementar-uc-rpt-05-06
     - P3
     - Doc
   * - 16
     - revisar-cnst-004-realtime-metrics
     - IACT-docs
     - implementar-uc-rpt-05-06
     - P4
     - Sponsor decision
   * - 17
     - normalizar-convencion-tst-ref-fr
     - IACT-docs
     - declarar-tst-ref-58
     - P3
     - Doc convencion
   * - 18
     - implementar-tst-fr-conformidad-por-dominio
     - IACT-api
     - auditar-conformidad-fr
     - P1
     - Tests + conformidad
   * - 19
     - ci-gate-conformidad-fr-tests
     - IACT-api
     - auditar-conformidad-fr
     - P2
     - CI
   * - 20
     - auditar-iniciativas-previas-bajo-grep-validado
     - IACT-docs
     - adoptar-protocolo-grep
     - P2
     - Audit retrospectivo

Convencion de FASES
=====================

PROC-GOB-013 v2.0.0 declara 5 fases del ciclo de
iniciativa:

* **Fase 1 — DISCOVER**: leer estado actual, identificar
  observables.
* **Fase 2 — SCOPE**: decidir estructura RST y alcance
  in/out.
* **Fase 3 — ESTRUCTURA**: crear archivos RST + enlazar
  toctree.
* **Fase 4 — EJECUTAR**: aplicar las tareas T-NNN.
* **Fase 5 — CIERRE**: actualizar progreso, decisiones,
  build limpio, commit + push.

Cada bloque abajo declara las tareas de **Fase 4** (las
demas son procedimentales segun PROC-GOB-013). Si una
iniciativa requiere fases especiales (auditoria
profunda, decision arquitectonica), se indica
explicitamente.

----

P1 — Resolver tests fallidos (3 iniciativas, 19 tests)
========================================================

#1 — resolver-tests-dashboard-residual-iact-api
-------------------------------------------------

**Repo:** IACT-api. **Tests afectados:** 10
en ``apps/dashboard/tests/``.

Tareas Fase 4:

* **T-001:** Inspeccionar
  ``test_list_dashboards_authenticated`` y verificar si
  la falla es pagination contract (espera ``list``,
  recibe ``OrderedDict``) o assertion delta. Fix segun
  diagnostico. Archivo:
  ``apps/dashboard/tests/test_viewsets.py``.
* **T-002:** Idem
  ``test_list_dashboards_unauthenticated``.
* **T-003..T-009:** Para cada uno de los 7 tests
  restantes (test_create_dashboard, test_clone_action,
  test_update_own_dashboard, test_update_other_dashboard,
  test_retrieve_own, test_retrieve_public,
  test_set_default_action), diagnostico individual +
  fix.
* **T-010:** Si el patron de fallas converge (e.g.
  todos por pagination), refactor a fixture comun en
  ``conftest.py``.
* **T-011:** Re-run pytest, verificar 0 dashboard
  fallas. Archivo verificable: log de pytest output.
* **T-012:** Documentar en
  ``decisiones-resolver-tests-dashboard-residual.rst``.

#2 — resolver-tests-alerts-residual-iact-api
----------------------------------------------

**Repo:** IACT-api. **Tests afectados:** 8
(test_viewsets 2, test_models 4, test_services 1,
test_scheduler 1).

Tareas Fase 4:

* **T-001:** ``test_create_message_endpoint`` —
  diagnostico (puede ser permission_django no asignado).
  Archivo: ``apps/alerts/tests/test_viewsets.py``.
* **T-002:** ``test_mark_read_endpoint`` — diagnostico.
  Mismo archivo.
* **T-003..T-006:** Cada uno de los 4
  ``test_models.py`` failures. Archivo:
  ``apps/alerts/tests/test_models.py``.
* **T-007:** ``test_services.py`` falla.
* **T-008:** ``test_scheduler.py`` falla.
* **T-009:** Re-run pytest alerts, verificar 0 fallas.
* **T-010:** Decisiones + cierre.

#3 — resolver-tests-pipeline-residual-iact-api
------------------------------------------------

**Repo:** IACT-api. **Tests afectados:** 2-4
(``test_quarter_valido_retorna_filas`` en
TestIVRMenuRedirected/MenuCenter + heartbeat).

Tareas Fase 4:

* **T-001:** Verificar si ``base_ivr_detalle`` tiene
  datos del quarter esperado por el test
  (probablemente Q01_25 — fixture ``ivr_quarter_data``).
* **T-002:** Si la fixture poblo correctamente pero
  los SPs no retornan, inspeccionar el SP
  ``sp_rpt_menu_redirigidos`` con sus 2 argumentos
  esperados (signature check).
* **T-003:** Para heartbeat tests, verificar config
  del ``IVR_QUERY_TIMEOUT_SEC`` y mock del clock si
  aplica.
* **T-004:** Re-run pytest pipeline, verificar 0.
* **T-005:** Decisiones + cierre.

----

P2 — Saneamiento estructural (5 iniciativas)
==============================================

#4 — sanear-pytest-config-iact-api
-------------------------------------

**Repo:** IACT-api. Objetivo: cambiar default de
``pytest.ini`` de ``--reuse-db`` a ``--create-db`` o
documentar la diferencia; revisar default
``DJANGO_SETTINGS_MODULE`` en ``manage.py``.

Tareas Fase 4:

* **T-001:** Cambiar ``pytest.ini`` line 6 de
  ``addopts: --reuse-db --strict-markers`` a
  ``--create-db --strict-markers``. Archivo:
  ``callcentersite/pytest.ini``.
* **T-002:** Medir impacto en tiempo de suite
  (esperado: +30-60s por full run; --create-db evita
  los 932 errores de cross-marker pollution).
* **T-003:** Cambiar default de manage.py de
  ``config.settings.development`` a
  ``config.settings.testing_local``. Archivo:
  ``callcentersite/manage.py``.
* **T-004:** Verificar que ``./manage.py runserver``
  sigue funcionando con override
  ``DJANGO_SETTINGS_MODULE=development`` para flujo
  dev. Documentar en README.
* **T-005:** Decisiones + cierre.

#5 — sanear-deuda-deps-npm-iact-ui
-------------------------------------

**Repo:** IACT-ui. Objetivo: eliminar warnings de
``inflight``, ``fstream``, ``lodash.isequal``,
``whatwg-encoding``, ``uuid@8``.

Tareas Fase 4:

* **T-001:** ``npm outdated`` para inventario.
  Captura como log.
* **T-002:** Identificar el paquete top-level que
  trae cada transitivo deprecado. ``npm ls inflight
  --all``.
* **T-003:** Actualizar cada paquete top-level a la
  ultima version compatible que ya no use la
  transitiva deprecada. Archivo: ``package.json``.
* **T-004:** ``npm install`` y verificar warnings
  reducidas. Captura log.
* **T-005:** ``npm test`` y ``npm run build`` para
  asegurar sin regresion.
* **T-006:** Decisiones + cierre.

#9 — documentar-ucs-implementados-no-declarados
--------------------------------------------------

**Repo:** IACT-docs. Objetivo: crear RST docs para los
~8 markers en codigo sin contraparte en
``requisitos-funcionales/``.

Markers a documentar (verificados):

* UC_ACC_03 (Permisos del usuario)
* UC_ACC_04 (Asignar agrupador)
* UC_ACC_05 (Reglas de Separacion de Funciones)
* UC_LOG_08 (Eventos del pipeline analitico)
* UC_PIP_05 (Gestionar configuracion job ETL)
* UC_USR_05, 06, 07 (UI extras, sin descripcion clara)

Tareas Fase 4:

* **T-001:** Crear
  ``source/requisitos/requisitos-funcionales/access/uc-NNN-permisos-usuario-alias/index.rst``
  + ``fr-NNN-01-*.rst`` para UC_ACC_03. Numero
  asignar (puede ser uc-024-permisos-usuario o
  reservado).
* **T-002..T-005:** Idem para UC_ACC_04, UC_ACC_05,
  UC_LOG_08, UC_PIP_05.
* **T-006..T-008:** Inspeccionar UC_USR_05/06/07 en
  IACT-ui/src (que feature implementan) y decidir si
  documentar como UC o como helper UI. Si UC, crear
  RST.
* **T-009:** Actualizar ``index.rst`` del dominio
  correspondiente.
* **T-010:** sphinx-build dummy 0 warnings.
* **T-011:** Decisiones + cierre.

#10 — aclarar-duplicacion-perm-03-acc-08
------------------------------------------

**Repo:** IACT-api. Objetivo: determinar si
``UC_PERM_03`` y ``UC_ACC_08`` son endpoints
distintos (Preview vs Conceder real) o duplicacion
accidental.

Tareas Fase 4:

* **T-001:** Leer
  ``apps/permissions/.../views.py`` que declara
  UC_PERM_03.
* **T-002:** Leer
  ``apps/access/.../views.py`` que declara
  UC_ACC_08.
* **T-003:** Cruzar con FR-014.NN
  (``requisitos-funcionales/permissions/uc-014-conceder-permiso-excepcional-perm/fr-014-*.rst``)
  para identificar si los pasos del UC se reparten
  entre ambos endpoints o si uno es legacy.
* **T-004:** Si son distintos endpoints
  intencionales: documentar separacion en el RST de
  uc-014. Archivo:
  ``uc-014-conceder-permiso-excepcional-perm/index.rst``.
* **T-005:** Si es duplicacion: deprecar el menos
  usado, mantener el otro. Marcar uno con
  ``@extend_schema(deprecated=True)``.
* **T-006:** Tests para asegurar el path correcto.
* **T-007:** Decisiones + cierre.

#12 — auditar-componentes-ui-sin-marker
------------------------------------------

**Repo:** IACT-ui. Objetivo: para los 9-13 UCs que
tienen api pero no se detectaron en UI con marker,
verificar si hay componente UI sin tag (gap real vs
solo marker faltante).

UCs candidatos: UC_AUTH_04, UC_PERM_01/06/09,
UC_RPT_08, 13, 14, 15, 16, 17.

Tareas Fase 4:

* **T-001:** Para UC_AUTH_04 (cambiar password):
  buscar ``src/pages/auth/ChangePassword.jsx``;
  si existe, anadir marker UC_AUTH_04 en
  ``@uc`` JSDoc o comentario top-level.
* **T-002..T-010:** Idem para cada uno de los otros 9
  UCs. Un archivo Edit por UC para anadir marker.
* **T-011:** Re-grep con protocolo grep-validado
  (rules/grep-validated-audit.md) para confirmar
  cobertura UI actualizada.
* **T-012:** ``npm test`` sin regresion.
* **T-013:** Decisiones + cierre.

#14 — enumerar-otros-ucs-inclusion
------------------------------------

**Repo:** IACT-docs. Objetivo: verificar si hay otros
UCs con prefijo ``UC_INC_*`` no contados en la
auditoria original.

Tareas Fase 4:

* **T-001:** Grep en docs:
  ``grep -rohE "UC_INC_[A-Z]+_[0-9]+"
  source/requisitos/ | sort -u``. Output a log.
* **T-002:** Para cada UC_INC encontrado, leer su
  RST para confirmar es inclusion (no user-facing).
* **T-003:** Listar inclusion UCs y consultar al
  sponsor cuales quedan OUT del scope.
* **T-004:** Actualizar el deep-analysis de
  ``aclarar-uc-047-resolver-segmento`` con la lista
  completa.
* **T-005:** Actualizar el conteo total in-scope
  segun resolucion del sponsor.
* **T-006:** Decisiones + cierre.

#19 — ci-gate-conformidad-fr-tests
------------------------------------

**Repo:** IACT-api. Objetivo: gate de CI que verifica
cada FR-NNN.NN tiene al menos un test marcado con
``@pytest.mark.tst_fr("FR-NNN.NN")``.

Tareas Fase 4:

* **T-001:** Crear ``scripts/check_fr_coverage.py``
  que: (a) enumera FRs de docs, (b) extrae markers
  pytest tst_fr del codigo, (c) reporta FRs sin
  test asociado.
* **T-002:** Anadir step a ``.github/workflows/validate.yml``
  que ejecuta el script y falla si hay FRs
  descobertos.
* **T-003:** Documentar el gate en
  ``source/normativa/procedimientos/proc-doc-014-conformidad-fr.rst``
  nuevo.
* **T-004:** Aplicar gate desactivado (warning-only)
  primero, activado bloqueante tras
  implementar-tst-fr-conformidad-por-dominio.
* **T-005:** Decisiones + cierre.

#20 — auditar-iniciativas-previas-bajo-grep-validado
------------------------------------------------------

**Repo:** IACT-docs. Objetivo: re-auditar las 15
iniciativas cerradas en esta sesion aplicando el
protocolo ``grep-validated-audit.md`` para detectar
cualquier claim SPECULATIVE remanente.

Tareas Fase 4:

* **T-001..T-015:** Por cada iniciativa cerrada,
  abrir su deep-analysis y aplicar la checklist de 6
  items pre-publicacion. Marcar claims que no
  cumplen como SPECULATIVE.
* **T-016:** Consolidar lista de claims SPECULATIVE
  detectados.
* **T-017:** Para cada claim, abrir sub-iniciativa
  de validacion o aceptar como deuda.
* **T-018:** Decisiones + cierre.

----

P3 — Mejoras de calidad (6 iniciativas)
=========================================

#6 — sanear-sass-deprecations-iact-ui
---------------------------------------

**Repo:** IACT-ui. Warnings: ``@import`` deprecado,
``darken()`` deprecado, total ~63 warnings.

Tareas Fase 4:

* **T-001:** Reemplazar ``@import 'archivo'`` por
  ``@use 'archivo'`` en cada SCSS donde aparezca.
  Aproximadamente 20-30 archivos.
* **T-002:** Reemplazar ``darken($color, X%)`` por
  ``color.adjust($color, $lightness: -X%)``.
* **T-003:** ``npm run build`` para verificar
  warnings reducidas.
* **T-004:** ``npm test`` sin regresion.
* **T-005:** Decisiones + cierre.

#7 — sanear-eslint-warnings-iact-ui
-------------------------------------

**Repo:** IACT-ui. 204 warnings (react/prop-types,
no-unused-vars).

Tareas Fase 4:

* **T-001:** ``npm run lint -- --fix`` para 6
  warnings auto-fixable.
* **T-002:** Para warnings ``react/prop-types``:
  decidir si anadir PropTypes a cada componente
  (trabajo masivo) o silenciar la regla por
  ``eslint-disable-next-line`` con justificacion (TS
  migration pendiente).
* **T-003:** Para warnings ``no-unused-vars``:
  eliminar variables / parametros realmente no
  usados, o anadir ``_`` prefix donde son
  intencionales.
* **T-004:** ``npm run lint`` con 0 warnings o
  warnings documentadas.
* **T-005:** Decisiones + cierre.

#8 — dedupe-fixtures-alerts-iact-api
--------------------------------------

**Repo:** IACT-api. Refactor: 3 setUp identicos en
``apps/alerts/tests/test_viewsets.py`` para creacion
de Module + Function RBAC.

Tareas Fase 4:

* **T-001:** Crear ``apps/alerts/tests/conftest.py``
  con fixture ``module_alerts`` y ``function_*``
  reutilizables. Archivo nuevo.
* **T-002:** Refactorizar
  ``InternalMessageViewSetTest.setUp`` para usar la
  fixture. Archivo:
  ``apps/alerts/tests/test_viewsets.py``.
* **T-003:** Idem ``AlertConfigurationViewSetTest``.
* **T-004:** Idem ``AlertSubscriptionViewSetTest``.
* **T-005:** ``pytest -m unit apps/alerts/`` sin
  regresion (8 fallas se mantienen o reducen).
* **T-006:** Decisiones + cierre.

#11 — alinear-numeracion-uc-api-ui
-------------------------------------

**Repos:** IACT-api + IACT-ui. UC_USR_05, 06, 07
existen en UI sin contraparte api. Resolucion:
documentar el por que de cada uno o eliminar el
marker en UI si es obsoleto.

Tareas Fase 4:

* **T-001:** Grep en IACT-ui para cada UC_USR_05/06/07
  con contexto (10 lineas antes/despues) para
  entender que feature implementan.
* **T-002:** Si son features UI-only (settings,
  preferencias): documentar como UC en docs nuevos
  con prefijo ``uc-ui-*`` o etiquetar como
  ``UC_UI_USR_NN`` (UI-only namespace).
* **T-003:** Si son obsoletos: eliminar markers
  remanentes de IACT-ui/src.
* **T-004:** ``npm test`` sin regresion.
* **T-005:** Decisiones + cierre.

#13 — separar-ucs-inclusion-de-user-facing
---------------------------------------------

**Repo:** IACT-docs. Convencion estructural: UCs INC
deben estar visualmente separados de user-facing.

Tareas Fase 4:

* **T-001:** Decidir convencion: subdirectorio
  ``inclusion/`` dentro de cada dominio O prefijo
  ``uc-inc-*`` en el nombre del directorio. Doc
  decision.
* **T-002:** Mover ``uc-047-resolver-segmento-usuario``
  a la nueva ubicacion (e.g.
  ``reports/inclusion/uc-047-resolver-segmento-usuario/``).
* **T-003:** Actualizar todos los toctree y links
  que referencien uc-047.
* **T-004:** Aplicar a cualquier otro UC_INC
  encontrado por #14 (depende de #14 cerrada).
* **T-005:** Actualizar PROC-GOB-013 o crear
  ``proc-gob-015-ucs-inclusion.rst`` con la
  convencion formal.
* **T-006:** sphinx-build 0 warnings.
* **T-007:** Decisiones + cierre.

#15 — documentar-stubs-en-rst-de-uc
-------------------------------------

**Repo:** IACT-docs. UCs implementados como STUB
deben declararlo en su RST.

Tareas Fase 4:

* **T-001:** Identificar todos los STUBs en codigo:
  ``grep -irE "STUB" apps/`` para casos como
  UC_RPT_02 (real-time metrics por CNST-004).
* **T-002:** Para cada STUB detectado, anadir
  admonicion ``.. warning:: STUB`` al RST del UC
  correspondiente con justificacion (CNST aplicable).
* **T-003:** Aplicar primero a uc-033 (UC_RPT_02
  real-time metrics).
* **T-004:** sphinx-build 0 warnings.
* **T-005:** Decisiones + cierre.

#17 — normalizar-convencion-tst-ref-fr
-----------------------------------------

**Repo:** IACT-docs. Dos convenciones coexisten:
``TST-FR-NNN.NN`` (uppercase + punto, 45 FRs) vs
``TST-fr-NNN-NN`` (lowercase + guion, 58 FRs).
Decision del sponsor sobre cual es canonica.

Tareas Fase 4:

* **T-001:** Consultar sponsor: cual convencion es
  canonica? (recomendable lowercase + guion porque
  es la mayoria — 58 vs 45).
* **T-002:** ``sed`` masivo para normalizar los
  archivos de la minoria a la canonica.
* **T-003:** sphinx-build 0 warnings tras la
  normalizacion.
* **T-004:** Documentar la convencion en STD-007
  (``source/normativa/estandares/std-007-convencion-naming.rst``)
  con la regla TST-NNN.
* **T-005:** Decisiones + cierre.

----

P4 — Decision arquitectonica (1 iniciativa)
=============================================

#16 — revisar-cnst-004-realtime-metrics
------------------------------------------

**Repo:** IACT-docs. Decision del sponsor: revisitar
CNST-004 (NO Channels, NO Celery, NO Redis) para
habilitar UC_RPT_02 real-time o aceptar el STUB
permanente.

Esta iniciativa es **NO ejecutable por agente sin
input del sponsor**. Las tareas son de analisis y
documentacion para entregar al sponsor.

Tareas Fase 4 (orientadas a producir analisis para
decision, no a ejecutar la decision):

* **T-001:** Documento de analisis costo/beneficio
  CNST-004:

  - Mantener CNST-004 (STUB): costo 0, valor 0,
    riesgo arquitectonico 0.
  - Permitir Channels (ASGI): costo
    infraestructura (daphne / uvicorn + reverse
    proxy SSE), valor real-time, riesgo seguridad +
    operacional + complejidad.

* **T-002:** Documento de alternativas:

  - Long-polling como pseudo-real-time (sin
    Channels).
  - Server-Sent Events sobre WSGI streaming
    response (sin Channels formales).
  - REST polling cada N segundos (UC_RPT_01
    dashboard ya cumple eso).

* **T-003:** Entregar documento al sponsor en
  ``source/gestion/decisiones-pendientes/decision-cnst-004-realtime.rst``.
* **T-004:** Pause hasta resolucion del sponsor.

----

P1 (separado por escala) — implementar-tst-fr-conformidad-por-dominio
=======================================================================

**#18 — Iniciativa madre con 9 sub-iniciativas (1 por
dominio).** 103 FRs in-scope -> 103 tests nuevos
minimo (1 por FR) + decorador
``@pytest.mark.tst_fr``.

Estructura:

* **18.1** — implementar-tst-fr-auth (5 FRs UC, ~21
  FRs sub)
* **18.2** — implementar-tst-fr-users (4 UCs, 17 FRs)
* **18.3** — implementar-tst-fr-access (2 UCs, 7 FRs)
* **18.4** — implementar-tst-fr-permissions (10 UCs,
  22 FRs)
* **18.5** — implementar-tst-fr-reports (16 UCs, 16
  FRs)
* **18.6** — implementar-tst-fr-alerts (5 UCs, 5 FRs)
* **18.7** — implementar-tst-fr-audit (4 UCs, 4 FRs)
* **18.8** — implementar-tst-fr-logs (7 UCs, 7 FRs)
* **18.9** — implementar-tst-fr-pipeline (4 UCs, 4
  FRs)

Total: ~103 tests nuevos. Trabajo masivo (~3-5 dias
con buen ritmo si los FRs son claros, ~2 semanas si
hay ambiguedad en criterios de aceptacion).

Tareas Fase 4 por dominio (patron repetido):

* **T-001:** ``pip install pytest-tst-fr-marker``
  (o crear el marker custom en
  ``conftest.py`` raiz si no existe). Archivo:
  ``callcentersite/conftest.py``.
* **T-002..T-N (uno por FR del dominio):**
  Implementar test con marker
  ``@pytest.mark.tst_fr("FR-NNN.NN")`` que valida
  el criterio de aceptacion del FR
  correspondiente. Archivo: tests/conformidad/
  ``test_fr_NNN_NN_*.py``.
* **T-N+1:** Re-run pytest con marker filter
  ``pytest -m tst_fr`` para confirmar todos pasan.
* **T-N+2:** Update RST del FR cambiando "(pendiente)"
  por la fecha de implementacion.
* **T-N+3:** Decisiones + cierre.

----

Resumen agregado del plan
==========================

.. list-table::
   :header-rows: 1
   :widths: 16 12 16 16 40

   * - Prioridad
     - Iniciativas
     - Tareas estimadas
     - Repos
     - Categoria
   * - P1
     - 4 (1-3 + 18)
     - 30 + 103 = 133
     - IACT-api
     - Tests + conformidad
   * - P2
     - 7 (4-5, 9-10, 12, 14, 19-20)
     - ~70
     - multiple
     - Saneamiento estructural
   * - P3
     - 6 (6-8, 11, 13, 15, 17)
     - ~40
     - multiple
     - Calidad
   * - P4
     - 1 (16)
     - 4
     - IACT-docs
     - Decision sponsor

**Total iniciativas pendientes: 20.**
**Total tareas atomicas estimadas: ~247.**

Recomendacion de orden de ejecucion
======================================

1. **P1 tests** (#1, #2, #3) — cierra los 19 tests
   fallidos restantes. Trivial-moderado.
2. **P2 saneamiento estructural alto-impacto**:
   #4 (pytest config), #9 (UCs no documentados),
   #12 (UI sin marker) — son habilitadores para
   conformidad real.
3. **P1 conformidad** (#18) — masivo pero
   transformacional. Cada dominio puede paralelizarse.
4. **P2 audit retrospectivo** (#20) — antes de
   confiar plenamente en las cifras de la sesion.
5. **P2 CI gate** (#19) — solo cuando #18 este
   completo en al menos 1 dominio.
6. **P3 calidad** — orden libre.
7. **P4 decision** — pendiente sponsor.

Sin la decision del sponsor (P4) y sin las P1
completas, las P3 son trabajo cosmetico sobre una
base no validada.
