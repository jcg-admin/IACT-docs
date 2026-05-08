```yml
created_at: 2026-05-08 04:00:00
project: IACT-docs
work_package: 2026-05-08-03-56-35-tdd6-std010-scope-extension
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — TD-D6 (STD-010 §2.5.4-§2.5.7 scope extension)

## [1.0.0] — 2026-05-08

### Changed

- `source/normativa/estandares/std-010-vocabulario-abstracto.rst`
  bump `1.2.0 → 1.3.0` (MINOR — extiende ámbito).

### Added

#### STD-010 §2.5.4 — Procedimientos operativos

Exenta `source/normativa/procedimientos/**` por su naturaleza de
**instrucciones ejecutables**. Documentos como
`proc-devops-001-devops-automation.rst` requieren nombrar
herramientas concretas (`pytest`, `docker`, `runs-on:
ubuntu-latest`) para ser ejecutables.

#### STD-010 §2.5.5 — ADRs (Architecture Decision Records)

Exenta `source/normativa/gobernanza/adr-*.rst` y
`source/arquitectura-tecnica/modulos/*/decisiones/adr-*.rst`.
Los ADRs registran **decisiones tecnológicas con trade-offs**:
nombrar la tecnología elegida y la descartada es el propósito
del documento.

#### STD-010 §2.5.6 — Plantillas técnicas

Exenta `source/normativa/estandares/plantillas/**`. Las
plantillas con ejemplos concretos (Stack: Django REST
Framework, Cache Redis, etc.) pierden valor pedagógico si los
ejemplos se abstraen.

#### STD-010 §2.5.7 — Análisis de arquitectura modular

Exenta `source/gestion/evidencia/arquitectura-modular/**` —
evidencia de análisis arquitectónico real del sistema con
mismo carácter que identity files (§2.5.1) pero a granularidad
de módulo.

#### Tabla §2.1 — cuatro filas adicionales

| Archivo | Aplica |
|---|---|
| `source/normativa/procedimientos/**` | No — exenta (§2.5.4) |
| `source/normativa/gobernanza/adr-*` | No — exenta (§2.5.5) |
| `source/normativa/estandares/plantillas/**` | No — exenta (§2.5.6) |
| `source/gestion/evidencia/arquitectura-modular/**` | No — exenta (§2.5.7) |

#### §8 Historial — entrada v1.3.0

Documenta el alcance MINOR del bump, las cuatro exenciones, las
230 referencias cubiertas, y el cierre del roadmap CLEAN_CODE
remediation sin deuda activa pendiente.

### Verification

```bash
$ grep -nE '^2\.5\.[0-9]' source/normativa/estandares/std-010-vocabulario-abstracto.rst
2.5.1 Identity files — declaración del stack del proyecto
2.5.2 Landing page arquitectónica — ``source/index.rst``
2.5.3 Testing files — paralelo de §5.1
2.5.4 Procedimientos operativos — instrucciones ejecutables   ← NUEVO
2.5.5 ADRs (Architecture Decision Records)                     ← NUEVO
2.5.6 Plantillas técnicas con ejemplos concretos               ← NUEVO
2.5.7 Análisis de arquitectura modular                         ← NUEVO

$ grep ':version:' source/normativa/estandares/std-010-vocabulario-abstracto.rst
 :version: 1.3.0
```

### Refs cubiertas por TD-D6 (230 totales)

| Categoria | Refs | Clausula |
|---|---|---|
| `normativa/procedimientos/**` | 127 | §2.5.4 |
| `normativa/gobernanza/adr-*` | 46 | §2.5.5 |
| `normativa/estandares/plantillas/**` | 51 | §2.5.6 |
| `gestion/evidencia/arquitectura-modular/**` | 6 | §2.5.7 |
| **Total** | **230** | — |

### Estado final del scope STD-010

Tras TD-D5 + TD-D6, las cláusulas §2.5 cubren las 251 refs
identificadas como falsos positivos en WP-G:

| Origen | Refs | Cubierto por |
|---|---|---|
| Identity files | 12 | §2.5.1 (TD-D5) |
| Landing arquitectónica | 5 | §2.5.2 (TD-D5) |
| Testing files | 4 | §2.5.3 (TD-D5) |
| Procedimientos | 127 | §2.5.4 (TD-D6) |
| ADRs gobernanza | 46 | §2.5.5 (TD-D6) |
| Plantillas | 51 | §2.5.6 (TD-D6) |
| Arquitectura modular | 6 | §2.5.7 (TD-D6) |
| **Total** | **251** | 7 cláusulas |

## Commits del WP

1. (este commit) — Open + apply + close TD-D6

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
| TD-D5 | ✅ STD-010 §2.5 (3 exenciones) |
| TD-D6 | ✅ **este WP** — STD-010 §2.5 (4 exenciones adicionales) |

**Roadmap CLEAN_CODE remediation completamente cerrado.**
Sin deuda técnica activa pendiente. Todas las refs deferred
identificadas en WP-G están cubiertas normativamente.

## Refs

- TD-D5 `2026-05-08-03-38-01-tdd5-std010-scope-clarification`
  (mecanismo §2.5 establecido).
- WP-G `2026-05-08-03-08-21-wpg-std010-cleanup` (origen del
  diferimiento).
- STD-010 v1.3.0 §2.5.4 a §2.5.7 (artefactos creados por
  este WP).
