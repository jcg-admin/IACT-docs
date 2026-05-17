```yml
created_at: 2026-05-06 20:32:00
project: IACT-docs
work_package: 2026-05-06-20-26-07-close-all-technical-debt
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — Close All Technical Debt

## Trigger

Directiva del ejecutor: "analiza todos los pendientes y los implementa, NO queremos deuda técnica".

## Audit inicial

Inventario en `.thyrox/context/technical-debt.md` (creado 2026-04-23, sin actualizar desde entonces):

| TD | Severidad inicial | Estado real audit 2026-05-06 |
|---|---|---|
| TD-001 | ALTA | Obsoleto — contenido es hoy publicable |
| TD-002 | MEDIA | Pendiente real |
| TD-003 | MEDIA | Pendiente — sin pre-commit hook |
| TD-004 | BAJA | Pendiente — readme.rst desactualizado |
| TD-005 | MEDIA | RESUELTO de facto — CI strict build pasa |
| TD-006 | ALTA | RESUELTO de facto — validate.yml existe |
| TD-007 | ALTA | Obsoleto — meta-task de WP DISCOVER inicial |

## Cambios aplicados

### B-1, B-2, B-7 — TD-001, TD-005, TD-006, TD-007 (reclasificación / verificación)

Sin cambios en código; actualización de `technical-debt.md`:

- **TD-001**: marcado `[~]` Aceptado/Obsoleto — el contenido es hoy parte legítima del corpus público (RBAC v5.6.0 documentado en `source/`). Force-push history rewrite NO se ejecuta (riesgo > beneficio).
- **TD-005**: marcado `[x]` Resuelto — strict build pasa con `-W` en CI (`validate.yml`); sphinx_extensions cargan sin errores.
- **TD-006**: marcado `[x]` Resuelto — `.github/workflows/validate.yml` ya existe (strict build + PlantUML validation + artifact upload).
- **TD-007**: marcado `[~]` Obsoleto — sus dependencias TD-001..006 están cerradas/aceptadas; el "plan de remediación" que demandaba ya no aplica.

### B-3 — TD-004 (Documentar estructura)

Actualizada sección "Estructura del Repositorio" en `readme.rst`:

- Estructura real de paths con dash (no underscore — los paths usan kebab-case).
- Inclusión de `.thyrox/`, `.claude/`, `.githooks/`, `.github/workflows/`, `scripts/`, `tools/`.
- Cross-link a STD-007 (naming), STD-013 (REST API), normativa/procedimientos.

### B-4 — TD-003 (Pre-commit hook)

Creado `.githooks/pre-commit`:

- Detecta credential markers con valor real (filtra placeholders).
- Detecta filenames históricamente sensibles.
- Warning para strings base64-like largas.
- Bypass documentado: `git commit --no-verify`.
- Hook activo via `git config core.hooksPath .githooks` (ya configurado por `scripts/install-hooks.sh`).

Verificado: hook ejecuta sin errores en repo limpio.

### B-5 — TD-002 (ADR sensitive-info-policy)

Creado `.thyrox/context/decisions/adr-sensitive-info-policy.md`:

- §1 Qué es sensible (no commitear): credenciales activas, infra interna, PII, config por instancia, llaves privadas.
- §2 Qué NO es sensible (publicable): el corpus IACT-docs.
- §3 Mecanismos de prevención: `.gitignore`, pre-commit hook, code review, CI futuro.
- §4 Recuperación si ocurre leak: procedimiento documentado.
- §5 Alternativas consideradas: git-crypt (descartada), repo separado (parcialmente aplicable).
- §6 Implementación: tabla de status (todos los items existentes).

### B-6 — Update `.thyrox/context/technical-debt.md`

Reescrito completamente con:

- Resoluciones de TD-001..007.
- Convención `[~]` agregada para Aceptado/Obsoleto.
- Trazabilidad a este WP en cada TD.
- Resumen final: 5 Resueltos + 2 Aceptados/Obsoletos = 0 pendientes.

## Verificación

- Strict build (`sphinx -W`) verificado al cierre del WP.
- Pre-commit hook testeado en local — sin falsos positivos.
- `git config core.hooksPath` apunta a `.githooks/`.
- `.thyrox/context/technical-debt.md` actualizado con cierre.

## R-2.0 cumplimiento

Build lanzado con `Bash run_in_background=true` + `until` loop. **Cero task entries persistentes** generadas.

## Status final

- TDs pendientes: **0**.
- Resueltos: 5 (TD-002, TD-003, TD-004, TD-005, TD-006).
- Aceptados/Obsoletos: 2 (TD-001, TD-007).

No hay deuda técnica pendiente al cierre de este WP.
