```yml
created_at: 2026-05-04 20:03:00
updated_at: 2026-05-04 20:03:00
project: THYROX
work_package: 2026-05-04-20-02-59-broken-refs-normativa
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — broken-refs-normativa (R-07)

## Added

- `discover/broken-refs-normativa-analysis.md` — análisis de 2 broken refs:
  paths de directorio sin sufijo `/index` en archivos de normativa/estandares.
- `logs/build-after-fix-2026-05-04T200310.txt` — log del build post-fix.

## Fixed

- **`normativa/estandares/metodologia-analisis-dominio-ucs.rst:33`** —
  `:doc:` ref corregida: `.../analisis-dominio` → `.../analisis-dominio/index`.

- **`normativa/estandares/metodologia-oop-para-ucs.rst:37`** —
  `:doc:` ref corregida: `.../orientacion-objetos` → `.../orientacion-objetos/index`.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. Entrada sugerida bajo `### Fixed`:

```
- Corregir 2 broken :doc: refs en normativa/estandares (R-07): rutas de
  directorio sin sufijo /index en metodologia-analisis-dominio-ucs.rst y
  metodologia-oop-para-ucs.rst.
```
