```yml
created_at: 2026-05-08 01:50:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — clean-code-naming audit

## [1.0.0] — 2026-05-08

### Added (8 artefactos de audit)

- `discover/by-category/c1-suffixes-prohibited.md` — 148
  clases con sufijos tecnicos prohibidos.
- `discover/by-category/c2-acronyms.md` — 1225 refs
  SOD/SoD/sod, 10 filenames con acronimo.
- `discover/by-category/c3-std010-vocabulary.md` — 629 refs
  con tecnologia concreta fuera de exempt.
- `discover/by-category/c4-filenames.md` — 11 archivos con
  violaciones de naming.
- `discover/by-category/c5-methods-variables.md` — 0
  violaciones reales tras analisis con contexto.
- `discover/audit-global.md` — reporte consolidado +
  hallazgo critico (conflicto `backend/conventions.rst`).
- `plan-execution/remediation-roadmap.md` — 8 WPs futuros
  priorizados, 3 sprints, 70-100 h estimadas.
- `wp-state.md` — definicion del WP audit-only.

### Findings

**Volumen total:** ~1100 ediciones distribuidas en ~150 archivos
unicos (subset de los 2866 archivos `.rst` del corpus).

**Hallazgo critico:** `source/backend/conventions.rst`
prescribe sufijos `Serializer`, `ViewSet`, `View`,
`Permission` que CLEAN_CODE_NAMING_PRINCIPLES §6.2 prohibe.
Resolver conflicto normativo es PRE-REQUISITO antes de
cualquier rename masivo de clases C1.

**Decisiones requeridas del ejecutor (4):**

1. ADR resolucion conflicto backend/conventions vs CLEAN_CODE.
2. Scope STD-010: ¿exempt `_metodologia-aplicacion/`,
   `index.rst`, sistemas externos del cliente?
3. Builder en dominio: `ResumenSaludBuilder` ¿viola §1.2?
4. RBAC en prosa: ¿excepcion implicita por vocabulario disciplinar?

### Excluded (audit only — no execute)

Este WP **NO ejecuta** correcciones. La remediacion se
fragmenta en 8 WPs futuros documentados en
`plan-execution/remediation-roadmap.md`.

### Excepciones legitimas confirmadas (preservar)

1. Tokens RBAC opacos (`access:*_sod`) — contrato API.
2. Codigos BD persistidos (`SOD-001..003`, `AGR-NNN`).
3. "Separation of Duties" / "RBAC" como vocabulario
   disciplinar en prosa larga.
4. Sistemas externos del cliente (MySQL del IVR como
   informacion factual).
5. Clases base de librerias externas (DjangoModelFactory,
   BasePermission, ModelBackend, APIView, etc.).

## Commits del WP

3 commits totales:

1. WP setup + 5 reportes by-category.
2. Reporte global + roadmap.
3. (este commit) — TR cierre.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES v1.0.0.
- STD-010 v1.0.0.
- 5 WPs precedentes parciales (cerrados).
