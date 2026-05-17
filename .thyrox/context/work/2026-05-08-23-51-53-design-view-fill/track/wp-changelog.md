```yml
created_at: 2026-05-08 23:55:00
project: IACT-docs
work_package: 2026-05-08-23-51-53-design-view-fill
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — design-view-fill

## [1.0.0] — 2026-05-08

### Resumen

Cierra H-CONTENT-1 del WP previo `dag-completion-loop`.
Completa los 4 modulos de design-view que tenian solo 2
archivos (bounded-context + interaction-pattern), agregando
el lifecycle/flow representativo de la entidad principal del
modulo.

### Added

- `design-view/users/user-lifecycle.rst` — FSM de ``User``
  (ACTIVE / INACTIVE / BLOCKED) con reglas de transicion y
  efectos colaterales sobre tokens JWT.
- `design-view/admin/menu-item-lifecycle.rst` — FSM de
  ``MenuItem`` (DRAFT / ACTIVE / DEPRECATED / ARCHIVED)
  alineada con UC_ADM_05.
- `design-view/audit/audit-event-lifecycle.rst` — FSM de
  ``AuditEvent`` (RECEIVED / PERSISTED / PURGED) con
  invariantes de hash chain.
- `design-view/logs/log-retention-flow.rst` — flujo de
  actividad de retencion/purga con politica configurable
  por nivel.

### Changed

- 4 toctree actualizados: `users/index.rst`,
  `admin/index.rst`, `audit/index.rst`, `logs/index.rst`.

### Fixed

- Cross-ref roto a `domain-model/system-log` (entidad no
  existe en el corpus). Repointed a `infrastructure-log.rst`
  (archivo real).

### Verification

- Build strict EXIT=0, 0 warnings.
- Criterio: 4 modulos con minimo 3 archivos — admin: 3,
  audit: 3, logs: 3, users: 3.

### Refs

- WP precedente: `dag-completion-loop` (H-CONTENT-1).
- WPs siguientes: WP-CONTENT-3, WP-CONTENT-2.
