```yml
created_at: 2026-04-28 04:05:00
updated_at: 2026-04-28 04:05:00
project: IACT-docs
work_package: 2026-04-28-03-59-01-bootstrap-hardening
phase: Phase 1 — DISCOVER (con implementación adelantada por instrucción ejecutor)
author: NestorMonroy
status: Implementación parcial completa
```

# WP Changelog — bootstrap-hardening

Registro de todos los cambios y eventos del WP. Formato Keep a Changelog.

---

## [Unreleased]

### Added

- `Makefile`: target `check-bootstrap` (PHONY). Verifica
  `tools/plantuml.jar` y `.venv/bin/sphinx-build` (o el equivalente
  Windows). Aborta con mensaje accionable en color rojo si falta
  algo: *"ejecutá primero: `bash scripts/setup.sh`"*.
- `Makefile`: target `html` ahora tiene dependencia `check-bootstrap`
  — falla rápido si bootstrap incompleto, en vez de generar 183
  warnings fantasma. (F-02 resuelto vía implementación adelantada).

### Fixed

- `Makefile`: bug pre-existente en selección de `SPHINXBUILD` y
  `SPHINXAUTOBUILD`. La lógica solo verificaba paths de Windows
  (`.venv/Scripts/sphinx-build.exe`), no los de Linux/Mac
  (`.venv/bin/sphinx-build`). Resultado: en Linux/Mac, `make html`
  caía silenciosamente al `sphinx-build` global del sistema en vez
  de usar el del venv. Esto explicaba el `ExtensionError` con
  `sphinx_design` faltante: el sphinx del sistema no tenía las
  extensions del venv. Cambio: priorizar Linux/Mac primero, después
  Windows, después fallback global.

### Verified

- **CI bootstrap end-to-end YA EXISTE.** Verificado en
  `.github/workflows/validate.yml`:
  - Setup Python 3.11 + uv
  - Install system deps (libenchant + Java)
  - Run `bash scripts/setup.sh` (línea 32)
  - Run `make clean` + `sphinx-build -W` (warnings as errors)
  - Validate PlantUML
  - Trigger: PR a develop/main + push a feature/**
  Conclusión: la sub-acción "CI" de F-NEW-7 ya estaba cubierta. El
  discover doc inicial decía "no conocido — pendiente verificar".
  Esto fue una falla mía de discovery; lo corrijo aquí.

### Verification end-to-end

- `make clean && make html` → `build succeeded.` (0 warnings, exit 0).
  Verificado 2026-04-28 04:05 con bootstrap completo.
- `make check-bootstrap` con bootstrap completo → exit 0.
- `make check-bootstrap` con plantuml.jar movido fuera → exit 1
  con mensaje "ejecutá primero: bash scripts/setup.sh" en rojo.

## Pendiente (no implementado en esta tanda)

Por priorización del ejecutor, se implementaron solo Makefile guard
+ verificación de CI. Quedan pendientes (van a Phase 5/6 de este WP
si se decide continuarlo):

- D1: ¿`CONTRIBUTING.md` separado o sección en `readme.rst`?
- D4: Soft-disable de spellcheck si enchant no está
- F-05: Pre-push hook con warning de bootstrap

## Status de promoción a CHANGELOG.md raíz

Pendiente. Cambios al Makefile son developer-facing — relevantes
para incluir en próximo bump de versión bajo categoría "Developer
Experience".
