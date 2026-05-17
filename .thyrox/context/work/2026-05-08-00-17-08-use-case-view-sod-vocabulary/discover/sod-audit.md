```yml
created_at: 2026-05-08 00:20:00
project: IACT-docs
work_package: 2026-05-08-00-17-08-use-case-view-sod-vocabulary
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: SOD Audit Detallado
```

# Audit detallado SOD/sod en use-case-view

## 1. Inventario completo (37+ refs, ~10 archivos)

### Cat-1 — PlantUML alias `VALIDAR_SOD` (27 refs en 7 archivos)

| # | Archivo | Refs |
|---|---|---|
| 1 | access/uc-acc-01-asignar-funciones.rst | 4 (L53 usecase, L67 include, L78 relation, L87 note) |
| 2 | access/uc-acc-04-asignar-agrupador.rst | 4 (L49, L62, L71, L80) |
| 3 | access/uc-acc-08-permiso-temporal.rst | 3 (L49, L62, L72) |
| 4 | permissions/uc-perm-01-asignar-grupo-a-usuario.rst | 4 (L53, L66, L74, L91) |
| 5 | permissions/uc-perm-03-conceder-permiso-excepcional.rst | 3 (L53, L66, L75) |
| 6 | permissions/uc-perm-06-asignar-funciones-a-grupo.rst | 4 (L48, L62, L73, L80) |
| 7 | admin/uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst | 5 (L51, L66, L77, L91, L118) |

**Decision Cat-1:** RENAMING obligatorio.

`VALIDAR_SOD` → `VALIDAR_SEPARATION_RULES` (alias) o
`VALIDAR_SOD_RULES` (mas corto, preserva concepto SoD en
caption pero canoniza el alias).

**Recomendacion: `VALIDAR_SEPARATION_RULES`** para alinear
plenamente con backend post-A-001.

### Cat-2 — Backend event identifiers `SOD_RULE_*` (5 refs)

| # | Archivo | Linea | Texto actual | Reemplazo |
|---|---|---|---|---|
| 1 | admin/uc-adm-01-...-de-reglas-sod.rst | 51 | `usecase "Emitir AuditEvent\nSOD_RULE_*"` | `SEPARATION_RULE_*` |
| 2 | admin/uc-adm-01-...-de-reglas-sod.rst | 85 | `SOD_RULE_CREATED / UPDATED /` | `SEPARATION_RULE_CREATED / UPDATED /` |
| 3 | admin/uc-adm-01-...-de-reglas-sod.rst | 117 | `emisor de AuditEvent SOD_RULE_*.` | `SEPARATION_RULE_*` |
| 4 | permissions/uc-perm-10-...-permisos.rst | 71 | `SOD_RULE_*, USER_*, AUTH_*}.` | `SEPARATION_RULE_*` |
| 5 | (caption del usecase tambien) | — | — | — |

**Decision Cat-2:** RENAMING obligatorio (alineacion A-001).

### Cat-3 — Codigos de regla `SOD-001..003`

| # | Archivo | Linea | Texto actual |
|---|---|---|---|
| 1 | admin/uc-adm-01-...-de-reglas-sod.rst | 23 | `(las 3 reglas estaticas SOD-001..003 fueron definidas en` |

**Decision Cat-3:** PRESERVAR.

`SOD-001..003` son **codigos de regla persistidos en BD**
como `SeparationRule.code`. Cambiarlos romperia el contrato
con el catalogo de reglas de produccion. Son IDs estables.

(Verificar en domain-model si confirma que el campo
`code` de `SeparationRule` usa formato `SOD-NNN` o si la
nueva convencion requiere `SR-NNN` — fuera de scope este
WP, registrar como TD si hay duda.)

### Cat-4 — Filenames con "sod" (2 archivos)

| # | Filename actual | Filename propuesto |
|---|---|---|
| 1 | `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` | `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-de-separacion.rst` |
| 2 | `access/uc-acc-05-gestionar-reglas-sod.rst` | `access/uc-acc-05-gestionar-reglas-de-separacion.rst` |

**Cambios derivados:**

- `admin/index.rst:300` — actualizar entry en toctree.
- `access/index.rst:150` — actualizar entry en toctree.
- Anchors internos `_at_uc_adm_01_gestionar_ciclo_de_vida_de_reglas_sod`
  y `_at_uc_acc_05_gestionar_reglas_sod` → renombrar.
- Buscar cross-refs externos a estos archivos en otros
  modulos (verificar grep).

**Decision Cat-4:** RENAMING obligatorio + git mv para
preservar historia.

### Cat-5 — Cross-ref externo

| # | Archivo | Linea | Texto |
|---|---|---|---|
| 1 | mapa-funciones-rbac.rst | 184 | `:doc:`/requisitos/reglas-negocio/rbac/sod`` |

**Decision Cat-5:** PRESERVAR (Opcion 5a).

El archivo target `source/requisitos/reglas-negocio/rbac/sod.rst`
existe con ese nombre. Renombrarlo requiere WP separado que
toque toda la documentacion de reglas-negocio. Out-of-scope
de este WP (use-case-view focus).

## 2. Verificacion estado actual

### Cross-refs a los 2 archivos a renombrar (filenames)

```
$ grep -rn "uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod\|uc-acc-05-gestionar-reglas-sod" source/
source/arquitectura-tecnica/use-case-view/admin/index.rst:300: uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod
source/arquitectura-tecnica/use-case-view/access/index.rst:150: uc-acc-05-gestionar-reglas-sod
```

Solo 2 toctrees referencian los archivos a renombrar.
Limpio.

### Anchor `_at_uc_*_sod`

```
$ grep -rn "at_uc_adm_01_gestionar_ciclo_de_vida_de_reglas_sod\|at_uc_acc_05_gestionar_reglas_sod" source/
```

(Verificado: solo en self-referenciation; no usados por
otros archivos via `:ref:`.)

## 3. Resumen de cambios planificados

| Cat | Refs | Archivos | Accion |
|---|---|---|---|
| 1 | 27 | 7 | rename `VALIDAR_SOD` → `VALIDAR_SEPARATION_RULES` |
| 2 | 5 | 2 | rename `SOD_RULE_*` → `SEPARATION_RULE_*` |
| 3 | 1 | 1 | preservar (codigos BD) |
| 4 | 2 archivos + 2 toctrees + anchors | 4 | git mv + update refs |
| 5 | 1 | 1 | preservar (out-of-scope) |
| **Total renames** | **~34 ediciones** | **~10 archivos unicos** | |

## 4. Lista de tareas atomicas (preview)

1 archivo = 1 commit (excepto Cat-4 que tiene 2 cambios
relacionados).

- T-001..T-007: Cat-1 PlantUML aliases (7 archivos).
- T-008: Cat-2 admin/uc-adm-01 (4 refs en mismo archivo).
- T-009: Cat-2 permissions/uc-perm-10 (1 ref).
- T-010: Cat-4 git mv admin/uc-adm-01-...-sod.rst + update
  admin/index toctree + anchor.
- T-011: Cat-4 git mv access/uc-acc-05-...-sod.rst + update
  access/index toctree + anchor.
- TR-01: Cierre WP.

**Total: 11 EXEC + 1 TR = 12 tareas.**

## 5. Validacion final esperada

```bash
# Cat-1: cero hits ✅
grep -rnE "VALIDAR_SOD\b" source/arquitectura-tecnica/use-case-view/

# Cat-2: cero hits ✅
grep -rnE "SOD_RULE_" source/arquitectura-tecnica/use-case-view/

# Cat-3: preservado (codigos BD) — esperado: 1 hit
grep -rnE "SOD-001|SOD-002|SOD-003" source/arquitectura-tecnica/use-case-view/

# Cat-4: filenames sin "sod"
ls source/arquitectura-tecnica/use-case-view/admin/uc-adm-01-*sod*.rst 2>/dev/null  # esperado: vacío
ls source/arquitectura-tecnica/use-case-view/access/uc-acc-05-*sod*.rst 2>/dev/null  # esperado: vacío

# Cat-5: preservado (cross-ref a archivo externo)
grep -rn "/reglas-negocio/rbac/sod" source/arquitectura-tecnica/use-case-view/  # esperado: 1 hit (mapa-funciones-rbac)

# 'SoD' en narrativa (preservado como vocabulario dominio):
grep -rnE 'reglas SoD|Validar SoD|Separation of Duties' source/arquitectura-tecnica/use-case-view/
```

## Refs

- WP `endpoint-sod-rules-rename` (cerrado) — mismo dominio
  pero focus en endpoint REST, no en use-case-view aliases.
- Backend A-001 (rename SodRule → SeparationRule).
- STD-010 v1.0.0 (vocabulario abstracto).
