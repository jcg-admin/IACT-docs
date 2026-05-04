```yml
created_at: 2026-05-04 19:39:00
updated_at: 2026-05-04 19:39:00
project: THYROX
work_package: 2026-05-04-19-36-59-duplicate-labels-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — duplicate-labels-fix (R-05)

## Added

- `discover/duplicate-labels-fix-analysis.md` — análisis de 33 instancias de
  duplicate label: 32 archivos con título duplicado en template, 1 label
  explícito colisionado en overview.rst.
- `logs/build-after-fix-*.txt` — log del build post-fix.

## Fixed

- **32 archivos** en `arquitectura-tecnica/*/diagramas/`: eliminadas lines
  19-21 (título duplicado + underline + blank) que causaban que autosectionlabel
  generara el mismo label dos veces en el mismo archivo.
- **1 archivo** `arquitectura-tecnica/domain-model/overview.rst`: label
  `.. _modelo-dominio-iact:` renombrado a `.. _overview-modelo-dominio-iact:`
  para eliminar colisión con el label canónico en `modelo-dominio-iact.rst`.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. Entrada sugerida bajo `### Fixed`:

```
- Corregir 33 instancias de duplicate label en 33 archivos RST (R-05):
  32 títulos duplicados en template de diagramas, 1 label explícito
  colisionado.
```
