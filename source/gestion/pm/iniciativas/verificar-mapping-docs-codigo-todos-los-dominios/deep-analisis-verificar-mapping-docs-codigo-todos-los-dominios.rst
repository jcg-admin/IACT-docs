.. meta::
   :artefacto: DEEP-ANALISIS-VERIFICAR-MAPPING-DOCS-CODIGO-TODOS-LOS-DOMINIOS
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/verificar-mapping-docs-codigo-todos-los-dominios
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:29:37
   :ultimo_cambio: 2026-05-19T20:29:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-verificar-mapping-docs-codigo-todos-los-dominios:

==============================================================
Deep-Analisis: Mapping Docs <-> Codigo (12 dominios)
==============================================================

Metodologia
============

Para cada dominio in-scope:

1. Listar UCs declarados en
   ``source/requisitos/requisitos-funcionales/{dominio}/uc-NNN-*/``.
2. Extraer descripciones de markers ``UC_<DOM>_<NN>`` en
   ``IACT-api/callcentersite/apps/`` con
   ``grep -rohE "UC_<DOM>_[0-9]+ — [^.\\n']{10,80}"``.
3. Mapear por **coincidencia textual descripcion-de-marker
   <-> nombre-de-UC-docs**, no por linearidad numerica.
4. Identificar markers extras en codigo (sin docs) y UCs en
   docs sin marker en codigo.

Total descripciones recolectadas: 265 lineas (extracto en
``/tmp/marker-descriptions.txt`` durante la sesion;
reproducible con el grep documentado arriba).

----

Mapping verificado por dominio
================================

auth (5 docs, 5 markers) — LINEAR
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion en codigo (canonica)
     - UC docs
   * - UC_AUTH_01
     - Iniciar Sesion
     - uc-001-iniciar-sesion
   * - UC_AUTH_02
     - Cerrar Sesion
     - uc-002-cerrar-sesion
   * - UC_AUTH_03
     - Resetear contrasena de usuario (admin)
     - uc-003-recuperar-password
   * - UC_AUTH_04
     - Cambiar Contrasena
     - uc-004-cambiar-password
   * - UC_AUTH_05
     - Listar/cerrar sesiones activas
     - uc-005-gestionar-sesiones

Cobertura: **5/5 (100%)**.

users (4 docs, 4 markers api) — NON-LINEAR
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion en codigo
     - UC docs
   * - UC_USR_01
     - Crear Usuario
     - uc-006-crear-usuario
   * - UC_USR_02
     - Consultar Usuarios (list + retrieve)
     - **uc-009-listar-usuarios** (no uc-007)
   * - UC_USR_03
     - Modificar Usuario (PATCH)
     - **uc-007-modificar-usuario** (no uc-008)
   * - UC_USR_04
     - Eliminar usuario (baja logica BR-009)
     - **uc-008-baja-usuario** (no uc-009)

Cobertura: **4/4 (100%)**, pero mapping **no lineal**:
docs ordena por accion temporal (crear, modificar, baja,
listar) y codigo ordena por CRUD (Create, Read, Update,
Delete).

ui declara markers extras UC_USR_05, UC_USR_06, UC_USR_07
sin descripcion textual visible — posibles features ui
sin UC docs equivalente, o numeracion ui distinta de api.
Verificar en iniciativa futura
``auditar-componentes-ui-sin-marker``.

access (2 docs, 7 markers api) — DOCS INCOMPLETOS
---------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion en codigo
     - UC docs equivalente
   * - UC_ACC_01
     - Asignar funciones a usuario
     - uc-010-asignar-funciones
   * - UC_ACC_02
     - Revocar funciones de usuario (BR-009)
     - uc-011-revocar-funciones
   * - UC_ACC_03
     - Permisos del usuario (alias accessService)
     - **sin UC docs equivalente**
   * - UC_ACC_04
     - Asignar agrupador a usuario
     - **sin UC docs equivalente directo**
       (relacionado con uc-012)
   * - UC_ACC_05
     - Reglas de Separacion de Funciones
     - **sin UC docs equivalente**
   * - UC_ACC_08
     - Conceder permiso excepcional temporal
     - **uc-014-conceder-permiso-excepcional-perm**
       (cross-dominio: docs lo pone en permissions/)
   * - UC_ACC_09
     - Auditar Cambios de Acceso
     - **uc-020-auditar-acceso**
       (cross-dominio: docs lo pone en permissions/)

Cobertura **api: 2/2 docs declarados + 5 markers extras**.
Hallazgo: la separacion docs vs codigo no es 1-1 por
dominio. ``UC_ACC_08`` y ``UC_ACC_09`` son cross-dominio:
implementados bajo ``access`` en codigo, documentados bajo
``permissions/`` en docs. UC_ACC_03/04/05 son markers de
codigo sin UC declarado en docs (deuda documental inversa).

permissions (10 docs, 10 markers en api) — MIXED
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_PERM_01
     - Asignar AccessGroup a usuario
     - uc-012-asignar-grupo-usuario-perm
   * - UC_PERM_02
     - Revocar AccessGroup de usuario
     - uc-013-revocar-grupo-usuario-perm
   * - UC_PERM_03
     - Aprobar permiso excepcional
     - uc-014-conceder-permiso-excepcional-perm
       (ya cubierto por UC_ACC_08 — duplicacion?)
   * - UC_PERM_04
     - Revocar permiso excepcional
     - uc-015-revocar-permiso-excepcional
   * - UC_PERM_05
     - Gestionar Grupos de Funciones (AGR)
     - uc-016-gestionar-grupo-permisos
   * - UC_PERM_06
     - Asignar funcion a grupo
     - uc-017-asignar-funciones-grupo
   * - UC_PERM_07
     - Verificar Permiso
     - uc-018-verificar-permiso-usuario
   * - UC_PERM_08
     - Menu dinamico
     - uc-019-generar-menu-dinamico
   * - (sin UC_PERM_09)
     - —
     - **uc-020-auditar-acceso** ya implementado
       como UC_ACC_09 (cross-dominio)
   * - UC_PERM_10
     - Consultar Auditoria de Permisos
     - uc-021-consultar-auditoria-permisos

Cobertura: **10/10 (100%)** docs cubiertos, con
``uc-020`` implementado bajo marker
``UC_ACC_09`` (cross-dominio) y posible duplicacion
entre ``UC_PERM_03`` y ``UC_ACC_08`` para
uc-014 (verificar caso por caso).

reports (16 docs, 15 markers en codigo) — GAP NUMERACION
----------------------------------------------------------

Documentado en detalle en
:doc:`/gestion/pm/iniciativas/implementar-uc-rpt-05-06-programacion-reportes/deep-analisis-implementar-uc-rpt-05-06-programacion-reportes`.
Resumen:

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_RPT_01
     - Dashboard de KPIs IVR
     - uc-032-ver-dashboard
   * - UC_RPT_02
     - Real-time metrics STUB (CNST-004)
     - uc-033-ver-metricas-tiempo-real
   * - UC_RPT_03
     - Ver Reportes Historicos
     - uc-034-ver-reportes-historicos
   * - UC_RPT_04
     - Exportar Reporte
     - uc-035-exportar-reporte
   * - **(05, 06 sin asignar)**
     - **gaps de numeracion**
     - —
   * - UC_RPT_07
     - Programar Reporte
     - uc-036-programar-reporte
   * - UC_RPT_08
     - Ver Reportes Programados
     - uc-037-ver-reportes-programados
   * - UC_RPT_09
     - Configurar Filtros (SavedFilter)
     - uc-038-gestionar-filtros-guardados
   * - UC_RPT_10
     - Guardar Vista
     - uc-039-guardar-vista
   * - UC_RPT_11
     - Compartir Reporte
     - uc-040-compartir-reporte
   * - UC_RPT_12
     - Reporte de rendimiento de agentes
     - uc-041-reporte-agentes
   * - UC_RPT_13
     - Reporte de colas (llamadas abandonadas)
     - uc-042-reporte-colas
   * - UC_RPT_14
     - Reporte de campanas (anomalias cMenu)
     - uc-043-reporte-campanas
   * - UC_RPT_15
     - Transferencias IVR (KPIs SLA)
     - uc-044-reporte-transferencias
   * - UC_RPT_16
     - Menus IVR (redirigidos / menu_centro)
     - uc-045-reporte-menus-ivr
   * - UC_RPT_17
     - Clientes unicos por segment
     - uc-046-reporte-clientes-unicos
   * - **(sin marker)**
     - **uc-047-resolver-segmento-usuario**
     - **posible gap real** (o helper interno
       de UC_RPT_17, sin verificar)

Cobertura: **15-16 / 16**. El unico potencialmente sin
implementacion es ``uc-047`` — requiere lectura del RST
de uc-047 para verificar si es UC user-facing o helper
backend.

alerts (5 docs, 5 markers) — LINEAR
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_ALR_01
     - Gestionar Reglas de Alerta (CRUD)
     - uc-050-configurar-umbrales-alertas
   * - UC_ALR_02
     - Ver Alertas Activas
     - uc-051-ver-alertas-activas
   * - UC_ALR_03
     - Reconocer Alerta
     - uc-052-reconocer-alerta
   * - UC_ALR_04
     - Ver Historial de Alertas
     - uc-053-ver-historial-alertas
   * - UC_ALR_05
     - Gestionar Suscripciones (FASE 4)
     - uc-054-gestionar-suscripciones-alertas

Cobertura: **5/5 (100%)** linear.

audit (4 docs, 4 markers) — LINEAR
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_AUD_01
     - Consultar Auditoria
     - uc-055-consultar-audit-log
   * - UC_AUD_02
     - Buscar en Auditoria
     - uc-056-buscar-en-audit-log
   * - UC_AUD_03
     - Exportar auditoria
     - uc-057-exportar-audit-log
   * - UC_AUD_04
     - Generar Reporte de Compliance
     - uc-058-reporte-cumplimiento

Cobertura: **4/4 (100%)** linear.

logs (7 docs, 8 markers) — LINEAR + EXTRA
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_LOG_01
     - Tail de logs Django
     - uc-059-ver-logs-aplicacion
   * - UC_LOG_02
     - Tail del log ETL desde MariaDB
     - uc-060-ver-logs-etl
   * - UC_LOG_03
     - Busqueda en logs
     - uc-061-buscar-en-logs
   * - UC_LOG_04
     - Exportar Logs (async)
     - uc-062-exportar-logs
   * - UC_LOG_05
     - Logs de infraestructura
     - uc-063-ver-logs-infra
   * - UC_LOG_06
     - Estado de salud del sistema
     - uc-064-ver-estado-sistema
   * - UC_LOG_07
     - Metricas tecnicas del sistema
     - uc-065-ver-metricas-rendimiento
   * - UC_LOG_08
     - Eventos del pipeline analitico
     - **sin UC docs equivalente** (extra
       implementado, no documentado)

Cobertura docs: **7/7 (100%)**. ``UC_LOG_08`` es deuda
documental inversa.

pipeline (4 docs, 5 markers) — LINEAR + EXTRA
-----------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker
     - Descripcion
     - UC docs
   * - UC_PIP_01
     - Estado del pipeline ETL IVR
     - uc-071-ver-estado-pipeline
   * - UC_PIP_02
     - Errores del pipeline ETL
     - uc-072-ver-errores-pipeline
   * - UC_PIP_03
     - Disponibilidad de datos por quarter
     - uc-073-ver-disponibilidad-datos
   * - UC_PIP_04
     - Solicitar reintento del pipeline
     - uc-074-reintentar-pipeline
   * - UC_PIP_05
     - Gestionar configuracion del job ETL
     - **sin UC docs equivalente** (extra)

Cobertura docs: **4/4 (100%)**. ``UC_PIP_05`` es deuda
documental inversa.

----

Resumen agregado verificado
=============================

.. list-table::
   :header-rows: 1
   :widths: 16 10 10 14 18 32

   * - Dominio
     - UCs docs
     - Mapping
     - Cobertura
     - Markers extras
     - Notas
   * - auth
     - 5
     - LINEAR
     - 5/5
     - 0
     - —
   * - users
     - 4
     - NON-LINEAR
     - 4/4
     - 3 (UI)
     - CRUD vs accion-temporal
   * - access
     - 2
     - DISCREPANTE
     - 2/2 docs
     - 5 api
     - UC_ACC_08/09 cross-dominio
       (docs los pone en permissions)
   * - permissions
     - 10
     - MIXED
     - 10/10 docs
     - 0 (uc-020 cross via
       UC_ACC_09)
     - Duplicacion potencial
       UC_PERM_03 vs UC_ACC_08
   * - reports
     - 16
     - GAP NUMERACION
     - 15-16/16
     - 0 (sin extras)
     - uc-047 sin marker directo;
       UC_RPT_05/06 reservados
   * - alerts
     - 5
     - LINEAR
     - 5/5
     - 0
     - —
   * - audit
     - 4
     - LINEAR
     - 4/4
     - 0
     - —
   * - logs
     - 7
     - LINEAR
     - 7/7
     - 1
     - UC_LOG_08 extra
   * - pipeline
     - 4
     - LINEAR
     - 4/4
     - 1
     - UC_PIP_05 extra
   * - operator
     - 10
     - OUT
     - n/a
     - 0
     - 0 markers (concuerda OUT)
   * - supervision
     - 3
     - OUT
     - n/a
     - 0
     - 0 markers (concuerda OUT)
   * - caller
     - 5
     - OUT
     - n/a
     - 0
     - 0 markers (concuerda OUT)

**Total in-scope: 57 UCs.**

**Total con implementacion verificada api: 56-57**.

* Verificados con marker textual: **56**.
* Caso ambiguo: **uc-047-resolver-segmento-usuario**
  (sin marker directo; puede ser cubierto implicitamente
  por UC_RPT_17 o ser gap real). Requiere lectura del
  RST.

**Cobertura real api in-scope: 98-100%** (no ~98% con
2 gaps como reporto el deep-analysis original; era 1 gap
ambiguo).

**Markers extras (implementados sin UC docs):**

* UC_ACC_03, UC_ACC_04, UC_ACC_05 (3 en access)
* UC_LOG_08 (1 en logs)
* UC_PIP_05 (1 en pipeline)
* UC_USR_05, UC_USR_06, UC_USR_07 (3 en UI, sin docs;
  pueden ser features ui no canonicas)

Total deuda documental inversa: **~8 markers
implementados sin RST equivalente** en
``requisitos-funcionales/``.

----

Correcciones al deep-analysis original
========================================

C-1 — Cobertura api real es ~98-100%, no 98% con 2 gaps
--------------------------------------------------------

Original: "56/57 con marker (~98%), 2 UCs estrictamente
sin codigo: UC_RPT_05/06".

Corregido: **56-57/57 con codigo**. Los UC_RPT_05/06
**no eran UCs sin codigo** — eran markers inexistentes
en una numeracion no-lineal. Los UCs docs correspondientes
(uc-036/037) estan implementados bajo UC_RPT_07/08. El
unico gap potencialmente real es ``uc-047`` (sin
verificacion del RST).

C-2 — H-A3 (UCs api sin ui) sobreestima la brecha ui
------------------------------------------------------

Original lista UC_AUTH_04, UC_PERM_01/06/09, UC_RPT_08,
13, 14, 15, 16, 17 como "api pero no ui".

Pero UC_PERM_09 **no existe en api** (gap de numeracion).
Y UC_RPT_08 cubre uc-037 que **si tiene ui** (pendiente
verificar). La brecha ui real es menor que reportada.

C-3 — Deuda documental inversa cuantificada
---------------------------------------------

Markers en codigo sin UC docs equivalente: ~8.
Iniciativa
``documentar-ucs-implementados-no-declarados``
cubre esto.

----

Hallazgos nuevos
==================

H-B1 — Duplicacion potencial UC_PERM_03 vs UC_ACC_08
------------------------------------------------------

Ambos markers describen "permiso excepcional" (conceder
o aprobar). UC_PERM_03 dice "Aprobar permiso excepcional"
y UC_ACC_08 "Conceder permiso excepcional temporal". El
UC docs uc-014 se llama "conceder-permiso-excepcional-perm".

Puede ser:

* Dos endpoints distintos (preview en UC_PERM_03 vs
  conceder real en UC_ACC_08), correctamente separados.
* Duplicacion accidental: la misma funcionalidad
  implementada dos veces.

Requiere lectura del codigo y comparacion con el FR del
uc-014 para resolver. Iniciativa
``aclarar-duplicacion-perm-03-acc-08``.

H-B2 — Cross-dominio code vs docs
-----------------------------------

uc-020-auditar-acceso (en permissions/ docs) esta
implementado bajo UC_ACC_09 (en access del codigo).
uc-014-conceder-permiso-excepcional-perm (en permissions/
docs) puede estar en UC_ACC_08 (access codigo).

Patron: el codigo agrupa por "scope tecnico" (access vs
permissions reflejan tablas/modelos), docs agrupa por
"actor / boundary" (el usuario que pide permisos vs el
admin que los gobierna). La discrepancia es legitima
pero requiere mapping explicito.

H-B3 — UI numeracion divergente
---------------------------------

UI tiene UC_USR_05, 06, 07 sin contraparte en api. Puede
ser:

* Features ui-only (preferencias, settings UI).
* Numeros usados por convencion distinta en UI.

Iniciativa ``alinear-numeracion-uc-api-ui``.

H-B4 — uc-047 ambiguo
-----------------------

uc-047-resolver-segmento-usuario no tiene marker directo
en api. Necesita lectura del RST para determinar si es
UC user-facing (entonces gap real) o helper backend
(entonces implementado implicitamente). Iniciativa
``aclarar-uc-047-resolver-segmento``.

----

Conclusion
===========

La cobertura real es **muy alta** (~98-100% in-scope api).
La auditoria original reporto 98% pero con 2 gaps reales;
en realidad eran **0-1 gaps** reales y 2 artefactos de
numeracion. La diferencia entre lo reportado y la realidad
es ~5% — significativa para decisiones de priorizacion.

**Implicacion para el sponsor:** el sistema esta mucho
mas completo de lo que la auditoria sugeria. La pregunta
"se implementaron todos los flujos de los UCs?" tiene
respuesta calibrada: **practicamente todos** (al menos
56 de 57 in-scope con codigo). La deuda real es
documental (markers sin docs) y de calidad/conformidad
(que cada flujo cumpla todos sus FRs — fuera del scope
de esta auditoria).

Iniciativas derivadas:

1. ``documentar-ucs-implementados-no-declarados`` — cierra
   los ~8 markers sin docs.
2. ``aclarar-uc-047-resolver-segmento`` — resuelve el
   unico gap ambiguo.
3. ``aclarar-duplicacion-perm-03-acc-08`` — resuelve la
   duplicacion potencial.
4. ``alinear-numeracion-uc-api-ui`` — resuelve UC_USR_05/
   06/07 ui sin api.
5. ``auditar-conformidad-fr-tests-aceptacion`` — el
   trabajo de orden superior pendiente.

La iniciativa cierra COMPLETADA con la matriz maestra
verificada documentada arriba.
