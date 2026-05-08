```yml
created_at: 2026-05-08 00:50:00
project: IACT-docs
work_package: 2026-05-08-00-17-08-use-case-view-sod-vocabulary
phase: Phase 1 — DISCOVER (extended)
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Rule + Opinion + Context Documentation
```

# Regla "no Sod en identificadores" — documentacion completa

## 1. Directiva del ejecutor (literal)

> "no queremos nada que diga Sod, porque puede confundir"

Esta directiva amplia el alcance del WP de "renombrar
identificadores tecnicos SOD" (audit inicial) a
**"eliminar todas las apariciones de Sod/SOD en cualquier
forma controlada por el proyecto, salvo excepciones
explicitas".**

## 2. Razonamiento del ejecutor (transcrito)

El termino "Sod" causa confusion porque mezcla:

- **Identificador tecnico** (`SOD_RULE_CREATED`,
  `VALIDAR_SOD`).
- **Concepto de dominio** (regla de separacion).
- **Acronimo regulatorio** (Separation of Duties).

Las tres formas (mayus/mixta/minus) hacen que un lector
no sepa si esta leyendo codigo, dominio o terminologia.
La forma desambiguada es:

- Identificadores tecnicos: `SEPARATION_RULES`,
  `SeparationRuleValidator`, `validateSeparation`.
- Conceptos de dominio en prosa: "reglas de Separacion de
  Deberes", "Separation of Duties" (forma larga, clara).

## 3. Contexto IACT-ui (referenciado por ejecutor)

El ejecutor describio el alcance equivalente en el repo
**IACT-ui** (frontend) — repo separado de IACT-docs pero
gobernado por el mismo principio:

### Categoria 1 — Identificadores que violan CLEAN_CODE_NAMING_PRINCIPLES

| Archivo IACT-ui | Identificador prohibido | Correccion |
|---|---|---|
| FunctionSelector.jsx | `const SOD_RULES = {...}` | `const SEPARATION_RULES = {...}` |
| SoDValidator.jsx | `const SOD_RULES_INFO = {...}` | `const SEPARATION_RULES_INFO = {...}` |
| SoDValidator.jsx | `function SoDValidator` | `function SeparationRuleValidator` |
| SoDManagementPage.jsx | `const SOD_RULES_DATA` | `const SEPARATION_RULES_DATA` |
| SoDManagementPage.jsx | `const [sodRules, setSodRules]` | `const [separationRules, setSeparationRules]` |
| SoDManagementPage.jsx | `SoDManagementPage` (componente) | `SeparationRulesPage` |
| accessSlice.js | `validateSoD`, `sodConflicts`, `selectSoDConflicts` | `validateSeparation`, `separationConflicts`, `selectSeparationConflicts` |
| accessService.js | `validateSoD()` | `validateSeparation()` |

### Categoria 2 — Concepto `role` en datos de usuario (post-A-005)

| Archivo IACT-ui | Problema | Correccion |
|---|---|---|
| PropShapes.js | `role: PropTypes.oneOf(['admin', 'user'])` | eliminar campo `role` |
| mocks/auth.js, authMocks.js, mockInterceptor.js | `role: 'admin'` en mocks | eliminar campo `role` |
| UserManagement.jsx | columna `role` y badge `user.role === 'admin'` | usar `function_codes` o `access_groups` |

### Categoria 3 — Endpoint incorrecto

`accessService.js` llama a `/access/validate-sod` — endpoint
inexistente en backend. El correcto:
`GET /api/access/separation-rules/check/?function_a=X&function_b=Y`.

### Aceptable (NO se toca en IACT-ui)

Textos UI en prosa explicativa: **"Reglas de Separacion de
Deberes"**, **"Separation of Duties"** — terminos
regulatorios del dominio, NO identificadores de codigo.

## 4. Estado real del trabajo IACT-ui

> Cita literal del ejecutor:
>
> "El trabajo descrito no esta aplicado. Esos cambios
> pertenecen a una sesion futura o a otro contexto."

**Implicacion para IACT-docs:** la migracion en IACT-ui
es trabajo planificado pero no realizado. IACT-docs y
IACT-ui se alinearan independientemente; este WP cubre
solo IACT-docs use-case-view.

## 5. Mi opinion (Claude) — analisis y recomendacion

### Acuerdo total con la regla

La directiva del ejecutor es coherente con el principio
ya aplicado en WPs previos:

- WP `endpoint-sod-rules-rename`: renombro endpoint
  `/sod-rules/` → `/separation-rules/`.
- WP `std-010-compliance`: aplico vocabulario canonico
  STD-010 a use-case-view.
- WP `users-alignment`: no introdujo refs SOD nuevos.

**Pero ninguno de estos WPs tomo el paso de eliminar
"Sod" como vocabulario en captions plantuml y narrativa.**
La directiva actual cierra ese gap.

### Excepciones inmovibles

| Excepcion | Razon |
|---|---|
| Tokens opacos backend (`access:view_sod`, `access:update_sod`, `access:disable_sod`) | Contrato API; renombrarlos rompe integracion |
| "Separation of Duties" en prosa explicativa larga | Termino regulatorio formal — preservable como vocabulario de dominio |
| Codigos BD `SOD-001..003` | IDs persistidos en `SeparationRule.code`; renombrar requiere migracion BD |

### Tres archivos fuera de use-case-view con refs SOD

Detectados durante el audit ampliado:

1. `requisitos/reglas-negocio/rbac/sod.rst` — el archivo en
   si tiene `sod` en el nombre + contenido descriptivo de
   las 3 reglas SOD-NNN.
2. `requisitos/reglas-negocio/rbac/grupos-funciones.rst:375` —
   usa `SOD-002` (codigo BD, preservar).
3. `requisitos/casos-uso/admin/uc-adm-01/informacion-general.rst:32` —
   usa `SOD-001..003` (codigos BD, preservar).

**Decision:** estos 3 archivos quedan **out-of-scope** de
este WP. Razones:

- Los codigos BD son excepciones inmovibles (preservar).
- Renombrar `sod.rst` → `separacion-de-deberes.rst`
  requiere actualizar todas las cross-refs `:doc:` desde
  multiples modulos del corpus → WP separado.

### Scope final aprobado para este WP

**Solo `source/arquitectura-tecnica/use-case-view/`:**

| Cat | Tipo | Refs | Archivos |
|---|---|---|---|
| 1 | PlantUML aliases (`VALIDAR_SOD`, `SOD_RULE_*`) | 31 | 9 |
| 2 | Captions plantuml ("Validar SoD\n...") | 7 | 7 |
| 3 | Narrativa ("reglas SoD") | 16 | ~10 |
| 4 | Filenames con `-sod.rst` (2) + toctrees (2) + anchors (2) + cross-refs internos | 6 | 4 |
| **Total** | | **~60 ediciones** | **~12 archivos unicos** |

### Diferido a WP futuro

- TD-SOD-1: rename `requisitos/reglas-negocio/rbac/sod.rst`
  → `separacion-de-deberes.rst` + actualizar toctrees +
  cross-refs en multiples modulos.
- TD-SOD-2: verificar con backend si codigos `SOD-001..003`
  migran a `SR-NNN`. Si si, alinear docs en WP separado.

## 6. Decision sobre forma del rename

**`VALIDAR_SOD` → `VALIDAR_SEPARATION_RULES`** (alias plantuml).

Razones de la forma elegida:

- Alinea con backend post-A-001 (`SeparationRule` clase).
- Alinea con IACT-ui propuesto (`SEPARATION_RULES` constante).
- Alinea con endpoint canonico `/separation-rules/`.
- Auto-documentado: el alias = nombre de la entidad.

**`SOD_RULE_CREATED` → `SEPARATION_RULE_CREATED`** (eventos).

**Captions plantuml "Validar SoD\n(CNST-005)"** → "Validar
regla de separacion\n(CNST-005)".

**Narrativa "reglas SoD"** → "reglas de separacion" (forma
breve) o "reglas de Separacion de Deberes" (forma larga
explicativa).

## 7. Plan de tareas atomicas (next: Phase 8)

- T-001..T-009: Cat-1 PlantUML aliases (1 archivo = 1 commit).
- T-010..T-016: Cat-2 captions (mismo archivo si Cat-1 ya
  lo tocó, consolidar; si no, archivos independientes).
- T-017..T-026: Cat-3 narrativa.
- T-027..T-028: Cat-4 git mv filenames + actualizar toctrees +
  anchors.
- TR-01: cierre WP.

Algunos archivos aparecen en multiples categorias (e.g.,
`uc-acc-01-asignar-funciones.rst` tiene Cat-1 + Cat-2). Se
consolidaran en un solo commit por archivo.

## 8. Validacion final esperada

```bash
# CERO refs en use-case-view (excepto excepciones documentadas):
grep -rnE "SOD|SoD|sod" source/arquitectura-tecnica/use-case-view/

# Esperado: solo Cat-5 (cross-ref a archivo externo
# rbac/sod.rst) — preservada hasta WP futuro.
```

## Refs

- WP `endpoint-sod-rules-rename` (cerrado, mismo dominio).
- WP `std-010-compliance` (cerrado, dejo este gap).
- Backend A-001..A-005 (rename SodRule → SeparationRule).
- IACT-ui (repo separado, alineamiento futuro).
- STD-010 v1.0.0 (vocabulario abstracto).
