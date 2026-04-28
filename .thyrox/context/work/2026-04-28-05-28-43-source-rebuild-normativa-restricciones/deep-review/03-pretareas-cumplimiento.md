```yml
created_at: 2026-04-28 13:35:00
project: IACT-docs
work_package: 2026-04-28-05-28-43-source-rebuild-normativa-restricciones
phase: Phase 1 — DISCOVER
author: claude (deep-review agent)
status: Aprobado
version: 1.0.0
type: Deep-Review Artifact
source: wp-state.md + discover/*.md + source/normativa/restricciones/
topic: Cumplimiento de pre-tareas, D-CNST y riesgos heredados
```

# Deep-Review 03 — Cumplimiento de pre-tareas del WP

## Resumen ejecutivo

Cumplimiento global: **alto**. Las 5 pre-tareas, las 5 sub-decisiones D-CNST y los 2 riesgos heredados están documentados con evidencia trazable en los artefactos del WP. Se detectó **1 hallazgo bloqueante menor** (referencia stale `CNST_012` en MTM_03) y 7 hallazgos no bloqueantes — todos dentro del alcance permitido (≤8).

## Tabla de cumplimiento — Pre-tareas (5)

| # | Pre-tarea | Evidencia | Estado |
|---|-----------|-----------|--------|
| 1 | Lectura doc maestro `RESTRICCIONES_COMPLETAS_DEL_SISTEMA_IACT.md` | `discover/normativa-restricciones-analysis.md:19` (1135 líneas registradas); columna "Categoría doc maestro" en tabla de mapeo conceptual (líneas 25–38) | ✅ Cumplida |
| 2 | Lectura propuesta `ACTUALIZACION_DEL_ARBOL_SECCION_RESTRICCIONES.md` | `analysis.md:20` + `mapeo-viejo-nuevo.md:51-52` (versión 1.1.0 consolida la propuesta) | ✅ Cumplida |
| 3 | Inspección v2.0.0 standalone `CNST_05_Restriccion_Creacion_Iterativa_2_0_0.rst` | `analysis.md:21,69-77` (D-CNST-3 — descartado del cajón con razón explícita) | ✅ Cumplida |
| 4 | Mapeo source ↔ temp-holding ↔ doc maestro | `analysis.md:25-38` (tabla 3-columnas) | ✅ Cumplida |
| 5 | Tabla de mapeo viejo→nuevo (input WP #6) | `discover/mapeo-viejo-nuevo.md:19-32` + sección "Cambios de referencia obligatorios" (líneas 36-38) | ✅ Cumplida |

## Tabla de cumplimiento — Sub-decisiones D-CNST (5)

| ID | Decisión esperada | Resolución registrada | Evidencia |
|----|-------------------|------------------------|-----------|
| D-CNST-1 | Numeración nueva o respetar source | Respeta backup canónico, renumera sólo 012→011 para cerrar gap | `analysis.md:50-58` |
| D-CNST-2 | Huérfanas (incorporar/descartar/fusionar) | "No hay huérfanas conceptuales" — TH CNST_004/006/007 subsumidas en CNST_001/007 | `analysis.md:60-67` |
| D-CNST-3 | v2.0.0 standalone | Descartado del cajón (regla de proceso, no de sistema); diferido a procedimientos | `analysis.md:69-77` |
| D-CNST-4 | Llenar gap CNST_011 | Cierre por renumeración 012→011 (sin contenido inventado, respeta out-of-scope wp-state:73) | `analysis.md:79-84` |
| D-CNST-5 | Sub-categorías flat o agrupadas | Flat por número en filesystem; agrupación por dominio expuesta vía `index.rst` | `analysis.md:86-93` + `restricciones/index.rst:42-60` |

## Tabla de cumplimiento — Riesgos heredados (2)

| ID | Riesgo | Mitigación verificable | Estado |
|----|--------|------------------------|--------|
| R1 | WP #6 requisitos consume CNSTs (bloqueante) | `discover/mapeo-viejo-nuevo.md` entrega tabla canónica viejo→nuevo + cambios de referencia obligatorios | ✅ Mitigado |
| R2 | Pérdida de CNST huérfana | D-CNST-2 valida que ninguna CNST temp-holding aporta concepto ausente (subsumidas documentadas) | ✅ Mitigado |

## Verificación de artefactos

| Artefacto esperado | Existe | Notas |
|--------------------|--------|-------|
| `discover/normativa-restricciones-analysis.md` | ✅ | status: Aprobado, version 1.0.0 |
| `discover/mapeo-viejo-nuevo.md` | ✅ | status: Aprobado, version 1.0.0 |
| `source/normativa/restricciones/` | ✅ | 11 archivos CNST_001…CNST_011 + index.rst (verificado con `ls`) |
| `source/normativa/index.rst` incluye `restricciones/index` | ✅ | toctree presente líneas 30+ del index padre |
| Inputs declarados en `temp-holding/` | ✅ | Los 3 archivos de input verificados con `ls` |

## Hallazgos (≤8)

### F-1 — BLOQUEANTE MENOR — Referencia stale `CNST_012` en MTM_03
- **Origen:** `source/base_cognitiva/_taxonomias_y_metamodelos/metamodelos/MTM_03_Metamodelo_RBAC.rst:701`
- **Texto literal:** `"materializacion concreta ... esta documentada como restricción **CNST_012** en normativa/restricciones/ (dominio aún no integrado al toctree público durante el rebuild)"`
- **Contradicción:** D-CNST-1 renumeró 012→011 y el toctree YA está integrado (verificado en `restricciones/index.rst:32-42` y `normativa/index.rst`).
- **Impacto:** R3 (línea 126-128 de analysis.md afirma "ningún archivo en source/ actual referencia CNST_012") es **falso parcial** — MTM_03 sí lo referencia.
- **Acción recomendada:** Update MTM_03:701 → `CNST_011` y eliminar la cláusula "(dominio aún no integrado al toctree público)". Antes de cerrar el WP.

### F-2 — Inconsistencia en tabla mapeo conceptual (analysis.md:38)
- La fila final dice `CNST_012 RBAC_Flat_SoD_Permisos` pero el set canónico final tiene **CNST_011** (renumerado).
- **Impacto:** Bajo — la tabla documenta el ANTES de la decisión D-CNST-1; coherente con la lectura cronológica. No requiere cambio si se interpreta como "Backup canónico (pre-renumeración)".
- **Acción recomendada:** opcional — agregar nota al pie aclarando que la columna refleja el backup pre-renumeración.

### F-3 — Versión declarada 1.1.0 sin justificación SemVer en mapeo-viejo-nuevo.md
- `mapeo-viejo-nuevo.md:52` declara "Versión metadata: 1.1.0" — corresponde a la propuesta `ACTUALIZACION_DEL_ARBOL`. CNST_011 efectivamente lleva `:version: 1.1.0`.
- **Impacto:** Bajo. La propuesta original era "descongelar 10 CNST a v1.1.0" — solo 11 archivos llevan 1.1.0; consistente.
- **Acción recomendada:** ninguna.

### F-4 — D-CNST-3 deferral sin tracking
- `analysis.md:75` difiere v2.0.0 standalone "a una iteración futura del WP de procedimientos / metodología" pero no hay TD-NNN ni handoff registrado.
- **Impacto:** Riesgo de pérdida del input. No bloquea cierre del WP actual (out-of-scope confirmado en wp-state:73).
- **Acción recomendada:** crear entrada en `.thyrox/context/technical-debt.md` o handoff explícito al WP de procedimientos antes del cierre.

### F-5 — Pre-tarea 4 cumple pero el doc maestro no aparece en `mapeo-viejo-nuevo.md`
- La tabla de mapeo solo tiene 3 columnas (backup / temp-holding / nuevo). No hay columna "doc maestro" en `mapeo-viejo-nuevo.md` (sí en `analysis.md:25-38`).
- **Impacto:** Bajo — el mapeo viejo→nuevo no necesita doc maestro como columna (no es input directo de WP #6).
- **Acción recomendada:** ninguna; cumplimiento aceptado vía `analysis.md`.

### F-6 — `BR-006` mencionado en CNST_011 sin trazabilidad
- `CNST_011_RBAC_Flat_SoD_Permisos.rst:25` referencia `BR-006 (regla de negocio pendiente de WP requisitos)`.
- **Impacto:** Aceptable como handoff a WP #6. Confirma R1 — el mapeo viejo→nuevo debe transportar también este link.
- **Acción recomendada:** ninguna en este WP; verificar en kickoff de WP #6.

### F-7 — Plan de ejecución (analysis.md:106-118) lista 9 pasos, no hay evidencia de checklist completado
- El analysis cierra con plan de ejecución pero no hay artefacto que confirme "build limpio (0 warnings)" ni que los 3 deep-reviews paralelos hayan corrido todos.
- **Impacto:** Medio. Este deep-review es el `03-` (de 3+); falta confirmar que 01 y 02 existen y están aprobados.
- **Acción recomendada:** verificar existencia de `deep-review/01-*.md` y `deep-review/02-*.md` antes de cerrar WP. Si faltan, no cerrar.

### F-8 — Anti-sesgo cumplido
- Las decisiones D-CNST-1…5 derivan de evidencia documentada (mapeo conceptual + categorías doc maestro), no de hipótesis a priori.
- D-CNST-2 ("no hay huérfanas") es un claim falsable y verificado por la tabla — no un descarte por sesgo.
- **Impacto:** ninguno (confirmación positiva).

## Recomendación final

**NO CERRAR el WP todavía.** Tres acciones bloqueantes mínimas antes del gate:

1. **Fijar F-1** — actualizar `MTM_03_Metamodelo_RBAC.rst:701` (CNST_012 → CNST_011 y limpiar cláusula obsoleta sobre toctree). Sin esto, R3 documentado en `analysis.md:126-128` queda como claim falso.
2. **Resolver F-7** — confirmar que los deep-reviews 01 y 02 paralelos existen y están aprobados; si no, completarlos.
3. **Resolver F-4** — registrar el deferral de v2.0.0 standalone en `technical-debt.md` o como handoff explícito al WP de procedimientos.

Con esas tres acciones fijadas, el cumplimiento de pre-tareas, D-CNST y riesgos heredados está completo y el WP es candidato válido para gate Phase 1 → Phase 2 (o cierre directo si la estrategia padre lo permite).

**Items correctamente cubiertos:** 12 de 12 (5 pre-tareas + 5 D-CNST + 2 riesgos).
**Hallazgos:** 8 (1 bloqueante menor, 1 medio, 6 bajos / informativos).
