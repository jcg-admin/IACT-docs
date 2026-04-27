```yml
created_at: 2026-04-27 04:20:01
updated_at: 2026-04-27 04:55:00
project: IACT-docs
work_package: 2026-04-27-04-20-01-repository-diagnostics
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Borrador
```

# WP Changelog — repository-diagnostics

> Registro de TODOS los cambios producidos durante el WP. Este documento
> reemplaza al CHANGELOG.md de raíz mientras el WP está en una rama feature.
> Cuando la rama haga merge a `main`, el contenido relevante se promueve al
> CHANGELOG.md global con el bump de versión correspondiente.

## Hallazgos atendidos

11 hallazgos de Phase 1 DISCOVER — todos con código aplicado en este WP.

## Added

- WP `repository-diagnostics` — diagnóstico inicial del repositorio con 11
  hallazgos (`discover/repository-diagnostics-analysis.md`).
- `ROADMAP.md` y `CHANGELOG.md` en raíz (F-07) — requeridos por CLAUDE.md.
- `scripts/setup.sh` — bootstrap del entorno (uv sync + activar hooks)
  (F-04 + F-09).
- `scripts/install-hooks.sh` — configura `core.hooksPath=.githooks` (F-03).
- `.claude/.claude-plugin/plugin.json` — manifest del plugin THYROX (F-11),
  cumple ADR-019 (FASE 31).
- `.claude-plugin/marketplace.json` — marketplace local, sin red, apunta
  a `./.claude` como fuente del plugin (F-11).
- `.claude/settings.json::extraKnownMarketplaces.thyrox-local` (source
  `directory`) + `enabledPlugins["thyrox@thyrox-local"]: true` para
  auto-cargar el plugin sin `--plugin-dir` (F-11).
- `.thyrox/context/work/2026-04-26-02-39-17-git-workflow-documentation/CLOSURE-NOTICE.md`
  (F-06).
- `.thyrox/context/work/2026-04-25-04-44-30-monitor-behavior-analysis/ARCHIVED.md`
  (F-06).

## Changed

- `pyproject.toml` `readme` apunta a `readme.rst` — antes referenciaba
  `README.md` inexistente (F-02).
- `git rm -r --cached build/` — 1126 archivos / 64 MB removidos del
  index. Files preservados en filesystem (F-01).
- `.gitignore` simplificado: regla `build/` única, eliminado comentario
  contradictorio (F-01).
- `.thyrox/context/now.md` — reseteado al WP activo, antes mezclaba estado
  de 3 WPs distintos (F-05).
- `.claude/rules/commit-conventions.md` — reescrito para estilo Tim Pope
  (subject imperativo + body con QUÉ y POR QUÉ).
- `.githooks/commit-msg` — nuevo validador (largo, mayúscula, no punto,
  imperativo heurístico).
- `.claude/CLAUDE.md` — Locked Decision #7 actualizada (Conventional →
  Tim Pope), version `3.7`.

## Removed

- Branches `claude/*` (workflow del harness) — el proyecto usa `feature/*`
  (F-08). `claude/repository-diagnostics-Gz5jw` borrado local + remote.
  `claude/review-project-config-V8Fg5` bloqueado por server (HTTP 403),
  pendiente borrado manual.
- Estilo Conventional Commits (`type(scope): description`) — reemplazado
  por Tim Pope. Historial previo conservado, regla aplica desde el commit
  de cambio en adelante.

## Aceptado / no fixeado

- F-10: WPs auto-referenciales — patrón meta de proceso, no fix de código.
- F-08 parcial: branch `claude/review-project-config-V8Fg5` requiere
  borrado manual desde la UI de GitHub (server bloqueó delete con 403).

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge `feature/repository-diagnostics → develop → main`.
Cuando ocurra, mover este contenido a `CHANGELOG.md` raíz bajo el
release apropiado con bump de versión SemVer.
