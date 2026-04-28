```yml
created_at: 2026-04-28 03:35:00
updated_at: 2026-04-28 03:35:00
project: IACT-docs
work_package: 2026-04-28-01-58-08-source-rebuild-strategy
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: En curso
```

# WP Changelog — source-rebuild-strategy

Registro de todos los cambios y eventos del WP. Formato Keep a Changelog.

---

## [Unreleased]

### Fixed

- `.gitignore`: resuelto conflicto de merge sin resolver. Combinó
  excludes de `tools/` (HEAD) y `temp-holding/**/transcripts`,
  `temp-holding/**/mnt` (otra rama). Descartó duplicado de `build/`.
  (F-NEW-1, commit `1cfda4b`).

### Changed

- `discover/source-rebuild-strategy-analysis.md` bumpeado a v2.0.0.
  Razón MAJOR: cambio de premisa en D4 (eliminada la "tensión" entre
  IDs semánticos y STD_007 — STD_007 los codifica, no los prohíbe) y
  en D5 (de "lift-and-shift vs refactor" a "backup as reference").
  (commit `6ef3ee4`).
- `wp-state.md`: status `Bloqueado` → `Aprobado`. Phase 1 DISCOVER
  cerrada. Listo para Phase 5/6.
  (commit `6ef3ee4`).

### Added

- 10 decisiones consolidadas en discover doc: D1, D2, D3 confirmadas
  + D4, D5 resueltas + F-04, F-05 resueltas + F-NEW-1/2/3 nuevas +
  CLEANUP final.
- Sección 11 ("Criterio editorial — quién decide"): clasificación
  inicial la propone Claude, ejecutor confirma.
- Sección 12 ("Estado del WP"): salida atómica explícita.

### Investigation (no code change yet)

- **Sphinx instalado fuera del flujo oficial** (2026-04-28 03:18):
  `pip3 install Sphinx==8.2.3 Furo myst-parser sphinxcontrib-plantuml`
  en system Python. **Esto NO es la instalación correcta del
  proyecto** — es solo binario `sphinx-build` disponible para
  verificaciones puntuales. (F-NEW-3).
- **F-NEW-4 — pyproject.toml roto:** investigación de opciones de fix.
  - Opción B descartada (2026-04-28 03:35): la última versión
    disponible de `sphinx-toolbox` en PyPI es **4.1.2**, la misma
    que ya está pinneada. Su metadata declara
    `Requires-Dist: sphinx-tabs<3.4.7,>=1.2.1`. No existe versión
    de sphinx-toolbox compatible con sphinx-tabs 3.5.0.
  - Opciones viables restantes: A (restaurar a versiones de
    `uv.lock`: sphinx-tabs 3.4.5 + sphinx-toolbox 4.1.0) o C
    (bajar sphinx-tabs a 3.4.6, mantener toolbox 4.1.2).
  - **Pendiente decisión del ejecutor.**

## Aceptado / no fixeado

- `temp-holding/` con filenames con espacios y tildes — material de
  referencia, no se renombra. Aceptado tal cual.

## Status de promoción a CHANGELOG.md raíz

Pendiente. Este WP no genera bump de versión todavía — Phase 1
DISCOVER no afecta el contrato público. Los cambios visibles para
usuarios (rebuild de source/) ocurrirán en WPs posteriores.
