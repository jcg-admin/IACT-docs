```yml
created_at: 2026-05-04 19:30:00
updated_at: 2026-05-04 19:30:00
project: THYROX
work_package: 2026-05-04-19-05-53-title-overlines-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — title-overlines-fix (R-04)

## Added

- `discover/title-overlines-fix-analysis.md` — inventario de 31 instancias
  únicas de title underline/overline too short identificadas en clean build.
- `logs/build-clean-2026-05-04T190553.txt` — log del build limpio pre-fix
  (52 warnings de título).
- `logs/build-after-fix-*.txt` — log del build post-fix (esperado 0 warnings).

## Fixed

- 31 instancias de `Title underline too short` / `Title overline too short`
  en 23 archivos RST:
  - 7 overline+underline pairs en `arquitectura-tecnica/` y
    `base-cognitiva/_uml/` y `requisitos/reglas-negocio/rbac/`
  - 24 underlines en `databases/`, `requisitos/casos-uso/` y
    `requisitos/reglas-negocio/`
  - Corregidos todos con script Python que calcula `len(titulo)` y
    reescribe el decorador con el carácter correcto.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. Entrada sugerida bajo `### Fixed`:

```
- Corregir 31 instancias de title underline/overline demasiado cortos
  en 23 archivos RST (R-04).
```
