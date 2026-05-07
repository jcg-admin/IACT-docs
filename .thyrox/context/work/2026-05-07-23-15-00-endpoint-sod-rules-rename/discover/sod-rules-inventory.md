```yml
created_at: 2026-05-07 23:20:00
project: IACT-docs
work_package: 2026-05-07-23-15-00-endpoint-sod-rules-rename
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Inventory
```

# Inventario de referencias a `sod-rules` en docs

## 1. Resumen

- **20 referencias** en **11 archivos**.
- **18 referencias renombrables** (paths reales).
- **2 referencias preservar como ejemplo educativo** en STD-013.

## 2. Detalle por archivo

### A. uc-adm-01 (admin SoD rule mgmt) — 5 refs en 3 archivos

| # | Archivo | Linea | Texto actual | Accion |
|---|---|---|---|---|
| 1 | actores-precondiciones.rst | 32 | `POST /api/admin/sod-rules/` | rename |
| 2 | actores-precondiciones.rst | 39 | `PATCH /api/admin/sod-rules/{id}/` | rename |
| 3 | actores-precondiciones.rst | 42 | `POST /api/admin/sod-rules/{id}/disable/` | rename |
| 4 | flujo-principal.rst | 10 | `POST /api/admin/sod-rules/.` | rename |
| 5 | diagramas-uml/diagrama-de-actividad.rst | 12 | `:Invoker emite POST /api/v1/admin/sod-rules/;` | rename |

### B. uc-acc-05 (access SoD rule view) — 13 refs en 7 archivos

| # | Archivo | Linea | Texto actual | Accion |
|---|---|---|---|---|
| 6 | actores-precondiciones.rst | 31 | `\`\`/api/access/sod-rules/\`\` (GET/POST/` | rename |
| 7 | criterios-aceptacion.rst | 23 | `**DADO** GET \`\`/api/access/sod-rules/{id}/\`\`,` | rename |
| 8-12 | datos-involucrados.rst | 17,20,23,26,29 | `\`\`/api/access/sod-rules/...\`\`` | rename (5x) |
| 13 | diagramas-uml/diagrama-de-secuencia-crear-regla.rst | 19 | `Frontend -> Createsodruleview: POST /api/access/sod-rules/` | rename + alias |
| 14 | flujo-principal.rst | 22 | `PASO 1   GET /api/access/sod-rules/?...` | rename |
| 15 | flujo-principal.rst | 43 | `PASO 1   POST /api/access/sod-rules/` | rename |
| 16 | flujo-principal.rst | 78 | `PASO 1   PATCH /api/access/sod-rules/{id}/` | rename |
| 17 | flujo-principal.rst | 106 | `PASO 1   DELETE /api/access/sod-rules/{id}/` | rename |
| 18 | implementacion-tecnica.rst | 22 | `- GET \`\`/api/access/sod-rules/\`\`` | rename |
| 19 | testing.rst | 182 | `WHEN  GET /api/access/sod-rules/` | rename |

**Hallazgo adicional en linea 13:**
``Createsodruleview`` (alias UML). Es identificador, NO token
opaco — debe renombrarse a ``CreateSeparationRuleView`` para
alinear con backend A-002 (SeparationRuleViewSet).

### C. STD-013 (norma) — 2 refs en 1 archivo, **PRESERVAR**

| # | Archivo | Linea | Texto actual | Accion |
|---|---|---|---|---|
| 20 | std-013-rest-api-conventions.rst | 82 | `❌  /access/sod-rules` | **PRESERVAR** (ejemplo educativo de bad practice) |

(Solo 1 referencia in-scope en STD-013 — la linea 80 ya tiene
``✅ /access/separation-rules/validate``.)

## 3. Total de cambios planificados

- **18 rename** de path REST `sod-rules` -> `separation-rules`.
- **1 rename** de alias UML `Createsodruleview` -> `CreateSeparationRuleView`.
- **0 cambios** en STD-013 (preservar ejemplo educativo).
- **0 cambios** en `catalogo-funciones.rst` (tokens opacos).

**Total: 19 ediciones en 10 archivos in-scope** (excluye STD-013).

## 4. Plan de ejecucion sugerido

- 1 commit por archivo de UC (10 commits).
- Sin builds intermedios (R-2.0 — un solo build clean serial al final).
- Strict build deterministic (-W -j 1) en TR-01.

## 5. Validacion

Tras ejecutar todos los renames:

```bash
grep -rn "sod-rules" source/requisitos/ source/normativa/
```

Debe retornar UNA SOLA linea: la del ejemplo educativo en
STD-013 (linea 82, `❌  /access/sod-rules`).

## Refs

- Backend A-001..A-005 (rename SodRule -> SeparationRule).
- STD-013 §66, §80, §92, §138 (norma canonica
  separation-rules).
