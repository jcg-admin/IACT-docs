```yml
type: Estado de Sesión
version: 3.2
updated_at: 2026-04-28 05:54:05
cold_boot: false
current_epic: 5
epic_name: source-rebuild-strategy
current_work: .thyrox/context/work/2026-04-28-05-28-42-source-rebuild-normativa-procedimientos
stage: ÉPICA 8 CERRADA
stage_number: 11
current_phase: Phase 11 — TRACK (CERRADO 2026-04-28 05:35)
flow: thyrox
methodology_step: cerrado
blockers: []
last_completed_phase: Phase 10 — EXECUTE (33/33 tareas completas, 16 hijos spawneados)
next_decision_required: "Decidir qué WP-hijo abrir primero (recomendado: source-rebuild-base-cognitiva)"
stage_sync_required: true
```

# IACT-docs — Source Rebuild Strategy

**WP activo:** `2026-04-28-01-58-08-source-rebuild-strategy`
**Branch:** `feature/solve-problem-docs`
**Phase 1 DISCOVER:** completa — D1-D5 + F-04/F-05 + F-NEW-1..7 resueltos.
**Phase 5 STRATEGY:** aprobada (v2.0) — 10 Key Ideas, 14 Decisions, 3 análisis de soporte.
**Phase 6 PLAN:** en curso.

## Strategy v2.0 — resumen

- 3 dimensiones: methodology + spec/tech + lifecycle.
- 16 WPs granular en orden secuencial.
- 8 cajones técnicos nuevos (backend, frontend, infrastructure, databases, operations, onboarding, quality, risks-technical-debt).
- source/ y .thyrox/ son worlds separados.
- Re-autoría con v1.0.0 fresh (no migración).
- Skeleton-first para tech cajones.

## WPs relacionados

- `bootstrap-hardening` (2026-04-28-03-59-01) — paralelo, recibió F-NEW-8 (tech-skill fix backend-nodejs → backend-django) pendiente.

## Próximo paso

Phase 6 PLAN del WP source-rebuild-strategy:
- Definir in/out scope detallado del WP-padre.
- Listar los 16 WPs hijos como spinoff.
- Actualizar ROADMAP.md si existe.
- Producir `plan/source-rebuild-strategy-plan.md`.
