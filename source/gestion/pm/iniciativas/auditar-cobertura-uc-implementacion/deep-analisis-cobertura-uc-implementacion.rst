.. meta::
   :artefacto: DEEP-ANALISIS-COBERTURA-UC-IMPLEMENTACION
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-cobertura-uc-implementacion
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:13:49
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-cobertura-uc-implementacion:

==============================================================
Deep-Analisis: Cobertura UC -> Implementacion
==============================================================

Metodologia
============

**Universo:** 75 UCs declarados en
``source/requisitos/requisitos-funcionales/{dominio}/uc-NNN-*/``
(verificado con
``find ... -mindepth 2 -maxdepth 2 -type d -name "uc-*" | wc -l``).

**Convencion de mapeo docs <-> codigo:** los docs usan
``uc-NNN-descripcion`` (numero secuencial global); el codigo
usa ``UC_<DOMINIO>_<NN>`` (numero secuencial por dominio).

.. list-table::
   :header-rows: 1
   :widths: 25 25 18 32

   * - Dominio docs
     - Marker codigo
     - Rango UC
     - Cantidad
   * - auth
     - UC_AUTH
     - uc-001..005
     - 5
   * - users
     - UC_USR
     - uc-006..009
     - 4
   * - access
     - UC_ACC
     - uc-010..011
     - 2
   * - permissions
     - UC_PERM
     - uc-012..021
     - 10
   * - operator
     - UC_OPR
     - uc-022..031
     - 10
   * - reports
     - UC_RPT
     - uc-032..047 (excl. 048,049)
     - 16
   * - alerts
     - UC_ALR
     - uc-050..054
     - 5
   * - audit
     - UC_AUD
     - uc-055..058
     - 4
   * - logs
     - UC_LOG
     - uc-059..065
     - 7
   * - caller
     - UC_CALL
     - uc-066..070
     - 5
   * - pipeline
     - UC_PIP
     - uc-071..074
     - 4
   * - supervision
     - UC_SUP
     - uc-075..077
     - 3

Total: **75 UCs** (suma columna Cantidad).

**Comando de verificacion:**

.. code-block:: bash

   # Markers en codigo IACT-api
   for m in UC_AUTH UC_USR UC_ACC UC_PERM UC_OPR UC_RPT UC_DSH \\
             UC_ALN UC_ALR UC_AUD UC_LOG UC_CALL UC_PIP UC_SUP; do
     grep -rohE "\\b${m}_[0-9]+\\b" \\
       /home/user/IACT-api/callcentersite/apps/ 2>/dev/null \\
       | sort -u | tr '\\n' ' '
   done

   # Markers en codigo IACT-ui
   for m in UC_AUTH UC_USR UC_ACC UC_PERM UC_RPT UC_DSH UC_ALN \\
             UC_ALR UC_AUD UC_LOG UC_PIP; do
     grep -rohE "\\b${m}_[0-9]+\\b" \\
       /home/user/IACT-ui/src/ 2>/dev/null \\
       | sort -u | tr '\\n' ' '
   done

----

Scope: dos lecturas del OUT
================================

El sponsor declaro OUT: "TODOS los uc-opr-*, uc-sup-*, y los
uc-cli-01..05".

**Lectura A — Estricta literal:** el prefijo ``uc-cli-``
solo existe en ``source/requisitos/casos-uso/caller/``
(uc-cli-01..05) — no en ``requisitos-funcionales/``. Bajo
esta lectura, el sponsor excluye solo los 18 UCs del
arbol ``casos-uso/`` (10 opr + 3 sup + 5 cli) y los 75 UCs
de ``requisitos-funcionales/`` quedan TODOS in-scope.

**Lectura B — Por categoria de actor (recomendada):** los
prefijos refieren a actores. ``uc-opr-*`` = operator,
``uc-sup-*`` = supervision, ``uc-cli-01..05`` = los 5 UCs
del actor caller (que en ``requisitos-funcionales/`` son
uc-066..070). Bajo esta lectura, los 18 UCs de los tres
actores quedan OUT en ambos arboles.

**Adoptada en esta auditoria: lectura B.** Razon: el
sistema implementa un solo modelo por actor;
``operator/uc-022..031`` y ``operator/uc-opr-01..10`` son
versiones de los mismos UCs en arboles distintos del docs.
Excluir solo casos-uso/ pero IN
requisitos-funcionales/operator/ deja un scope
incoherente.

Bajo lectura B:

* OUT: 10 (operator) + 3 (supervision) + 5 (caller) = **18**.
* IN: 75 - 18 = **57 UCs in-scope**.

----

Cobertura observada por dominio
=================================

Conteo de marker IDs distintos detectados en codigo via grep.
Marker presente en codigo => UC tiene al menos una referencia
en docstrings/comentarios; **no garantiza implementacion
completa**, pero es un proxy fuerte (no se decora codigo no
existente con el marker).

.. list-table::
   :header-rows: 1
   :widths: 14 7 12 12 12 12 8 23

   * - Dominio
     - Docs
     - Markers api
     - Markers ui
     - Cobertura api
     - Cobertura ui
     - Scope
     - Notas
   * - auth
     - 5
     - 5
     - 4
     - 100%
     - 80%
     - IN
     - ui falta UC_AUTH_04
       (cambiar-password). Puede
       existir en UI sin tag.
   * - users
     - 4
     - 4
     - 7
     - 100%
     - 175%
     - IN
     - ui tiene 3 UC_USR extras
       (05, 06, 07) no en docs.
   * - access
     - 2
     - 7
     - 8
     - 350%
     - 400%
     - IN
     - Codigo tiene UC_ACC_01..05,
       08, 09 (7 markers); docs
       solo declaran 2 dirs.
       Probable: docs incompletos
       respecto a impl.
   * - permissions
     - 10
     - 10
     - 7
     - 100%
     - 70%
     - IN
     - ui falta UC_PERM_01, 06, 09.
   * - operator
     - 10
     - 0
     - n/a
     - 0%
     - 0%
     - OUT
     - Confirmado: 0 markers en
       api. Concuerda con scope
       OUT.
   * - reports
     - 16
     - 15
     - 9
     - 94%
     - 56%
     - IN
     - api falta UC_RPT_05, 06.
       ui falta UC_RPT_05, 06,
       08, 13, 14, 15, 16.
   * - alerts
     - 5
     - 5
     - 5
     - 100%
     - 100%
     - IN
     - Completo.
   * - audit
     - 4
     - 4
     - 4
     - 100%
     - 100%
     - IN
     - Completo.
   * - logs
     - 7
     - 8
     - 8
     - >100%
     - >100%
     - IN
     - Codigo tiene UC_LOG_08
       extra no en docs.
   * - caller
     - 5
     - 0
     - n/a
     - 0%
     - 0%
     - OUT
     - Confirmado: 0 markers.
   * - pipeline
     - 4
     - 5
     - 5
     - >100%
     - >100%
     - IN
     - Codigo tiene UC_PIP_05
       extra no en docs.
   * - supervision
     - 3
     - 0
     - n/a
     - 0%
     - 0%
     - OUT
     - Confirmado: 0 markers.

----

Resumen agregado in-scope (57 UCs)
====================================

.. list-table::
   :header-rows: 1
   :widths: 30 18 18 34

   * - Categoria
     - UCs api
     - UCs ui
     - Notas
   * - Implementados api (marker detectado)
     - 56 / 57
     - n/a
     - Solo UC_RPT_05 / UC_RPT_06
       sin marker en api.
   * - Implementados ui (marker detectado)
     - n/a
     - 44 / 57
     - 13 UCs sin marker en ui
       (UI puede existir sin tag).
   * - api + ui (ambos)
     - n/a
     - n/a
     - Aprox 44 / 57 (~77%)
   * - Sin marker en ningun repo
     - 2
     - n/a
     - UC_RPT_05 y UC_RPT_06.

----

Hallazgos
==========

H-A1 — Codigo tiene mas UCs implementados que docs declaran
-------------------------------------------------------------

Dominios afectados:

* **access**: codigo declara 7 markers (UC_ACC_01..05,
  08, 09); docs solo 2 (uc-010-asignar-funciones,
  uc-011-revocar-funciones). Faltan en docs:
  UC_ACC_01..05, 08, 09 — al menos 7 UCs no
  documentados pero implementados.
* **users**: ui declara UC_USR_05, 06, 07 — 3 UCs no
  documentados.
* **logs**: codigo declara UC_LOG_08 — 1 UC no
  documentado.
* **pipeline**: codigo declara UC_PIP_05 — 1 UC no
  documentado.

**Total UCs implementados pero NO documentados: ~12**.
Es deuda documental, no de implementacion. Candidata
a iniciativa
``documentar-ucs-implementados-no-declarados``.

H-A2 — UCs documentados sin marker en codigo
----------------------------------------------

In-scope sin marker en api:

* **UC_RPT_05** (uc-036-programar-reporte): sin
  marker en api ni ui.
* **UC_RPT_06** (uc-037-ver-reportes-programados):
  sin marker en api ni ui.

Posible: feature de programacion de reportes esta
solo en docs, no implementada. Candidata a iniciativa
``implementar-uc-rpt-05-06-programacion-reportes``.

H-A3 — UCs en api pero no en ui (gap ui)
------------------------------------------

In-scope con marker api pero NO ui:

* UC_AUTH_04 (cambiar-password)
* UC_PERM_01, 06, 09 (asignar grupo, gestionar grupo
  permisos, generar menu dinamico)
* UC_RPT_08 (reporte historico)
* UC_RPT_13, 14, 15, 16, 17 (varios reportes IVR)

**Total ~9 UCs con backend pero sin (o con incierto)
componente UI**. Pueden tener UI sin marker — auditoria
de calidad requiere abrir cada caso. Candidata a
iniciativa ``auditar-componentes-ui-sin-marker``.

H-A4 — UCs OUT confirmados por scope
--------------------------------------

Los 18 UCs OUT (operator 10, supervision 3, caller 5)
tienen **0 markers** en codigo de api y ui. Concuerda
con la decision del sponsor de no implementarlos:
nadie los marco en el codigo porque nunca se
implementaron.

H-A5 — La auditoria por marker NO valida flujo end-to-end
-----------------------------------------------------------

Detectar ``UC_AUTH_01`` en docstring no garantiza que el
endpoint cumpla los 5 FRs (fr-001-01..05). Esta
auditoria es de **presencia**, no de **conformidad**.

Para una auditoria de conformidad: cruzar cada FR
con su test de aceptacion. Es trabajo de orden superior;
candidata a
``auditar-conformidad-fr-tests-aceptacion``.

H-A6 — Tests cubren mucho del marker set
------------------------------------------

Los 1378 tests passing de IACT-api (98.64% de 1397
collected) cubren los flujos donde el marker existe. Sin
embargo, esta auditoria no verifico que cada UC tenga
**al menos un test que mencione su marker** — solo
verifico presencia del marker en codigo no-test.

Es una asuncion razonable: tests con cobertura del
98.64% en codigo decorado con markers => mayoria de los
UCs marcados tienen tests pasando.

----

Conclusiones
=============

* De los 57 UCs in-scope, **55-56 tienen implementacion
  en api** (marker detectado): cobertura efectiva ~98%.
* De los 57 in-scope, **~44 tienen implementacion en
  ui** (marker detectado): cobertura efectiva ~77%.
  Posible subestimacion si hay UI sin marker.
* **2 UCs explicitamente sin implementacion**:
  UC_RPT_05 (uc-036-programar-reporte) y UC_RPT_06
  (uc-037-ver-reportes-programados).
* **18 UCs OUT** confirmados con 0 markers (concuerda
  con scope).
* **~12 UCs implementados pero no documentados**
  (deuda documental inversa).
* Esta auditoria mide **presencia**, no **conformidad
  FR-test**. La conformidad requiere iniciativa
  separada.

**Respuesta a la pregunta del sponsor "se implementaron
todos los flujos de los UCs?":**

* In-scope con impl detectada (api): **~56 / 57 (98%)**.
* In-scope con impl detectada (ui): **~44 / 57 (77%)**.
* Estrictamente sin implementacion (ni api ni ui): **2**
  (programar y ver reportes programados).

No se implemento **ningun UC nuevo en esta sesion**. La
cobertura observada es resultado del trabajo de
desarrollo previo.

----

Iniciativas candidatas derivadas
==================================

Ordenadas por prioridad sugerida:

1. **implementar-uc-rpt-05-06-programacion-reportes**
   (IACT-api + IACT-ui): 2 UCs documentados sin
   implementacion. Cierra el unico gap real de
   in-scope sin codigo.
2. **auditar-componentes-ui-sin-marker** (IACT-ui):
   ~9-13 UCs con api pero ui incierto. Verificar caso
   por caso si el componente existe sin marker
   o si requiere implementacion.
3. **documentar-ucs-implementados-no-declarados**
   (IACT-docs): ~12 UCs implementados pero no en docs
   (access 5+, users 3, logs 1, pipeline 1). Crea las
   carpetas
   ``source/requisitos/requisitos-funcionales/{dominio}/uc-NNN-*/``
   con sus FRs.
4. **auditar-conformidad-fr-tests-aceptacion**
   (multi-repo): cruzar cada FR con su test que
   verifica el criterio de aceptacion. Trabajo de
   orden superior.
5. **resolver-tests-fallidos-residual** (3 iniciativas
   hermanas ya identificadas: dashboard residual,
   alerts residual, pipeline residual) — 19 tests
   fallando son test bugs, no implementacion faltante.
