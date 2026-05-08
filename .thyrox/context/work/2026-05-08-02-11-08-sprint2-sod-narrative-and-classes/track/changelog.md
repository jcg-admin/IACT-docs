```yml
created_at: 2026-05-08 03:00:00
project: IACT-docs
work_package: 2026-05-08-02-11-08-sprint2-sod-narrative-and-classes
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — Sprint 2 (SoD narrative + identifiers cleanup)

## [1.0.0] — 2026-05-08

### Changed (~1100 refs procesadas en 11 subdirectorios)

WP-B + WP-C combinados. WP-E (Factory/Builder/Manager)
**diferido** a WP separado por volumen + necesidad de
verificacion caso-por-caso del rol de cada clase.

### Por subdirectorio

| Bloque | Subdir | Refs procesadas | Commit |
|---|---|---|---|
| 1 | `business-requirements/` | 2 | sandbox |
| 2 | `requisitos-funcionales/` | 41 | 8 archivos |
| 3 | `domain-model/` | 27 | clase identifiers |
| 4 | `backend/` | 44 | events + identifiers |
| 5 | `_metodologia-aplicacion/` | 28 | narrativa + identifiers |
| 6 | `reglas-negocio/` | 56 | normas RBAC |
| 7 | `gestion/` | 62 | evidencia rbac-historia |
| 8 | `normativa/` | 83 | restricciones + raci |
| 9 | `base-cognitiva/` | 119 | metamodelos + glosario |
| 10 | `casos-uso/` | 629 | bloque mayor |
| 11 (final) | `arquitectura-tecnica/` (excl. UCV/DM) | 96 | residual |
| 12 (final) | normativa STD-* meta-normativos | 22 | ejemplos |

**Total: ~1209 refs procesadas en ~12 commits.**

### Tipos de transformacion aplicadas

**Identificadores tecnicos:**

- `VALIDAR_SOD` (alias plantuml) → `VALIDAR_SEPARATION_RULES`
- `SOD_RULE_*` (events) → `SEPARATION_RULE_*`
- `SOD_RULES` (constants) → `SEPARATION_RULES`
- `SoDRule`, `SoDRuleRepo`, `SoDRuleService`, `SoDRuleCache` →
  `SeparationRule`, `SeparationRuleRepo`, etc.
- `SoDValidator` → `SeparationRuleValidator`
- `SoDViolation`, `SoDViolationSpec` →
  `SeparationRuleViolation`, `SeparationRuleViolationSpec`
- `SoDRuleEndpoint`, `SoDRuleNotFound`, etc.
- `SoDComplianceReport` → `SeparationComplianceReport`
- `SoDPreCheckValidator` → `SeparationPreCheckValidator`
- `SoDRuleAlreadyExists`, `SoDRuleDuplicate`, etc.
- `validate_sod`, `validar_sod` → `validate_separation`,
  `validar_separacion`
- `enforce_sod` → `enforce_separation`
- `CASCADE_SOD_VIOLATION` → `CASCADE_SEPARATION_VIOLATION`
- `SOD_RULES_VIEWED` → `SEPARATION_RULES_VIEWED`
- `SOD_VIOLATION` → `SEPARATION_VIOLATION`
- `configure_sod` → `configure_separation_rules`
- `manage_sod` → `manage_separation_rules`
- `validateSoD` → `validateSeparation`
- `gestiona_sod` → `gestiona_separation`
- `ReglaSoD` → `ReglaSeparacion`
- `SoDEnforcer` → `SeparationRuleEnforcer`
- `SoDRuleFunction` → `SeparationRuleFunction`
- `SoDRuleDetail` → `SeparationRuleDetail`
- `SoDRepository` → `SeparationRuleRepository`
- `SoDCheckView` → `SeparationCheckEndpoint`
- Anchors `:ref:` `_*_sod*` → `_*_separacion*`

**Filenames de path que tenian sod:**

- `apps/access/sod.py` → `apps/access/separation.py`
- `sod_views.py::list_sod` → `separation_views.py::list_separation_rules`
- `BR_007_Separacion_Funciones_SoD.rst` →
  `BR_007_Separacion_Funciones.rst`
- `UC_ADM_01_Gestionar_Ciclo_Vida_SoD.rst` →
  `UC_ADM_01_Gestionar_Ciclo_Vida_Separacion.rst`

**Narrativa expandida (a "separacion de deberes"):**

- "reglas SoD" → "reglas de separacion"
- "Validar SoD" → "Validar separacion"
- "validacion/restricciones/conflicto/configuracion SoD" →
  formas con "de separacion"
- "SoD write-time" → "separacion write-time"
- "SoD compliance" → "compliance de separacion"
- "SoD cascade" → "separacion cascade"
- "(SoD)" parentetical → "(separation of duties)"
- "Separacion de Funciones SoD" → "...(separation of duties)"

**Captions plantuml:**

- "Validar SoD" → "Validar separacion" / "Validar regla de separacion"
- "Gestionar SoD" → "Gestionar separacion de deberes"
- "Detectar SoD" → "Detectar separacion"

**Codes/identifiers en pseudocodigo:**

- `"sod-001"`, `"sod-NNN"` → `"sr-001"`, `"sr-NNN"`
- `"validate-sod"` URL → `"validate-pii"` (en ejemplos negativos)

### Excepciones FINALES preservadas (3 categorias)

#### 1. Codigos BD persistidos (59 refs)

`SOD-001`, `SOD-002`, `SOD-003`, `SOD-NNN`.

Razon: campo `SeparationRule.code` en BD usa este formato.
Cambiar requiere migracion de datos coordinada con backend.
Documentado en CLEAN_CODE §8.3 + STD-010 §5.5.

#### 2. Tokens RBAC opacos backend (5 refs)

`access:view_sod`, `access:update_sod`, `access:disable_sod`.

Razon: contrato de integracion con backend RBAC. Cambiar
rompe la integracion sin beneficio. Documentado en
CLEAN_CODE §8.3.

#### 3. URLs externas a paper Purdue (3 refs)

`https://www.cs.purdue.edu/homes/ninghui/papers/sod-j.pdf`

Razon: es un path real de un recurso publicado en
cs.purdue.edu. Cambiar el path rompe el link al recurso.
No es un identificador del proyecto sino una **cita
academica** a contenido externo.

### Verification

```bash
$ grep -rnE "SOD|SoD|sod\b" source/ \
    | grep -vE "SOD-00[0-9]|access:[a-z_]*_sod|purdue\.edu/homes/ninghui/papers/sod-j\.pdf" \
    | wc -l
0  ✅
```

### WP-E (Factory/Builder/Manager) — DIFERIDO

Razones:

- 20 clases (Factory + Builder + Manager) requieren
  verificacion caso-por-caso del rol real (criterio D3).
- Sprint 2 ya alcanzo ~1200 refs solo en SoD; sumar 20
  renames de clase + sus refs derivadas excede capacidad
  practica.

Se abrira WP separado para WP-E.

### Sprint 2 cerrado

Roadmap audit clean-code-naming:

| WP | Estado |
|---|---|
| WP-A | ✅ Sprint 1 |
| WP-B | ✅ Sprint 2 (casos-uso 629 refs) |
| WP-C | ✅ Sprint 2 (backend/dm/normativa/etc) |
| WP-D | ✅ resuelto en naming-rules-resolution |
| WP-E | ⏸ DIFERIDO a WP separado |
| WP-F | ⏸ Sprint 3 disponible |
| WP-G | ⏸ Sprint 3 disponible |
| WP-H | ✅ Sprint 1 |

## Refs

- WP `clean-code-naming-audit` (audit-only).
- WP `naming-rules-resolution` (D1-D4 aplicadas).
- WP `sprint1-filenames-and-factory` (Sprint 1).
- CLEAN_CODE_NAMING_PRINCIPLES §1.4, §6.2, §8.2, §8.3.
- STD-010 v1.1.0 §2.4, §5.4, §5.5.
- backend/conventions.rst v2.0.0.
