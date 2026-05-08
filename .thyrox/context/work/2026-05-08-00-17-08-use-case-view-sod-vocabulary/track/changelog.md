```yml
created_at: 2026-05-08 01:30:00
project: IACT-docs
work_package: 2026-05-08-00-17-08-use-case-view-sod-vocabulary
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — use-case-view sod vocabulary cleanup

## [1.0.0] — 2026-05-08

### Changed (Cat-1: PlantUML aliases — 31 refs en 7 archivos)

`VALIDAR_SOD` → `VALIDAR_SEPARATION_RULES` en:

- access/uc-acc-01-asignar-funciones.rst (T-001)
- access/uc-acc-04-asignar-agrupador.rst (T-002)
- access/uc-acc-08-permiso-temporal.rst (T-003)
- admin/uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst (T-006)
- permissions/uc-perm-01-asignar-grupo-a-usuario.rst (T-009)
- permissions/uc-perm-03-conceder-permiso-excepcional.rst (T-010)
- permissions/uc-perm-06-asignar-funciones-a-grupo.rst (T-011)

`SOD_RULE_*` → `SEPARATION_RULE_*` en:

- admin/uc-adm-01-...-de-separacion.rst (3 refs, T-007)
- permissions/uc-perm-10-consultar-auditoria-de-permisos.rst (T-012)

### Changed (Cat-2: Captions plantuml — 7 refs)

"Validar SoD\n..." → "Validar regla de separacion\n..." o
"Validar separacion ..." segun contexto en los mismos
archivos arriba.

Extension point `PreviewSoDCascade` → `PreviewSeparationCascade`
(uc-perm-06).

UC titles "Reglas SoD" → "Reglas de Separacion" en:

- access/uc-acc-05-...-de-separacion.rst
- admin/uc-adm-01-...-de-separacion.rst

### Changed (Cat-3: Narrativa — 16+ refs)

"reglas SoD" → "reglas de separacion".
"SoD write-time" → "separacion write-time".
"ejecuta SoD" → "ejecuta validacion de separacion".
"Validacion SoD" → "Validacion de separacion".
"romper SoD" → "romper separacion".
"reglas estaticas SOD-001..003" PRESERVADO (codigos BD).

`SoDViolationSpec` → `SeparationRuleViolationSpec`.

Archivos afectados (ademas de los Cat-1):

- access/index.rst (3 refs body + caption)
- admin/index.rst (5 refs body + caption + toctree)
- mapa-funciones-rbac.rst (1 ref narrative)

### Renamed (Cat-4: filenames + toctrees + anchors)

**T-004 + T-005:**

- `access/uc-acc-05-gestionar-reglas-sod.rst` → `-de-separacion.rst`
- access/index.rst toctree updated.
- Anchor `_at_uc_acc_05_gestionar_reglas_sod` → `..._de_separacion`.

**T-007 + T-008:**

- `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` → `-de-separacion.rst`
- admin/index.rst toctree updated.
- Anchor `_at_uc_adm_01_gestionar_ciclo_de_vida_de_reglas_sod` → `..._de_separacion`.

### Preserved (excepciones)

- **Cross-ref `:doc:`/requisitos/reglas-negocio/rbac/sod``** en
  mapa-funciones-rbac.rst:184 — archivo externo, out-of-scope.
- **Codigos BD `SOD-001..003`** en uc-adm-01 narrative —
  IDs persistidos en `SeparationRule.code`; cambiarlos
  requiere migracion BD (TD-SOD-2 futuro).
- **Tokens opacos backend** `access:view_sod`,
  `access:update_sod`, `access:disable_sod` en
  catalogo-funciones.rst (fuera de use-case-view scope).

### Verification

```bash
$ grep -rnE "SoD|SOD|sod" source/arquitectura-tecnica/use-case-view/
# Solo 2 hits esperados:
# - mapa-funciones-rbac.rst:184 (cross-ref externo)
# - uc-adm-01-...-de-separacion.rst:24 (codigos BD)

$ find source/arquitectura-tecnica/use-case-view -name "*sod*.rst"
# Vacio
```

## Commits del WP (16 commits)

1. WP setup + Phase 1 audit (`c8bc9b39`).
2. Phase 1 extended + Phase 8 plan (`f7871be5`).
3. T-001..T-013 EXEC (13 commits).
4. (este commit) — TR-01 cierre.

## Diferido a WP futuro

- **TD-SOD-1:** rename `requisitos/reglas-negocio/rbac/sod.rst`
  → `separacion-de-deberes.rst` + actualizar todas las
  cross-refs.
- **TD-SOD-2:** verificar con backend si codigos
  `SOD-001..003` migran a `SR-NNN`. Si si, alinear docs +
  use-case-view + IACT-ui en WP coordinado.

## Build TR-02 diferido

Build serial deterministic al final de la cola de WPs.

## Refs

- discover/sod-audit.md (audit inicial).
- discover/rule-and-context.md (regla executor + IACT-ui).
- plan-execution/task-plan.md.
- WP `endpoint-sod-rules-rename` (cerrado).
- Backend A-001 (alineacion).
