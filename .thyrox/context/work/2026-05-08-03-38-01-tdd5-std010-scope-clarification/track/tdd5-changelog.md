```yml
created_at: 2026-05-08 03:45:00
project: IACT-docs
work_package: 2026-05-08-03-38-01-tdd5-std010-scope-clarification
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — TD-D5 (STD-010 §2.5 scope clarification)

## [1.0.0] — 2026-05-08

### Changed

- `source/normativa/estandares/std-010-vocabulario-abstracto.rst`
  bump `1.1.0 → 1.2.0` (MINOR — amplia ámbito).

### Added

#### STD-010 §2.5 — Tres clausulas de exencion

- **§2.5.1 Identity files** — declaracion del stack del
  proyecto. Exenta `_metadata/meta-01-identidad-proyecto.rst`
  y `_metadata/meta-05-estructura-documental.rst` por
  circularidad semantica ("Backend: Django REST Framework"
  vs absurdo "Backend: el Framework de Aplicacion").
- **§2.5.2 Landing page arquitectonica** — clarifica que
  `source/index.rst` parrafos introductorios y bullet lists
  de stack tecnologico operan bajo el mismo criterio que
  identity files (paralelo a §2.2 que ya cubria toctree).
- **§2.5.3 Testing files** — exenta
  `casos-uso/**/testing.rst` por paralelo explicito con
  `implementacion-tecnica.rst` (§5.1). Ambos documentan
  infraestructura tecnica del proyecto.

#### Tabla §2.1 — dos filas adicionales

| Archivo | Aplica |
|---|---|
| `source/base-cognitiva/_metadata/**` | No — exenta (§2.5.1) |
| `source/requisitos/casos-uso/**/testing.rst` | No — exenta (§2.5.3) |

#### §8 Historial — entrada v1.2.0

Documenta el alcance MINOR del bump, las tres exenciones, las
21 referencias cubiertas, y la trazabilidad a WP-G como origen
del diferimiento.

### Verification

```bash
# Estructura del archivo verificada
$ grep -nE '^[0-9]\.|^2\.[0-9]' source/normativa/estandares/std-010-vocabulario-abstracto.rst
1. Propósito
2. Ámbito de Aplicación
2.1 Tabla de archivos
2.2 ``index.rst`` raíz — aplicación por contenido
2.3 ``_metodologia-aplicacion/`` — exenta
2.4 Nombres propios de sistemas externos — exentos
2.5 Archivos de identidad y técnicos análogos a §5.1   ← NUEVO
2.5.1 Identity files                                    ← NUEVO
2.5.2 Landing page arquitectónica                       ← NUEVO
2.5.3 Testing files                                     ← NUEVO
3. Tabla de Vocabulario Canónico
...

# Version bumped
$ grep ':version:' source/normativa/estandares/std-010-vocabulario-abstracto.rst
 :version: 1.2.0
```

### Refs cubiertas por TD-D5 (21 totales)

| Categoria | Archivo(s) | Refs cubiertas | Clausula |
|---|---|---|---|
| Identity | `_metadata/meta-01-identidad-proyecto.rst` | 9 | §2.5.1 |
| Identity | `_metadata/meta-05-estructura-documental.rst` | 3 | §2.5.1 |
| Landing | `source/index.rst` | 5 | §2.5.2 |
| Testing | `casos-uso/auth/uc-auth-01/testing.rst` | 2 | §2.5.3 |
| Testing | `casos-uso/auth/uc-auth-02/testing.rst` | 2 | §2.5.3 |
| **Total** | — | **21** | — |

### Refs NO cubiertas (transparencia)

WP-G reporto ~288 refs diferidas totales. TD-D5 cubre 21
(las tres categorias explicitamente especificadas por el
ejecutor). Las restantes ~230 refs viven en categorias NO
incluidas en la directiva literal:

| Categoria | Refs aprox |
|---|---|
| `normativa/procedimientos/**` | 155 |
| `normativa/gobernanza/adr-*` | 50 |
| `normativa/estandares/plantillas/**` | 19 |
| `gestion/evidencia/arquitectura-modular/**` | 6 |
| **Subtotal pendiente** | **230** |

Estos archivos generan los mismos falsos positivos
(p. ej. un ADR backend que documenta "Redis prohibido"
necesita decir "Redis"; un procedimiento DevOps necesita
nombrar herramientas CI/CD), pero su exencion requiere
decision separada del ejecutor.

## Commits del WP

1. (este commit) — Open + apply + close TD-D5

## Roadmap status final

| WP | Estado |
|---|---|
| WP-A | ✅ Sprint 1 |
| WP-B | ✅ Sprint 2 |
| WP-C | ✅ Sprint 2 |
| WP-D | ✅ naming-rules-resolution |
| WP-E | ✅ Factory/Builder/Manager |
| WP-F | ✅ Serializer/ViewSet/View/Permission |
| WP-G | ✅ STD-010 cleanup vocabulario |
| WP-H | ✅ Sprint 1 |
| TD-D5 | ✅ **este WP** — STD-010 §2.5 clarificacion |

**Roadmap CLEAN_CODE remediation completo.** Sin deuda tecnica
activa pendiente de las directivas explicitas del ejecutor.

## Refs

- WP-G `2026-05-08-03-08-21-wpg-std010-cleanup` (origen del
  diferimiento documentado en `track/wpg-changelog.md`).
- STD-010 v1.2.0 §2.5 (artefacto creado por este WP).
- STD-010 v1.1.0 §2.1, §2.2, §2.3, §2.4, §5.1 (precedentes
  conceptuales para las tres clausulas).
