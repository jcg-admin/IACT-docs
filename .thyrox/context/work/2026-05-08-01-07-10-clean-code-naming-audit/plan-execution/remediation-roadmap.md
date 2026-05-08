```yml
created_at: 2026-05-08 01:45:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 8 — PLAN EXECUTION (audit-only)
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Remediation Roadmap (8 WPs futuros)
```

# Roadmap de remediacion — 8 WPs futuros

> Este WP es **audit only**. No ejecuta correcciones.
> Este roadmap define los WPs futuros priorizados.

## DAG de dependencias

```
WP-A (filenames sod) ──┐
WP-B (sod en casos-uso) ─┼─> WP-C (sod en backend/dm/rbac) ──┐
WP-H (factory-reportefactory) ─┘                              │
                                                              v
WP-D (ADR backend/conventions vs CLEAN_CODE) ──> WP-E (Factory/Builder/Manager) ──> WP-F (Serializer/ViewSet/View)
                                                              │
                                                              v
WP-G (STD-010 fuera exempt) ─── (independiente, requiere clarificar scope)
```

## WP-A — Filenames con `sod` rename

**Scope:** 10 archivos + sus cross-refs.

**Tareas:**

- Rename de `br-007-separacion-funciones-sod.rst`
- Rename de `rbac/sod.rst`
- Rename de `act-sod-check.rst`
- Rename de `cnst-030-reglas-de-separacion-de-funciones-sod.rst`
- Rename de `fr-010-02-validar-sod-antes-asignar.rst`
- Rename de `raci-sod.rst`
- Rename de `evaluacion-conflicto-sod.rst`
- Rename de `diagrama-de-estados-sod-rule.rst` (uc-adm-01)
- Rename de `diagrama-de-sod-validation.rst` (uc-acc-01)
- Rename de `diagrama-de-estados-sodrule.rst` (uc-acc-05)

**Ediciones derivadas:** todos los `:doc:` que apuntan a
estos paths (~30-50 cross-refs estimados).

**Esfuerzo:** 5-7 h.

**Pre-req:** ninguno.

## WP-B — Refs SoD en `requisitos/casos-uso/` (637 refs)

**Scope:** ~50 archivos, ~600 ediciones.

**Categoria de refs:**

- Narrativa "reglas SoD" → "reglas de separacion".
- "Validar SoD" → "Validar separacion".
- "SoD" en captions plantuml → preservar concepto SoD si es
  vocabulario regulatorio en prosa larga, o expandir si es
  identificador.
- `SOD_RULE_*` eventos → `SEPARATION_RULE_*`.
- Codigos `SOD-001..003` → preservar (excepcion §8.3).

**Esfuerzo:** 10-15 h.

**Pre-req:** ninguno.

## WP-C — Refs SoD en backend/ + domain-model/ + reglas-negocio/

**Scope:** ~10-15 archivos, ~100-130 ediciones.

**Esfuerzo:** 4-6 h.

**Pre-req:** WP-A, WP-B (consistencia).

## WP-D — ADR conflicto `backend/conventions.rst` vs CLEAN_CODE

**Tipo:** decision documental (no rename masivo).

**Tareas:**

- Crear ADR (`adr-naming-suffixes-resolution.md`) en
  `.thyrox/context/decisions/`.
- Decision A/B/C (ver `audit-global.md` §2.3).
- Si Opcion A: actualizar `backend/conventions.rst` para
  alinear con CLEAN_CODE.
- Si Opcion B: actualizar `CLEAN_CODE_NAMING_PRINCIPLES`
  con excepcion documentada.
- Si Opcion C: registrar como TD en
  `.thyrox/context/technical-debt.md`.

**Esfuerzo:** 2-4 h.

**Pre-req:** ninguno (decision human-driven).

## WP-E — Rename clases Factory/Builder/Manager

**Scope:** 20 clases unicas (9 Factory + 7 Builder + 4 Manager).

**Tareas:**

- 9 `*Factory` → `*TestData` (tests) o nombre de rol.
- 7 `*Builder` → preservar si es rol de dominio
  (`ResumenSaludBuilder`) o renombrar.
- 4 `*Manager` → triage caso por caso.

**Pre-req:** WP-D (decision sobre Builder en dominio).

**Esfuerzo:** 6-10 h.

## WP-F — Rename clases Serializer/ViewSet/View/Permission/Backend

**Scope:** 27 + 7 + 81 + 8 + 5 = **128 clases**.

**Tareas:**

- 27 `*Serializer` → `*Representation`.
- 7 `*ViewSet` → `*Endpoint`.
- 81 `*View` → `*Endpoint`.
- 8 `*Permission` → triage (algunos son dominio).
- 5 `*Backend` → triage (algunos son DTOs legitimos).

**Pre-req:** WP-D (resolver conflicto normativo).

**Esfuerzo:** 30-40 h. (WP grande, posible split por
cluster).

## WP-G — Cleanup STD-010 fuera exempt

**Scope:** ~265 ediciones en ~57 archivos.

**Pre-req:** clarificar scope STD-010 (norma actualizada
o decision sobre `_metodologia-aplicacion/`,
`index.rst`, sistemas externos).

**Esfuerzo:** 11-16 h.

## WP-H — Rename `factory-reportefactory.rst`

**Scope:** 1 archivo + cross-refs.

**Esfuerzo:** 30 min.

**Pre-req:** ninguno.

## Orden de ejecucion sugerido

### Sprint 1 (low-risk, sin pre-reqs)

- WP-A (filenames sod) — 5-7 h
- WP-H (factory-reportefactory) — 30 min
- WP-D (ADR) — 2-4 h

**Total Sprint 1:** ~8-12 h.

### Sprint 2 (cleanup masivo SoD, con resolucion del ADR)

- WP-B (sod en casos-uso) — 10-15 h
- WP-C (sod en otros) — 4-6 h
- WP-E (Factory/Builder/Manager — pequeno) — 6-10 h

**Total Sprint 2:** ~20-31 h.

### Sprint 3 (cleanup STD-010 + clases tecnicas grandes)

- WP-G (STD-010) — 11-16 h
- WP-F (Serializer/ViewSet/View — grande) — 30-40 h

**Total Sprint 3:** ~41-56 h.

### Total acumulado

**~70-100 h en 3 sprints.**

## Recomendacion al ejecutor

1. **Empezar por WP-D (ADR)** porque desbloquea WP-E y WP-F.
2. **En paralelo, ejecutar WP-A + WP-H** (low-risk, sin pre-reqs).
3. Tras decision ADR, planear Sprint 2 segun prioridad de
   alineamiento backend/frontend.

## Refs

- audit-global.md (priorizacion).
- discover/by-category/* (detalles).
- WPs previos cerrados como precedentes parciales.
