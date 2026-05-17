```yml
project: IACT-docs
work_package: 2026-05-06-08-10-51-uc-rpt-sp-flujo-principal-rewrite
created_at: 2026-05-06 08:10:51
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 5, 6, 8, 10, 11)
target: Ejecutar opcion B aprobada por el ejecutor en WP DISCOVER predecesor — alinear las 12 partes de los 5 UC_RPT (UC_RPT_01, 13, 15, 16, 17) con la realidad arquitectonica: el backend ejecuta cursor.callproc('sp_rpt_*') sobre BD_IVR legacy, NO agregacion ORM Django.
predecessor_wp: 2026-05-06-08-04-31-uc-rpt-stored-procedures-alignment (cerrado, contiene el analisis y el patron canonico)
canonical_pattern: source/arquitectura-tecnica/modulos/vis-reports/diagramas/secuencia-sp-rpt-flujo-completo.rst
```

# WP — UC_RPT SP Flujo Principal Rewrite

## Trigger

WP predecesor `uc-rpt-stored-procedures-alignment` aprobo
opcion B en SP-01: audit completo de las 12 partes de los 5
UC_RPT afectados.

## Mapeo SP → UC (heredado del predecesor)

| SP | UC | Detalle |
|---|---|---|
| `sp_rpt_centros_xsegmento` | UC_RPT_01 | Dashboard / centros por segmento |
| `sp_rpt_llamadas_abandonadas` | UC_RPT_13 | Reporte de abandono por queue |
| `sp_rpt_centros_transferencia` + `sp_rpt_centros_xsegmento` | UC_RPT_15 | Doble SP — transferencias + contexto |
| `sp_rpt_menu_redirigidos` + `sp_rpt_menu_centro` + `sp_rpt_cMENU_ERROR` | UC_RPT_16 | Triple SP — 3 sub-vistas de menu |
| `sp_rpt_clientes` | UC_RPT_17 | Clientes IVR con anonimizacion ETL |

## Patron canonico (heredado)

Documentado en `arquitectura-tecnica/modulos/vis-reports/
diagramas/secuencia-sp-rpt-flujo-completo.rst`:

```
view_reports → DashboardEndpoint
JWT + RBAC verify
SegmentResolver.resolve(user_id) → segmentos del usuario
alt sin segmentos
  → 400 USER_WITHOUT_SEGMENT
else
  ReportingService.callproc('sp_rpt_*', [period, ...])
  → BD_IVR.CALL sp_rpt_*
  → filas pre-agregadas
  → 200 + datos
end
```

## Scope: 12 partes × 5 UCs = 60 archivos potenciales

Por UC, 12 partes a auditar/actualizar:

1. `informacion-general.rst` — descripcion general (puede mencionar SP).
2. `actores-precondiciones.rst` — RBAC + DataSegment requerido.
3. `flujo-principal.rst` — **EL CRITICAL** — debe usar callproc.
4. `flujos-alternos.rst` — alternativas (e.g. cache hit, segment vacio).
5. `excepciones.rst` — errores del SP (timeout, datos invalidos).
6. `datos-involucrados.rst` — entradas/salidas del SP.
7. `criterios-aceptacion.rst` — verificar mencion del SP en
   acceptance criteria.
8. `requisitos-no-funcionales.rst` — performance del SP, cache.
9. `implementacion-tecnica.rst` — Django ReportingService + DRF.
10. `patrones-diseno.rst` — Repository + Strategy patterns.
11. `testing.rst` — mock del cursor.callproc.
12. `diagramas-uml/` — actividad y secuencia (ya alineados en
    algunos UCs per WP predecesor).

## Estrategia

Por cada UC (B-1..B-5), revisar las 12 partes con grep + lectura
y aplicar fix donde el contenido contradiga o ignore el SP. NO
es necesario reescribir partes que ya esten correctas.

## Stopping points

- **SP-01** (gate humano): ya aprobado en WP predecesor.
- **SP-02** (gate tecnico per-UC): build strict 0 warnings tras
  cada UC completo.
- **SP-03** (gate tecnico final): audit final + build strict +
  cierre.

## Plan de batches

| Batch | UC | SPs | Effort estimado |
|---|---|---|---|
| **B-1** | UC_RPT_01 | sp_rpt_centros_xsegmento | ~30 min |
| **B-2** | UC_RPT_13 | sp_rpt_llamadas_abandonadas | ~30 min |
| **B-3** | UC_RPT_15 | sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento | ~40 min (doble SP) |
| **B-4** | UC_RPT_16 | sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR | ~50 min (triple SP) |
| **B-5** | UC_RPT_17 | sp_rpt_clientes + ETL anonimizacion | ~40 min (caso especial) |

Total estimado: **~3.5h wall-clock**.

## Restricciones

- **No tocar** `domain-model/` ni `use-case-view/` (cerrados).
- **No tocar** codigo Python real del backend.
- **Solo `casos-uso/reports/uc-rpt-{01,13,15,16,17}/`** y sus 12 partes.

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Algunas partes ya estan correctas — sobre-modificar | Audit-first: leer antes de editar |
| R-02 | Modificar `criterios-aceptacion` puede invalidar tests downstream | Marcar cambios sustantivos en commit |
| R-03 | Triple SP en UC_RPT_16 puede generar 3 sub-flujos confusos | Documentar como sub-vistas alternas, NO 3 flujos paralelos |
| R-04 | UC_RPT_17 anonimizacion ETL es caso especial | Documentar el orden: ETL anonymize → callproc |
