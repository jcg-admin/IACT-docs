```yml
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
created_at: 2026-05-08 01:07:10
closed_at: 2026-05-08 01:55:00
current_phase: Phase 11 — TRACK
status: Cerrado (audit-only — sin EXECUTE)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: grande (audit exhaustivo de todo source/ — solo analisis, sin ejecucion)
target: Auditar exhaustivamente todo `source/` contra CLEAN_CODE_NAMING_PRINCIPLES v1.0.0. Identificar violaciones por categoria (clases con sufijos tecnicos prohibidos, acronimos en identificadores no-opacos, vocabulario canonico STD-010, naming de archivos, metodos/variables ambiguos). El WP es **audit only** — no ejecuta correcciones. Produce reporte global + plan de remediacion fragmentado en WPs futuros priorizados por severidad.
predecessor_wp: 2026-05-08-00-17-08-use-case-view-sod-vocabulary (cerrado)
trigger: directiva del ejecutor "podrias crear un analisis de todo IACT-docs/source para ver si se esta aplicando lo siguiente: CLEAN_CODE_NAMING_PRINCIPLES v1.0.0"
```

# WP — clean-code-naming audit (whole source/)

## Trigger

El ejecutor solicito un audit exhaustivo de todo `source/`
contra el documento normativo `CLEAN_CODE_NAMING_PRINCIPLES`
v1.0.0 (vigente, scope: todo el proyecto).

## Naturaleza del WP

**AUDIT ONLY — sin EXECUTE.**

Este WP produce diagnostico + plan de remediacion. La
ejecucion se hace en WPs separados priorizados por
severidad:

- WPs futuros se abren segun decision del ejecutor tras
  revisar el reporte.
- Por volumen estimado, una sola ejecucion seria ineficiente
  y bloquearia revision por categorias.

## Categorias de audit (basadas en la norma)

| Cat | Norma | Foco |
|---|---|---|
| **C1** | §1.2, §6.2 | Clases con sufijos tecnicos prohibidos (Factory, Builder, Manager, Serializer, ViewSet, Backend, Middleware, Helper, Utils) |
| **C2** | §8 | Acronimos en identificadores no-opacos (SOD/SoD/sod, AGR, RBAC, etc.) |
| **C3** | §7 | Vocabulario canonico STD-010 (Redis, Celery, Postgres, etc. fuera de implementacion-tecnica.rst) |
| **C4** | §5 | Nombres de archivo (snake_case Python, kebab-case docs RST) |
| **C5** | §2, §3, §4 | Metodos vagos (process, handle, get_data, do_stuff), variables (`d`, `data`, `result`), constantes con nombres ambiguos |
| **C6** | §6.3 | Nombres de dominio vs framework — referencias a clases en docs que usen sufijos tecnicos |

## Output esperado

**Phase 1 DISCOVER (este WP):**

- Audit por categoria → 6 reportes en `discover/by-category/`.
- Reporte global consolidado en `discover/audit-global.md`.
- Plan de remediacion en `plan-execution/remediation-roadmap.md`
  con WPs futuros priorizados.

**Phase 11 TRACK (este WP):**

- Cierre del audit. Sin EXECUTE en este WP.

## Restricciones

- **NO modificar codigo / documentacion** durante el audit.
- Aplicar excepciones documentadas en CLEAN_CODE §8.3:
  tokens RBAC opacos (`access:*_sod`) y codigos BD persistidos
  (`SOD-001..003`) NO son violaciones.
- Distinguir entre "narrativa exempt" (`implementacion-tecnica.rst`,
  STD-010 §5.1) y "narrativa que aplica STD-010".

## Observaciones de scope

`source/` contiene principalmente documentacion RST, no codigo
Python directo. La norma aplica como sigue:

| Tipo de contenido | Aplicabilidad |
|---|---|
| Pseudocodigo en `implementacion-tecnica.rst` | Exempt (§5.1 STD-010) |
| Aliases PlantUML en `@startuml` blocks | Aplica (§8.2 norma) |
| Referencias a clases del backend en narrativa | Aplica §6 (deben usar nombres de dominio, no de framework) |
| Anchors `:ref:` y `:doc:` | Aplica §5 (snake_case y kebab-case respectivamente) |
| Filenames RST | Aplica §5.1 (kebab-case docs) |
| Identificadores de constantes en yml metadata | Aplica §4 |

## Stopping points

- **SP-01 (humano):** revisar reporte global antes de definir
  WPs futuros de remediacion.
- **SP-02 (humano):** aprobar plan de remediacion dividido
  en WPs.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES v1.0.0.
- STD-010 v1.0.0 (vocabulario abstracto).
- WPs previos: endpoint-sod-rules-rename, std-010-compliance,
  use-case-view-sod-vocabulary (precedentes parciales).
