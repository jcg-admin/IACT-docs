.. meta::
   :artefacto: DEEP-ANALISIS-AUDITAR-IMPLEMENTACION-UCS-API-UI
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-implementacion-ucs-api-ui
   :repo_objetivo: multiple
   :estado: Completada
   :version: 1.0.0
   :fecha_creacion: 2026-07-03T22:15:30
   :ultimo_cambio: 2026-07-03T22:15:30
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-auditar-implementacion-ucs-api-ui:

==============================================================
Deep-Analisis: Implementacion UCs docs -> api / ui
==============================================================

Metodologia
============

1. Enumerar UCs declarados en docs:

   .. code-block:: bash

      find source/requisitos/requisitos-funcionales \
        -mindepth 2 -maxdepth 2 -type d -name "uc-*" | wc -l
      # => 88

2. Extraer markers de codigo con tolerancia a formas
   compuestas y rangos (leccion de
   ``adoptar-protocolo-grep-validado-en-auditorias``):

   .. code-block:: bash

      # api
      grep -rhoE 'UC[_-][A-Z]{2,5}[_-][0-9]{1,2}([./,-]+[0-9]{1,2})*' \
        --include='*.py' /home/user/IACT-api
      # ui
      grep -rhoE 'UC[_-][A-Z]{2,5}[_-][0-9]{1,2}([./,-]+[0-9]{1,2})*' \
        --include='*.js' --include='*.jsx' --include='*.ts' \
        --include='*.tsx' /home/user/IACT-ui/src

   Los tokens se normalizan (``UC-RPT-08`` ≡ ``UC_RPT_08``) y
   se expanden a dos niveles de evidencia:

   * **Fuerte** — el numero esta nombrado explicitamente:
     marker simple (``UC_RPT_08``) o compuesto que lo nombra
     (``UC_RPT_07/08``, ``UC_ACC_06-07``).
   * **Debil** — el numero solo esta cubierto por el interior
     de un rango en comentario (``UC_ADM_01..03`` cubre
     debilmente al 02; ``UC_RPT_01..17`` cubre debilmente a
     los inexistentes 05/06). La evidencia debil **no** cuenta
     como implementacion: exige verificacion funcional.

   Resultado: api 73 markers fuertes / ui 73 markers fuertes.

3. Mapping UC docs → marker por validacion **textual**, nunca
   por linealidad numerica:

   * uc-001..077: mapping verificado de
     :doc:`/gestion/pm/iniciativas/verificar-mapping-docs-codigo-todos-los-dominios/deep-analisis-verificar-mapping-docs-codigo-todos-los-dominios`
     (incluye los no-lineales de users y los cross-dominio
     uc-014/uc-020).
   * uc-078..090: campo ``Marker código`` declarado en el
     ``index.rst`` de cada UC (retro-documentados).
   * uc-091: declara implementacion api via APScheduler
     (``apps/pipeline/scheduler.py``) — sin marker ``UC_``.

4. Inspeccion de buckets negativos ANTES de publicar gaps
   (seccion "Falsos gaps evitados").

Resumen por dominio
====================

.. list-table::
   :header-rows: 1
   :widths: 13 8 8 22 22 27

   * - Dominio
     - UCs
     - In-scope
     - api
     - ui
     - Notas
   * - auth
     - 5
     - 5
     - 5/5
     - 5/5
     - lineal (UC_AUTH_01..05)
   * - users
     - 7
     - 7
     - 7/7
     - 7/7
     - NO lineal: uc-007→USR_03, uc-008→USR_04,
       uc-009→USR_02; uc-083..085→USR_05..07
   * - access
     - 5
     - 5
     - 5/5
     - 5/5
     - uc-078..080→ACC_03..05 (retro-doc)
   * - permissions
     - 10
     - 10
     - 10/10
     - 10/10
     - uc-020 via ``UC_ACC_09`` (cross-dominio)
   * - operator
     - 10
     - 0
     - n/a
     - n/a
     - OUT — 0 markers (verificado)
   * - reports
     - 15
     - 15
     - 15/15
     - 15/15
     - gap de numeracion RPT_05/06 (no son UCs);
       uc-037 en ui via compuesto ``UC_RPT_07/08``
   * - alerts
     - 5
     - 5
     - 5/5
     - 5/5
     - uc-054 en ui con marker adicional ``UC_ALR_06``
   * - audit
     - 4
     - 4
     - 4/4
     - 4/4
     - lineal (UC_AUD_01..04)
   * - logs
     - 8
     - 8
     - 8/8
     - 8/8
     - incluye uc-081→LOG_08 (retro-doc)
   * - caller
     - 5
     - 0
     - n/a
     - n/a
     - OUT — 0 markers (verificado)
   * - pipeline
     - 6
     - 6
     - 6/6
     - 5/5 aplicables
     - uc-091 sin UI (actor Sistema; ETLScheduler
       verificado en ``apps/pipeline/scheduler.py``)
   * - supervision
     - 3
     - 0
     - n/a
     - n/a
     - OUT — 0 markers (verificado)
   * - admin
     - 5
     - 5
     - 5/5 (2 por endpoint)
     - 5/5
     - uc-086/087: endpoints presentes, marker api
       solo en rangos — ver F-03

**Totales: 88 UCs docs · 18 OUT · 70 in-scope · api 70/70 ·
ui 69/69 aplicables · 0 gaps docs → codigo.**

Matriz completa (88 filas):
:doc:`matriz-implementacion-uc-api-ui`.

Verificacion OUT
=================

Los dominios operator/caller/supervision se declaran
"Modulo reservado (out-of-scope para v5.6.0)" en su
``index.rst`` (muestra inspeccionada:
``requisitos-funcionales/operator/index.rst``). Presencia en
codigo:

.. code-block:: bash

   grep -rliE 'UC[_-](OPR|SUP|CLI)[_-][0-9]' --include='*.py' \
     /home/user/IACT-api          # => 0 archivos
   grep -rliE 'UC[_-](OPR|SUP|CLI)[_-][0-9]' /home/user/IACT-ui/src
   # => 0 archivos

Consistente: OUT declarado en docs y sin rastro en codigo.

Falsos gaps evitados (protocolo grep-validado)
================================================

Tres claims que una lectura ingenua habria publicado como
gaps y que la inspeccion del bucket negativo refuto:

FG-1 — "uc-037 sin ui" (UC_RPT_08 ausente en grep simple)
----------------------------------------------------------

El grep simple de markers no encontro ``UC_RPT_08`` en ui.
Inspeccion del bucket negativo: la ui SI implementa reportes
programados — el marker vive en forma **compuesta**:

* ``src/services/reportsGateway.js:21`` — "Reportes
  programados (UC_RPT_07/08)" con llamadas reales a
  ``/api/reports/schedules/``.
* ``src/router/AppRouter.jsx`` — ruta ``/reports/scheduled``
  comentada "UC_RPT_07/08" montando ``ScheduledReportPage``.
* ``src/redux/slices/reports.js`` — estado
  ``scheduledReports``.

Clasificacion: **PROVEN** (implementado). El mismo patron de
falso negativo que produjo el caso historico UC_RPT_05/06.

FG-2 — "uc-086/087/088 sin api" (UC_ADM_01/02/03 sin hit .py)
--------------------------------------------------------------

``UC_ADM_01/02/03`` no aparecen como markers granulares en
api. Inspeccion del bucket negativo: los endpoints que las
pantallas admin de ui consumen SI existen en api:

.. code-block:: bash

   grep -nE 'functions|access-groups|menu-items|separation-rules' \
     /home/user/IACT-api/callcentersite/apps/access/urls.py
   # separation-rules/ (:94), functions/ (:131),
   # access-groups/ (:85), menu-items/ (router :75)

Ademas ``UC_ADM_03`` si tiene marker explicito
(``apps/access/views.py:169`` — AccessGroup ViewSet), y
``config/urls.py:23`` reconoce el rango
"UC_ACC_01..09, UC_PERM_01..10, UC_ADM_01..03" bajo
``api/access/``. Clasificacion: **PROVEN** para presencia
funcional; el deficit es de conformidad de marker (F-03).

FG-3 — "uc-091 sin implementar" (sin marker UC_PIP)
----------------------------------------------------

uc-091 no tiene marker ``UC_``. Su RST declara la
implementacion como ``ETLScheduler``
(``apps/pipeline/scheduler.py``) + EVENT MariaDB. Verificado:

.. code-block:: bash

   ls /home/user/IACT-api/callcentersite/apps/pipeline/scheduler.py
   grep -c 'class ETLScheduler' .../apps/pipeline/scheduler.py  # => 1

Actor Sistema — no requiere UI. Clasificacion: **PROVEN**.

Hallazgos
==========

F-01 — Cobertura api in-scope: 70/70 (PROVEN)
-----------------------------------------------

67 UCs con marker fuerte directo, 2 con funcionalidad
verificada por endpoint y marker solo en rango (uc-086,
uc-087), 1 via scheduler declarado (uc-091). **Cero UCs docs
sin implementacion api.**

F-02 — Cobertura ui aplicable: 69/69 (PROVEN)
-----------------------------------------------

Todos los UCs in-scope con superficie UI esperada tienen
marker fuerte en ``src/``. uc-091 no aplica (actor Sistema).

F-03 — uc-086/uc-087 sin marker granular en api (PROVEN)
----------------------------------------------------------

Los docs declaran ``UC_ADM_01``/``UC_ADM_02`` y la ui los usa
como markers granulares, pero api solo los menciona en
comentarios de rango. La funcionalidad existe
(``separation-rules/``, ``functions/``). Accion derivada:
declarar los markers granulares en las vistas api
correspondientes (conformidad, no implementacion).

F-04 — ui-only UC_ACC_06/07 sin api ni UC docs (PROVEN)
---------------------------------------------------------

La ui contiene pantallas de segmentacion marcadas
``UC_ACC_06/07`` ("Gestionar segmentación y asignación de
usuarios"), pero ``src/services/accessGateway.js:10-12``
declara explicitamente que los endpoints fueron ELIMINADOS
por no existir en api (``/access/segments``,
``/access/segments/assign``). Gap real de consistencia
ui → api → docs: pantalla sin backend y sin UC declarado.

F-05 — Deuda documental inversa api: 6 markers (PROVEN)
---------------------------------------------------------

Markers en api sin UC en ``requisitos-funcionales/``:

* ``UC_DSH_01..04`` — app ``apps/dashboard`` (registrada en
  ``config/urls.py:41`` por
  ``resolver-tests-dashboard-iact-api``). La ui no llama
  ``/api/dashboard/`` (grep 0 hits en ``src/``).
* ``UC_PERM_09`` — emisor interno de AuditEvent (CA-01..11);
  servicio de soporte, no UC user-facing.
* ``UC_USR_08`` — ``SettingsViewSet`` (settings).

F-06 — Componente mock legacy en ui (INFERRED)
------------------------------------------------

``src/components/pages/Analytics/ScheduledReports.jsx`` usa
``mockSchedules`` hardcodeados. La ruta productiva
``/reports/scheduled`` monta ``ScheduledReportPage`` (no este
componente), por lo que se infiere legacy/no ruteado —
candidato a limpieza.

F-07 — Numeracion ui divergente UC_ALR_06 (PROVEN)
----------------------------------------------------

La ui marca la pantalla de suscripciones como ``UC_ALR_06``;
api implementa la misma funcionalidad bajo ``UC_ALR_05``
(``/api/alerts/me/subscriptions/`` verificado en
``apps/alerts/urls.py:52``). Mismo patron que resolvio
``alinear-numeracion-uc-api-ui`` para UC_USR_05..07.

Iniciativas derivadas
======================

1. ``declarar-markers-adm-granulares-iact-api`` — cierra F-03.
2. ``resolver-segmentacion-acc-06-07`` — decide F-04:
   implementar endpoints, retirar pantallas, o documentar UC.
3. ``documentar-ucs-dsh-perm09-usr08`` — cierra F-05
   (extension natural de
   ``documentar-ucs-implementados-no-declarados``).
4. ``limpiar-scheduled-reports-mock-iact-ui`` — cierra F-06.
5. ``alinear-numeracion-alr-06`` — cierra F-07.

Conclusion
===========

La respuesta a "¿los UCs mencionados en docs estan
implementados en api e ui?" es: **si — 70/70 in-scope en api
y 69/69 aplicables en ui, con 0 gaps de implementacion**. Los
18 UCs restantes estan declarados out-of-scope (v5.6.0) y,
consistentemente, no tienen rastro en codigo.

La deuda detectada es de **direccion inversa** (codigo sin
docs: F-04, F-05) y de **conformidad de markers** (F-03,
F-07) — no de implementacion faltante. La calidad interna de
cada flujo (FR por FR) permanece cubierta por las iniciativas
de conformidad, fuera del alcance de esta auditoria.
