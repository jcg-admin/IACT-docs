```yml
created_at: 2026-05-06 00:50:00
project: IACT-docs
work_package: 2026-05-06-00-31-12-api-socket-error-investigation
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — API Socket Error Investigation

WP de investigación. Causa raíz identificada con evidencia textual
de logs del cliente Claude Code. Phase 3 ANALYZE completa con dos
hipótesis confirmadas (H-1 + H-2), tres descartadas o no
concluyentes (H-3, H-4, H-5).

## Hallazgo principal

**El error visible "API Error: The socket connection was closed
unexpectedly" es la presentación user-facing de un evento interno
`cli_sse_liveness_timeout` del transporte SSE.**

Causa: el cliente Claude Code mantiene una conexión SSE con el
backend, con liveness timeout de ~5 min. Cuando un `tool_exec`
foreground (sphinx-build) toma más que ese período sin producir
mensajes desde el servidor, el stream cae.

## Evidencia decisiva

`/tmp/claude-code-2683623323.diag.log`:

```
19:31:19  cli_sse_message_received     ← último mensaje
19:36:22  cli_sse_liveness_timeout     ← +5 min 03 s
19:36:22  cli_sse_reconnect_attempt    ← reconexión automática
```

Patrón replicado 5 veces durante la sesión.

## Added

- `wp-state.md` — Phase 1 DISCOVER con 5 hipótesis y plan.
- `analyze/socket-error-root-cause.md` — Phase 3 ANALYZE con
  evidencia textual, validación de hipótesis, mecanismo de fallo.
- `track/recommendations.md` — R-1..R-5 reglas operacionales +
  3 anti-patterns documentados.
- Este changelog.

## Changed / Fixed / Removed

- N/A — WP diagnostic-only sin cambios al código o docs.

## Aceptado / no fixeado

- **No modificar el cliente Claude Code**: out of scope (NA-1).
- **No reportar bug upstream**: el comportamiento es correcto
  desde la perspectiva del transporte SSE; la responsabilidad de
  mantener viva la conexión es del agente (NA-2).
- **No documentar como guideline global ahora**: la propagación
  de R-1..R-5 a `.claude/rules/` queda como WP sucesor
  (`long-running-commands-guideline`).

## Verified

- Logs de cliente Claude Code accesibles en `/tmp/claude-code-*.diag.log`.
- Timeline reconstruido con timestamps de 5 sesiones.
- 3 reconexiones del cliente registradas en `environment-manager.out`
  (23:06, 23:20, 00:28 UTC).
- Mecanismo de fallo SSE confirmado por evento literal
  `cli_sse_liveness_timeout`.

## Status de promoción a CHANGELOG.md raíz

No aplica — WP de investigación sin cambios productivos.

## WPs sucesores derivados

1. `plantuml-cache-prerender-update` — atacar la causa de fondo
   (builds lentos por cache stale). Ya registrado en WP3.
2. `long-running-commands-guideline` — propagar reglas R-1..R-5
   a `.claude/rules/` como guideline global del harness.

## Refs

- WP donde ocurrió el error: `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass`.
- WP relacionado (causa de fondo): `2026-05-06-00-11-02-plantuml-cached-effectiveness-audit`.
- Logs evidencia:
  - `/tmp/claude-code-2683623323.diag.log` (sesión 19:08).
  - `/tmp/claude-code-1717198703.diag.log` (sesión 23:20).
  - `/tmp/environment-manager.out` (3 resumes registrados).
- Documento técnico: `analyze/socket-error-root-cause.md`.
- Recomendaciones operacionales: `track/recommendations.md`.
