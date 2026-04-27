# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/) y SemVer 2.0.0.

## [Unreleased]

### Added
- ROADMAP.md y CHANGELOG.md en raíz (F-07).
- `scripts/setup.sh` — bootstrap del entorno de desarrollo (uv sync + hooks).
- `scripts/install-hooks.sh` — activación de `.githooks/` via `core.hooksPath` (F-03).
- `.claude/.claude-plugin/plugin.json` — manifest del plugin THYROX (F-11) — registra el namespace `/thyrox:*` documentado en ADR-019 pero no implementado hasta ahora.
- `.claude-plugin/marketplace.json` — marketplace local (no público, sin red) que apunta a `./.claude/` como fuente del plugin thyrox.
- `.claude/settings.json` — `extraKnownMarketplaces.thyrox-local` (source `directory`) + `enabledPlugins["thyrox@thyrox-local"]: true` para auto-cargar el plugin sin `--plugin-dir` ni red.
- WP `repository-diagnostics` — diagnóstico inicial del repositorio con 11 hallazgos.

### Changed
- `pyproject.toml` `readme` apunta a `readme.rst` (F-02 — antes referenciaba `README.md` inexistente).
- Untrack de `build/` (F-01) — ~1126 archivos / 64 MB removidos del index.
- `.gitignore` simplificado: `build/` activo, eliminado comentario contradictorio.
- `.thyrox/context/now.md` — reseteado al WP activo (F-05 — antes mezclaba 3 WPs).

### Removed
- Branches `claude/*` (workflow del harness) — el proyecto usa `feature/*` (F-08).
- Estilo de commits Conventional (`type(scope): description`) — reemplazado por Tim Pope (subject imperativo + body explicando QUÉ y POR QUÉ). Historial previo conservado, regla aplica desde el commit de cambio en adelante.

## [1.0.0] — 2026-04-22

Versión inicial declarada en `pyproject.toml`. Corresponde a la finalización de
ÉPICA 1 (`phase1-discover-iact-docs`). Sin tag git asociado en el momento.
