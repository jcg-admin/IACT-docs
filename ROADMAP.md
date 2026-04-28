# IACT-docs — Roadmap

> Trayectoria de iniciativas (ÉPICAs) del proyecto. Cada ÉPICA = 1 work package en `.thyrox/context/work/`.

## En curso

| ÉPICA | WP | Branch | Estado |
|-------|----|--------|--------|
| 4 | 2026-04-27-04-20-01-repository-diagnostics | feature/repository-diagnostics | Phase 11 TRACK (docs cerradas, pendiente CLOSURE-NOTICE) |
| 5 | 2026-04-27-05-26-20-zero-warnings-build | feature/repository-diagnostics | Phase 11 TRACK (docs cerradas, pendiente CLOSURE-NOTICE) |
| 6 | 2026-04-27-23-28-26-deployment-pipeline | feature/repository-diagnostics | Phase 10 EXECUTE (parcial — bloqueado por refs muertas) |
| 7 | 2026-04-28-00-19-57-source-references-audit | feature/repository-diagnostics | Phase 1 DISCOVER (audit-only, no fixes) |
| 8 | 2026-04-28-01-58-08-source-rebuild-strategy | feature/solve-problem-docs | Phase 6 PLAN (strategy v2.0 aprobada; spawnea 16 sub-WPs — detalle en plan del WP) |
| 9 | 2026-04-28-03-59-01-bootstrap-hardening | feature/solve-problem-docs | Phase 1 DISCOVER (Makefile guard + venv fix commiteados; F-NEW-8 pendiente) |

## Completadas

| ÉPICA | WP | Cierre | Highlights |
|-------|----|--------|------------|
| 3 | 2026-04-26-02-39-17-git-workflow-documentation | 2026-04-26 | Convención feature/* + merge develop→main + git hooks + audit trail |
| 2 | 2026-04-23-18-51-33-plantuml-java-integration-impl | 2026-04-25 | PlantUML + Java integration, color system, central styles, 13 tareas |
| 1 | 2026-04-22-21-15-30-phase1-discover-iact-docs | 2026-04-22 | Phase 1 DISCOVER inicial del proyecto |

## Pendientes / pausadas

| ÉPICA | WP | Estado | Bloqueo |
|-------|----|--------|---------|
| — | 2026-04-26-00-59-49-github-actions-phase2-testing | PENDING | Esperando merge a main de Phase 1 |
| — | 2026-04-25-04-44-30-monitor-behavior-analysis | Sin cierre formal | Pendiente decisión usuario |

## Convenciones

- Branch por ÉPICA: `feature/{nombre-corto}` (ver `git-workflow-documentation` WP).
- Cada ÉPICA atraviesa hasta 12 stages THYROX (ver `.claude/skills/thyrox/SKILL.md`).
- Cierre de ÉPICA = `track/` + `CLOSURE-NOTICE.md` o `ARCHIVED.md` + entrada en CHANGELOG.md si hay bump de versión.
