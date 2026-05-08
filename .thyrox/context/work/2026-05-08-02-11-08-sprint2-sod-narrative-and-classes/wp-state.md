```yml
project: IACT-docs
work_package: 2026-05-08-02-11-08-sprint2-sod-narrative-and-classes
created_at: 2026-05-08 02:11:08
closed_at: 2026-05-08 03:05:00
current_phase: Phase 11 — TRACK
status: Cerrado (WP-B + WP-C completos; WP-E diferido)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: grande (~800 refs en ~50+ archivos, ~2-3 sub-sesiones)
target: Sprint 2 del roadmap clean-code-naming. Combina WP-B (refs SoD en casos-uso) + WP-C (refs en backend/dm/normativa/base-cognitiva/metodologia/gestion/requisitos-funcionales). **WP-E (Factory/Builder/Manager) se difiere a WP separado** por volumen + necesidad de verificacion caso-por-caso del rol de cada clase.
predecessor_wp: 2026-05-08-01-41-12-sprint1-filenames-and-factory (cerrado)
trigger: directiva del ejecutor "continuamos con Sprint 2"
```

# WP — Sprint 2 (narrativa SoD + identificadores en casos-uso/backend/dm)

## Trigger

Sprint 1 cerrado. Ejecutor autorizo Sprint 2.

## Re-audit del estado actual

| Subdirectorio | Refs |
|---|---|
| `requisitos/casos-uso/` | **629** |
| `base-cognitiva/` | 119 |
| `normativa/` | 83 |
| `gestion/` | 62 |
| `requisitos/reglas-negocio/` | 56 |
| `backend/` | 44 |
| `requisitos/requisitos-funcionales/` | 41 |
| `requisitos/_metodologia-aplicacion/` | 28 |
| `arquitectura-tecnica/domain-model/` | 27 |
| `arquitectura-tecnica/use-case-view/` | 1 (excepcion documentada) |
| `requisitos/business-requirements/` | 2 |
| **Total** | **~1092** |

Por tipo de patron:

- `VALIDAR_SOD` aliases plantuml: **20** (en casos-uso/permissions, casos-uso/admin, casos-uso/access)
- `SOD_RULE_*` event identifiers: **56** (eventos audit)
- `SOD-001/002/003` BD codes: **57** (PRESERVAR — excepcion §8.3)
- "reglas SoD": 86, "Validar SoD": 22, "SoD" aislado: 736, "SOD" aislado: 61

## Estrategia de transformacion

### Patrones automatizables (sed)

Categoria 1 — **Identificadores tecnicos** (deben renombrarse):

| Patron | Reemplazo |
|---|---|
| `VALIDAR_SOD` (plantuml alias) | `VALIDAR_SEPARATION_RULES` |
| `SOD_RULE_CREATED` | `SEPARATION_RULE_CREATED` |
| `SOD_RULE_UPDATED` | `SEPARATION_RULE_UPDATED` |
| `SOD_RULE_DISABLED` | `SEPARATION_RULE_DISABLED` |
| `SOD_RULE_DELETED` | `SEPARATION_RULE_DELETED` |
| `SOD_RULE_ENABLED` | `SEPARATION_RULE_ENABLED` |
| `SOD_RULE_*` (en captions/notas) | `SEPARATION_RULE_*` |
| `SoDRule` (Java/Python class) | `SeparationRule` |
| `SoDRuleRepo` | `SeparationRuleRepo` |
| `SoDRuleService` | `SeparationRuleService` |
| `SoDRuleCache` | `SeparationRuleCache` |
| `SoDRuleViewSet` | `SeparationRuleEndpoint` (rename + WP-F) |
| `SoDRuleSerializer` | `SeparationRuleRepresentation` (rename + WP-F) |
| `SoDViolation` | `SeparationRuleViolation` |
| `SoDValidator` | `SeparationRuleValidator` |
| `validate_sod` | `validate_separation` |
| `validar_sod` | `validar_separacion` |

Categoria 2 — **Narrativa** (texto explicativo):

| Patron | Reemplazo |
|---|---|
| `reglas SoD` | `reglas de separacion` |
| `Reglas SoD` | `Reglas de Separacion` |
| `regla SoD` | `regla de separacion` |
| `Validar SoD` | `Validar separacion` |
| `validar SoD` | `validar separacion` |
| `SoD write-time` | `separacion write-time` |
| `SoD compliance` | `compliance de separacion` |
| `SoDCompliance` | `SeparationCompliance` |
| `compliance SoD` | `compliance de separacion` |

### Patrones a PRESERVAR

- `SOD-001`, `SOD-002`, `SOD-003`, `SOD-NNN` — codigos BD (excepcion §8.3).
- `access:view_sod`, `access:update_sod`, `access:disable_sod` — tokens opacos.
- "Separation of Duties" — termino regulatorio en prosa larga.
- "SoD" aislado en prosa larga regulatoria SI hace falta — pero por directiva
  del ejecutor "no queremos nada que diga Sod, porque puede confundir",
  expandir cuando sea posible.

### Casos especiales

- `factory-method-reportes.rst` (renombrado en WP-H) tiene
  `SeparationComplianceReport` ya migrado.
- `use-case-view/admin/uc-adm-01-...-de-separacion.rst` tiene una
  ref a SOD-001..003 (codigo BD, preservar).
- `mapa-funciones-rbac.rst` ya solo tiene cross-ref a archivo externo
  (out-of-scope tras WP-A).

## Approach de ejecucion

Por **subdirectorio**, en orden de volumen ascendente para
ir validando el patron antes de aplicar a casos masivos:

1. `business-requirements/` (2 refs) — sandbox de validacion.
2. `requisitos-funcionales/` (41).
3. `domain-model/` (27).
4. `backend/` (44).
5. `_metodologia-aplicacion/` (28).
6. `reglas-negocio/` (56).
7. `gestion/` (62).
8. `normativa/` (83).
9. `base-cognitiva/` (119).
10. `casos-uso/` (629) — el bloque mayor.

Cada commit por subdirectorio (10 commits aprox), con
verificacion de patron antes de aplicar.

## WP-E (Factory/Builder/Manager) — DIFERIDO

El roadmap original incluia WP-E en Sprint 2. Se difiere
porque:

- 20 clases (Factory + Builder + Manager) requieren
  verificacion caso-por-caso del rol real (criterio de D3:
  "verificar codigo antes de commitear el rename").
- Sprint 2 ya alcanza ~1100 refs solo en SoD; sumar 20
  renames de clase + sus refs derivadas exede capacidad
  practica de un solo WP.

Se abrira WP separado tras cierre de este.

## Stopping points

- **SP-01:** validar patron sed en sandbox antes de masivo.
- **SP-02:** revisar antes de cierre.

## Refs

- WPs previos cerrados (8).
- CLEAN_CODE_NAMING_PRINCIPLES §1.4, §6.2, §8.2.
- STD-010 v1.1.0 §5.4, §5.5 (excepciones formales).
- backend/conventions.rst v2.0.0.
