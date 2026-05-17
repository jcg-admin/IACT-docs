```yml
created_at: 2026-05-06 08:08:00
project: IACT-docs
work_package: 2026-05-06-08-04-31-uc-rpt-stored-procedures-alignment
phase: Phase 1 — DISCOVER (consolida Phase 3 ANALYZE)
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Phase 1 DISCOVER — UC_RPT Stored Procedures Alignment

## 1. Hallazgo principal

Los **UC_RPT que dependen de stored procedures legacy del IVR**
NO reflejan esa realidad arquitectonica en su `flujo-principal
.rst`. Los flujos describen agregacion ORM-style ("Query
QueueDailyStat agregado") cuando el backend realmente ejecuta
`cursor.callproc('sp_rpt_*', [params])`.

## 2. Cobertura actual del corpus

### 2.1 Mapeo SP → UC_RPT (verificado)

| SP | UC primario | UC secundario | Mention en docs |
|---|---|---|---|
| `sp_rpt_llamadas_abandonadas` | UC_RPT_13 | — | 9 archivos |
| `sp_rpt_centros_transferencia` | UC_RPT_15 | — | 6 archivos |
| `sp_rpt_centros_xsegmento` | UC_RPT_15 | UC_RPT_01 | 14 archivos |
| `sp_rpt_menu_redirigidos` | UC_RPT_16 | — | 6 archivos |
| `sp_rpt_menu_centro` | UC_RPT_16 | — | 5 archivos |
| `sp_rpt_cMENU_ERROR` | UC_RPT_16 | — | 5 archivos |
| `sp_rpt_clientes` | UC_RPT_17 | — | 8 archivos |

**UCs afectados (5):** UC_RPT_01, UC_RPT_13, UC_RPT_15,
UC_RPT_16, UC_RPT_17.

### 2.2 Distribucion por zona del corpus

Los SPs SI estan documentados en zonas arquitectonicas:

| Zona | Cobertura |
|---|---|
| `arquitectura-tecnica/system-view/` | ✅ 6+ archivos |
| `arquitectura-tecnica/modulos/vis-reports/` | ✅ secuencia-sp-rpt-flujo-completo.rst (**canonico**) |
| `databases/etl-pipeline.rst` | ✅ los 7 SPs |
| `casos-uso/reports/uc-rpt-*/datos-involucrados.rst` | ⚠ mencion contextual |
| `casos-uso/reports/uc-rpt-*/diagramas-uml/secuencia.rst` | ⚠ 2/5 UCs (uc-rpt-13, uc-rpt-01 SI; uc-rpt-15, 16, 17 NO) |
| `casos-uso/reports/uc-rpt-*/flujo-principal.rst` | ❌ 0/5 UCs — **EL GAP** |

## 3. Patron arquitectonico canonico

`source/arquitectura-tecnica/modulos/vis-reports/diagramas/
secuencia-sp-rpt-flujo-completo.rst` v1.0.0 establece el
patron:

```
view_reports → DashboardEndpoint
DashboardEndpoint → JWT + RBAC verify
DashboardEndpoint → SegmentResolver.resolve(user_id)
SegmentResolver → returns [nacional_A, ...]

alt sin segmentos
  → 400 USER_WITHOUT_SEGMENT
else
  → ReportingService.callproc(sp_rpt_*, [Q1])
  → BD_IVR (base_ivr_detalle | base_ivr_clientes)
  → filas por segmento
  → 200 + datos del reporte
end
```

Este patron debe propagarse a los 5 `flujo-principal.rst`
afectados.

## 4. Gap por UC

### UC_RPT_01 — Dashboard / Centros por segmento

- `flujo-principal.rst`: ❌ no menciona SP, modela ORM.
- `diagramas-uml/diagrama-de-secuencia.rst`: ✅ usa
  `cursor.callproc(sp_rpt_centros_xsegmento)`.
- `datos-involucrados.rst`: ✅ menciona el SP.

**Fix requerido:** actualizar `flujo-principal.rst` con paso
explicito "PASO N — `cursor.callproc('sp_rpt_centros_xsegmento',
[period])` sobre `BD_IVR`".

### UC_RPT_13 — Llamadas Abandonadas

- `flujo-principal.rst`: ❌ "PASO 7 — Query QueueDailyStat
  agregado" + "PASO 8 — Calcular KPIs". Modela re-implementacion
  ORM en lugar de delegar al SP.
- `diagramas-uml/secuencia.rst`: ✅ usa
  `cursor.callproc(sp_rpt_llamadas_abandonadas)`.
- `diagramas-uml/actividad.rst`: ✅ menciona el SP.
- `datos-involucrados.rst`: ✅ menciona el SP.

**Fix requerido:** reemplazar PASO 7-8 con "PASO N —
`cursor.callproc('sp_rpt_llamadas_abandonadas', [period])` sobre
BD_IVR retorna filas pre-agregadas". Eliminar mencion de
"Calcular KPIs" porque el SP los devuelve calculados.

### UC_RPT_15 — Reporte Transferencias

- `flujo-principal.rst`: ❌ idem (a verificar).
- `diagramas-uml/actividad.rst`: ✅ menciona ambos SPs.
- `datos-involucrados.rst`: ✅ menciona ambos SPs.

**Fix requerido:** doble SP — usa
`sp_rpt_centros_transferencia` y `sp_rpt_centros_xsegmento`.
El flujo debe reflejar AMBAS llamadas en secuencia o segun
condiciones.

### UC_RPT_16 — Menu Reports (3 SPs)

- 3 SPs en mismo UC: `sp_rpt_menu_redirigidos`,
  `sp_rpt_menu_centro`, `sp_rpt_cMENU_ERROR`.
- `flujo-principal.rst`: ❌ no diferencia.
- `diagramas-uml/actividad.rst`: ✅ menciona los 3.

**Fix requerido:** documentar que el UC tiene 3 sub-vistas
(menu redirigidos, menu por centro, errores menu) cada una
con su SP. El flujo principal puede ser parametrizado por
sub-vista o tener 3 paso-2 alternos.

### UC_RPT_17 — Clientes IVR

- `flujo-principal.rst`: ❌ no menciona SP.
- `diagramas-uml/actividad.rst`: ✅ menciona `sp_rpt_clientes`.
- `diagramas-uml/flujo-de-anonimizacion-etl.rst`: ✅ menciona el SP.
- `datos-involucrados.rst`: ✅ menciona el SP.

**Fix requerido:** UC_RPT_17 tiene componente especial de
**anonimizacion ETL** previa al consumo del SP. El
`flujo-principal` debe documentar el orden:

1. Verify RBAC view_reports + view_pii_clientes.
2. ETL anonimizacion (si aplica para el segmento del usuario).
3. `cursor.callproc('sp_rpt_clientes', [period, anonymize=true])`.

## 5. Causa raiz

1. **Los UC_RPT se redactaron antes de validar la integracion
   con el legacy.** Asumieron re-implementacion ORM porque era
   el patron Django standard.
2. **`datos-involucrados.rst` se actualizo cuando se valido la
   fuente real (SPs)**, pero `flujo-principal.rst` no se
   sincronizo.
3. **Los diagramas de secuencia/actividad fueron ACTUALIZADOS
   correctamente** (uc-rpt-13 y uc-rpt-01 SI usan callproc),
   pero el flujo textual quedo divergente.
4. **Sin audit script** que detecte mismatch entre
   datos-involucrados (cita SP) y flujo-principal (modela ORM).

## 6. Decision de scope para Phase 5+

Opciones:

### Opcion A — Solo flujo-principal.rst de los 5 UCs

- Pros: scope quirurgico, ~5 archivos modificados.
- Contras: los `requisitos-no-funcionales`, `criterios-
  aceptacion`, `implementacion-tecnica` pueden seguir
  describiendo ORM. Inconsistencia parcial.
- Effort: ~30-45 min.

### Opcion B — Audit completo de los 5 UCs (todas las partes)

- Pros: alineacion total — todas las 12 partes del UC
  describen el mismo patron SP.
- Contras: scope mayor (~50-60 ediciones individuales).
- Effort: ~2-3 horas.

### Opcion C — Audit + fix completo + audit script C-08

- B + extender script con check C-08 "datos-involucrados ↔
  flujo-principal coherentes en mention de SPs".
- Effort: ~3-4 horas.

**Recomendacion:** Opcion B, deferrir el audit script a WP
sucesor para no inflar este WP.

## Stopping Point Manifest

| ID | Fase | Tipo | Evento | Accion |
|---|---|---|---|---|
| SP-01 | DISCOVER → STRATEGY | gate-humano | aprobar opcion (A/B/C) | Avanzar segun opcion |
| SP-02 | STRATEGY → EXECUTE | gate-humano | aprobar diffs propuestos | Aplicar |
| SP-03 | EXECUTE → TRACK | gate-tecnico | build strict 0 warnings | Cerrar WP |
