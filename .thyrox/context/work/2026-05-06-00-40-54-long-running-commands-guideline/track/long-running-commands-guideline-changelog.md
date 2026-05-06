```yml
created_at: 2026-05-06 00:42:00
project: IACT-docs
work_package: 2026-05-06-00-40-54-long-running-commands-guideline
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — Long-running Commands Guideline

WP de tamaño micro. Sin Phase 3-9. Implementacion directa.

## Added

- `.claude/rules/long-running-commands.md` — guideline global
  con R-1..R-5 reglas operacionales + AP-1..AP-5 anti-patterns +
  tabla de decision por duracion estimada + referencias al WP de
  origen.

## Changed / Fixed / Removed

- N/A.

## Verified

- El archivo cumple convencion de naming `.claude/rules/<nombre>.md`.
- Frontmatter `yml` con `type: Convencion de Proyecto`,
  `version: 1.0.0`, `applies_to: IACT-docs v1.0.0+`,
  `origin_wp` campo agregado para trazabilidad.
- Cargado automaticamente en sesiones futuras por I-009 invariant.

## Status de promocion a CHANGELOG.md raiz

No aplica — es una regla operacional del agente, no un cambio en
el codigo o docs publicados del proyecto.

## Refs

- Origen: `2026-05-06-00-31-12-api-socket-error-investigation/track/recommendations.md`.
- Evidencia: `/tmp/claude-code-2683623323.diag.log` (cli_sse_liveness_timeout).
- Invariante: `.claude/rules/thyrox-invariants.md` I-009 (rules
  cargan siempre).
