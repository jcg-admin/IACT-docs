```yml
project: IACT-docs
work_package: 2026-05-06-00-40-54-long-running-commands-guideline
created_at: 2026-05-06 00:40:54
closed_at: 2026-05-06 00:42:00
current_phase: Phase 11 — TRACK/EVALUATE
status: Cerrado
size: micro (DISCOVER → EXECUTE → TRACK directo)
predecessor_wp: 2026-05-06-00-31-12-api-socket-error-investigation
target: Propagar las reglas R-1..R-5 y los anti-patterns AP-1..AP-3 documentados en track/recommendations.md del WP api-socket-error-investigation a `.claude/rules/long-running-commands.md` para que apliquen como guideline global del harness, no solo a IACT-docs.
author: NestorMonroy
flow: rm
methodology_step: rm-management
deliverable: .claude/rules/long-running-commands.md
```

# WP — Long-running Commands Guideline

## Trigger

WP `api-socket-error-investigation` registro como successor:

> long-running-commands-guideline — propagar R-1..R-5 a
> `.claude/rules/` como guideline global del harness.

## Alcance

Crear `.claude/rules/long-running-commands.md` con:

- Regla operacional R-1..R-5 (de track/recommendations.md WP previo).
- Anti-patterns AP-1..AP-3 (idem) + AP-4 (`tail -f` sin filtro)
  + AP-5 (grep sin `--line-buffered`) extraidos de
  cli_sse_liveness_timeout root-cause analysis.
- Tabla de decision por duracion estimada.
- Referencia al WP de origen para trazabilidad.

## Out of scope

- Modificar `.thyrox/guidelines/` (los guidelines son tech-stack
  specific, esta regla es operacional cross-tech).
- Modificar el cliente Claude Code (no es nuestro repo).

## Verificacion

`.claude/rules/` cargan automaticamente en cada sesion (per
I-009 invariant en `thyrox-invariants.md`). Una vez commiteada,
la regla aplica de inmediato.

## Closure

WP de tamaño micro. No se requiere Phase 3-9. Phase 10 EXECUTE =
crear el archivo. Phase 11 TRACK = este wp-state como ack +
changelog minimo.

## Refs

- Origen de las reglas: `2026-05-06-00-31-12-api-socket-error-investigation/track/recommendations.md`.
- Causa raiz documentada: `2026-05-06-00-31-12-api-socket-error-investigation/analyze/socket-error-root-cause.md`.
- Invariante I-009 (rules cargan siempre): `.claude/rules/thyrox-invariants.md`.
