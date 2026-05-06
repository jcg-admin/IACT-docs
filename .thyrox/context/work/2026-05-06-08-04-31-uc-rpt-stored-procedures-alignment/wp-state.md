```yml
project: IACT-docs
work_package: 2026-05-06-08-04-31-uc-rpt-stored-procedures-alignment
created_at: 2026-05-06 08:04:31
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 3, 5, 6, 8, 10, 11)
target: Alinear los UC_RPT con la realidad arquitectonica: el backend consumira stored procedures (sp_rpt_*) del IVR legacy, no agrega via ORM. Hay 7 SPs canonicos identificados por el ejecutor que mapean a UC_RPT_01, 13, 15, 16, 17.
predecessor_wp: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
trigger: ejecutor identifico que el backend consume sp_rpt_llamadas_abandonadas, sp_rpt_centros_transferencia, sp_rpt_centros_xsegmento, sp_rpt_menu_redirigidos, sp_rpt_menu_centro, sp_rpt_cMENU_ERROR, sp_rpt_clientes — pero los UCs los modelan como agregacion ORM generica.
```

# WP — UC_RPT Stored Procedures Alignment

## Trigger

Identificacion del ejecutor:

> "el backend va a consumir los SP para poder mostrar los
> reportes... Los 7 tipos de reporte IVR reales son los que
> tienen stored procedures propios: sp_rpt_llamadas_abandonadas,
> sp_rpt_centros_transferencia, sp_rpt_centros_xsegmento,
> sp_rpt_menu_redirigidos, sp_rpt_menu_centro,
> sp_rpt_cMENU_ERROR, sp_rpt_clientes"

Auditoria preliminar revela:

- Los UC_RPT mencionan los SPs solo en `datos-involucrados.rst`
  (sección de contexto) pero NO en `flujo-principal.rst` (que
  describe la implementación esperada).
- El flujo principal modela "Query <Entity>DailyStat agregado"
  estilo ORM Django, NO `cursor.callproc('sp_rpt_*')`.
- Los uml-07 standalone (`use-case-view/reports/uc-rpt-*.rst`)
  no mencionan los SPs.

## Mapeo SP → UC_RPT identificado

| Stored Procedure | UC primario | UC secundario | Status doc actual |
|---|---|---|---|
| `sp_rpt_llamadas_abandonadas` | UC_RPT_13 | — | mencionado en datos-involucrados, NO en flujo |
| `sp_rpt_centros_transferencia` | UC_RPT_15 | — | idem |
| `sp_rpt_centros_xsegmento` | UC_RPT_15 | UC_RPT_01 | idem |
| `sp_rpt_menu_redirigidos` | UC_RPT_16 | — | idem |
| `sp_rpt_menu_centro` | UC_RPT_16 | — | idem |
| `sp_rpt_cMENU_ERROR` | UC_RPT_16 | — | idem |
| `sp_rpt_clientes` | UC_RPT_17 | — | idem |

UCs afectados (5): **UC_RPT_01, UC_RPT_13, UC_RPT_15, UC_RPT_16, UC_RPT_17**

## Hipotesis de causa raiz

1. **Asumio re-implementacion ORM**: los UCs se redactaron
   asumiendo que el backend Django REST Framework agregaria
   datos desde tablas pre-agregadas (`AgentDailyStatRepo`,
   `QueueDailyStat`, etc.) — patron típico Django ORM.
2. **Realidad legacy**: el IVR ya tiene SPs probados
   (`sp_rpt_*`) que retornan los reportes en forma terminada.
   Re-implementarlos en ORM duplicaria logica y arriesgaria
   regresion.
3. **`datos-involucrados.rst` es honesto** (cita el SP real)
   pero el `flujo-principal.rst` desconoce esa fuente.

## Output esperado

1. `discover/uc-rpt-stored-procedures-alignment-analysis.md` —
   Phase 1 con mapeo SP→UC + gap detallado por UC.
2. `analyze/sp-coverage-matrix.md` — tabla canónica:
   - UC_id | SP nombre | parametros entrada | columnas
     retorno | status doc | accion requerida
3. `analyze/uc-rpt-flujo-principal-corrections.md` — diff
   propuesto del flujo-principal de cada UC afectado para
   reflejar `cursor.callproc('sp_rpt_*', [params])`.
4. `analyze/domain-model-additions.md` — verificar si las
   *ReportService classes (CallerReportService,
   AbandonmentReportService, TransferReportService,
   IvrNavigationReportService) ya delegan a SPs o si necesitan
   actualizarse.
5. `track/recommendations.md` — propuesta de patches por UC.

## Restricciones

- **Sin modificar `domain-model/` ni `use-case-view/`** sin
  decision explícita del ejecutor (son WPs cerrados).
- **Sin modificar codigo Python real** del backend.
- **Foco exclusivo en `casos-uso/reports/uc-rpt-*`** que es la
  spec de requisitos.

## Stopping points

- **SP-01** (gate humano): aprobar mapeo y plan de actualizacion.
- **SP-02** (gate humano): aprobar diffs propuestos por UC.
- **SP-03** (gate tecnico): build strict 0 warnings tras cambios.

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Modificar UC_RPTs invalida specs existentes en domain-model y use-case-view | Solo actualizar casos-uso/; no tocar domain-model ni use-case-view sin decision explicita |
| R-02 | Algun SP no documentado afecta otros UC_RPTs no listados (UC_RPT_02..12, 14, 17) | Audit completo de mention "sp_rpt_" antes de proponer scope |
| R-03 | Los SPs requieren parametros del IVR (trimestre, segmentos) que no estan en el modelo de Django | Documentar mapping params del UC -> params del SP |
| R-04 | Las clases *ReportService del domain-model parecen genericas, podrian no reflejar SP delegation | Phase 3 verificacion explicita |
