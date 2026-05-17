```yml
project: IACT-docs
work_package: 2026-05-06-09-02-26-rbac-v5-6-0-corpus-alignment
created_at: 2026-05-06 09:02:26
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: grande (Stages 1, 5, 6, 8, 10, 11)
target: Bumpear el corpus IACT-docs de RBAC v5.5.0 → v5.6.0 con re-framing de scope. Activar MOD_Admin (NUEVO v5.6.0, 3 funciones) y declarar MOD_Operator (10 fn) + MOD_Supervision (3 fn) como extension points open-closed (out-of-scope para esta release, declarados en catálogo).
predecessor_wp: 2026-05-06-08-10-51-uc-rpt-sp-flujo-principal-rewrite (cerrado, alineación SP→UC)
trigger: directiva del ejecutor "tenemos un nuevo MOD de admin... MOD_Operator y MOD_Supervision están fuera de este scope, se mencionan porque se piensa como open close"
```

# WP — RBAC v5.6.0 Corpus Alignment

## Trigger

El ejecutor declaró que la versión vigente NO es v5.5.0 (74 fn) ni v5.4.0
sino **v5.6.0**, con dos cambios fundamentales:

1. **NUEVO MOD_Admin** (3 funciones) — declarado en
   `requisitos/reglas-negocio/rbac/catalogo-funciones.rst:658` como
   "NUEVO v5.6.0" pero el resto del corpus aún dice v5.5.0.
2. **MOD_Operator y MOD_Supervision son out-of-scope** — están en el
   catálogo (13 funciones combinadas) pero documentadas como **extension
   points open-closed**, NO activas en esta release.

## Framing canónico v5.6.0

```
                       RBAC v5.6.0
                            |
              ┌─────────────┴─────────────┐
              │                           │
       IN-SCOPE / ACTIVO              OUT-OF-SCOPE
       64 funciones                   (open-closed)
       9 módulos                      13 funciones
              │                       2 módulos
              ↓                            ↓
   Auth (4)                        MOD_Operator (10)
   Users (9)                       MOD_Supervision (3)
   Access (12)                          ↑
   Pipeline (4)                    Reservados / extension
   Reports (11) ← core              points; declarados
   Alerts (10)                      en catálogo pero no
   Audit (4)                        implementables en
   Logs (7)                         esta release.
   Admin (3) ← NUEVO v5.6.0
```

| Métrica | v5.5.0 (anterior) | v5.6.0 (actual) |
|---|---|---|
| Funciones activas | 74 (incluía OPR+SUP) | **64** |
| Funciones reservadas (open-closed) | — | **13** |
| Total catálogo declarado | 74 | **77** |
| Módulos activos | 11 | **9** |
| Módulos reservados | — | 2 |
| Grupos | 12 | 12 |
| Reglas SoD | 3 | 3 |

## Inventario de archivos a actualizar (~40)

Generado por `grep -rniE "RBAC v5\.[2-6]\.[0-9]+|7[3-7] funciones"
source/`. SVGs en `_generated_diagrams/` se omiten (build artifacts —
se regeneran al rebuildar PlantUML).

### Zona 1 — RBAC canónico (8 archivos)

- `arquitectura-tecnica/rbac/modelo-rbac-iact/index.rst` — :version:
  + nota MOD_Operator/MOD_Supervision (replantear)
- `arquitectura-tecnica/rbac/modelo-rbac-iact/arquitectura.rst:12,78`
  — "Distribución de 74 Funciones" + tabla con OPR+SUP in-scope
- `arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion.rst:98,
  190,194` — "74 Funciones (v5.5.0)" + comentario "v5.2.1"
- `arquitectura-tecnica/rbac/modelo-rbac-iact/modelo-datos.rst:16` —
  "74 funciones atómicas"
- `arquitectura-tecnica/rbac/modelo-rbac-iact/resumen.rst:57,116-126`
  — header v5.5.0 + footer v5.2.1 (doble desincronización)
- `arquitectura-tecnica/rbac/modelo-rbac-iact/diagramas/clases-
  entidades-rbac.rst:20`

### Zona 2 — Reglas de negocio RBAC (4)

- `requisitos/reglas-negocio/rbac/catalogo-funciones.rst:7` — "73 FUNCIONES"
- `requisitos/reglas-negocio/br-009-bajas-logicas.rst:218` — "v5.4.0"
- `requisitos/reglas-negocio/br-006-rbac-flat-nist.rst:135,168,213` —
  "74 funciones"

### Zona 3 — Base cognitiva (frontmatter compartido) (~12)

Boilerplate `"Sin Pretensiones" del modelo vigente v5.5.0: 74 funciones`
en línea 26-27 de:

- `_ontologia-sbvr/index.rst`
- `_ontologia-sbvr/sbvr-01..05*.rst` (5 archivos)
- `_taxonomias-y-metamodelos/metamodelos/mtm-01-...rst`
- `_taxonomias-y-metamodelos/metamodelos/mtm-03-metamodelo-rbac.rst:172,
  198,650`
- `_taxonomias-y-metamodelos/taxonomias/txm-01-...rst`
- `_taxonomias-y-metamodelos/taxonomias/txm-03-...rst`
- `_fundamentos-conceptuales/fnd-00-contexto-y-jerarquia.rst:247,283`
- `_fundamentos-conceptuales/fnd-03-casos-de-uso.rst:26,268,271,620`
- `_fundamentos-conceptuales/fnd-06-derivacion-vs-transformacion.rst:26`

### Zona 4 — Arquitectura técnica (modelo dominio + vistas) (~8)

- `arquitectura-tecnica/modelo-dominio-iact.rst:23,24,30,67,158,278,289`
- `arquitectura-tecnica/domain-model/overview.rst:42,46,83`
- `arquitectura-tecnica/domain-model/access-group-function.rst:22`
- `arquitectura-tecnica/context-view/context-diagram.rst:105`
- `arquitectura-tecnica/context-view/stakeholders.rst:34,94`
- `arquitectura-tecnica/perspectivas/perspectiva-security.rst:45`
- `arquitectura-tecnica/operational-view/system-installation.rst:52`
- `arquitectura-tecnica/matriz-dependencias-uc-iact.rst:31`

### Zona 5 — Backend ADRs (2)

- `backend/adr-back-005-middleware-decoradores-permisos.rst:85,557`
- `backend/adr-back-001-grupos-funcionales-sin-jerarquia.rst:22`

### Zona 6 — Normativa / gobernanza (5)

- `normativa/restricciones/cnst-029-rbac-modelo-plano.rst:184`
- `normativa/gobernanza/raci-rbac/index.rst:19`
- `normativa/gobernanza/raci-rbac/trazabilidad.rst:11`
- `normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual.rst:54,82,
  157,256`
- `normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm.rst:35`

### Zona 7 — Metodología y casos de uso (4)

- `requisitos/_metodologia-aplicacion/plan-documentacion-uc.rst:609`
- `requisitos/_metodologia-aplicacion/relaciones-uml/agregacion-grupo-
  agrega-funciones.rst:15`
- `requisitos/_metodologia-aplicacion/relaciones-uml/funcion-compuesta-
  funcion-funcion.rst:15`
- `requisitos/_metodologia-aplicacion/agregacion-interfaces/funcion-
  grupo-catalogo-rbac-iact.rst:27`
- `requisitos/casos-uso/admin/uc-adm-03/informacion-general.rst:26`
- `arquitectura-tecnica/use-case-view/admin/uc-adm-03-...rst:20`

## Plan de batches

| Batch | Zona | Archivos | Effort estimado |
|---|---|---|---|
| **B-1** | Zona 1 — RBAC canónico | 6 | ~30 min (alta criticidad — fuente de verdad) |
| **B-2** | Zona 2 — Reglas de negocio | 3 | ~15 min |
| **B-3** | Zona 3 — Base cognitiva (frontmatter) | 12 | ~30 min (mecánico) |
| **B-4** | Zona 4 — Arquitectura | 8 | ~25 min |
| **B-5** | Zona 5 + 6 — Backend + normativa | 7 | ~25 min |
| **B-6** | Zona 7 — Metodología + UC | 6 | ~15 min |

Total: **~2.5h wall-clock** + builds entre batches.

## Decisiones de redacción canónica

**1. Reemplazo de "74 funciones" → "64 funciones in-scope":**

Donde el contexto sea afirmación operativa del modelo vigente:
> "RBAC v5.6.0 con 64 funciones atómicas activas (más 13 reservadas
> open-closed para MOD_Operator y MOD_Supervision)"

Donde el contexto sea catálogo total declarado:
> "Catálogo de 77 funciones (64 activas + 13 reservadas)"

**2. Reemplazo de "11 módulos" → "9 módulos activos":**

> "9 módulos activos: MOD_Auth, MOD_Users, MOD_Access, MOD_Pipeline,
> MOD_Reports, MOD_Alerts, MOD_Audit, MOD_Logs, MOD_Admin"

**3. Tratamiento de MOD_Operator + MOD_Supervision:**

NO eliminar las secciones del catálogo (`catalogo-funciones.rst`
3.9 + 3.10). Reetiquetar con encabezado de status:
> "3.9 MOD_Operator (10 funciones) — RESERVADO v5.6.0 (extension
> point, out-of-scope para esta release)"

**4. Tabla de distribución (arquitectura.rst):**

Reorganizar en dos secciones:

- "2.1 Distribución de 64 Funciones Activas (v5.6.0)" — 9 módulos
- "2.2 Extension Points Reservados (open-closed)" — OPR + SUP

**5. Catálogo total:**

`catalogo-funciones.rst:7` cambia de "73 FUNCIONES" → "77 FUNCIONES
DECLARADAS (64 activas + 13 reservadas)".

## Restricciones

- **NO tocar** código de implementación real (sólo docs RST).
- Builds strict (`-W`) entre batches.
- Tim Pope commits.
- Logs de build a `execute/build-logs/`.

## Riesgos

| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Boilerplate de Zona 3 puede ser idéntico → cambio masivo con sed | Hacer Read-then-Edit por archivo (no sed batch) — preserva ortografía y diferencias sutiles |
| R-02 | Tabla de distribución en `arquitectura.rst` cambia su estructura → row-count varía → posible warning Sphinx en cross-refs | Build strict tras B-1 antes de continuar |
| R-03 | adr-gob-009 lista los 11 módulos explícitamente — orden importa | Replicar orden actual + nota de re-clasificación |
| R-04 | `catalogo-funciones.rst:7` "73" es ya inconsistente con la suma actual (77) — el bug existía antes del WP | Corregir en B-2 con la suma correcta |
| R-05 | UC_ADM_03 informacion-general menciona "12 agrupadores" — ese sí sigue siendo correcto (grupos no cambian) | NO tocar refs a "12 agrupadores"/"12 grupos" — sólo a "74 funciones" y "v5.5.0" |

## Stopping points

- **SP-01** (gate humano, ya): framing v5.6.0 + 64 in-scope + 13 open-
  closed aprobado por el ejecutor.
- **SP-02** (gate técnico per-batch): build strict 0 warnings tras
  cada batch.
- **SP-03** (gate humano final): cierre Phase 11 ordenado por el
  ejecutor.
