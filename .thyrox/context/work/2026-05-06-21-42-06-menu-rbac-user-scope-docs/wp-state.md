```yml
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
created_at: 2026-05-06 21:42:06
closed_at: 2026-05-07 04:08:13
current_phase: Phase 11 — TRACK
status: Cerrado (aprobado por ejecutor 2026-05-07)
successor_wp: 2026-05-07-04-08-13-use-case-view-analysis
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 5, 7, 11 ejecutados)
target: Documentar formalmente el WP frontend menu-rbac-user-scope en IACT-docs. Aterrizar el filtrado del sidebar por capabilities del user en artefactos del corpus (UC, BR, FR/NFR donde aplique) sin duplicar lo ya documentado (UC_PERM_08, CNST-032). Producir documentación que sirva como spec para el frontend.
predecessor_wp: 2026-05-06-21-19-26-rbac-v5-6-0-alignment-audit (cerrado, AGR-010 = 9 funciones explícitas)
sibling_wp: 2026-05-06-23-25-08-std-010-corpus-compliance (cerrado — 7 correcciones STD-010 aplicadas)
trigger: directiva del ejecutor "vamos a crear un nuevo WP menu-rbac-user-scope para empezar la documentación; genera análisis de qué se espera"
```

# WP — Menu RBAC User Scope (Documentación)

## Trigger

El frontend está implementando `menu-rbac-user-scope` (WP separado en repo frontend) con:

- Filtrado de `ALL_NAV_LINKS` por capabilities del user.
- Mock interceptor para `/api/permisos/verificar/{userId}/capacidades/`.
- Sub-menús OUT-OF-SCOPE.

IACT-docs debe documentar **qué se espera del comportamiento** sin duplicar lo que ya existe en UC_PERM_08 + CNST-032.

## Output esperado del WP

Análisis DISCOVER en `discover/menu-rbac-user-scope-docs-analysis.md` con:

1. Contexto IACT-docs existente sobre menu+RBAC.
2. Gap analysis vs el alcance del frontend.
3. Stakeholders.
4. Requisitos funcionales y no funcionales esperados.
5. Riesgos y restricciones.
6. Recomendación de qué documentar (decisión de Phase 6 SCOPE pendiente).

## Restricciones

- NO duplicar UC_PERM_08 (ya cubre "Generar Menu Dinámico").
- NO contradecir CNST-032 (Menu Dinámico Obligatorio).
- Cumplir R-2.0 — sin Monitor.
- Strict build (`-W`) tras cualquier cambio en source/.

## Stopping points

- **SP-01**: gate humano declarado innecesario.
- **SP-02**: build strict 0 warnings tras cambios en source/.
- **SP-03** (humano): aprobar el scope antes de ejecutar Phase 7 DESIGN.

## Resumen de cierre (2026-05-07)

El WP cubrio Phases 1, 5, 7, 11 (Phases 2/3/4/6/8/9/10 saltadas
por tamaño). 8 commits totales producidos.

**Phase 1 DISCOVER:** 11 archivos en ``discover/`` (analisis legacy
C_MENU2, design corrections, std-010 audit, final decisions
P1-P4 + 3 items pendientes resueltos).

**Phase 5 STRATEGY:** 3 archivos en ``strategy/`` (solution-strategy
con KI-1..KI-3, P1-P4, AP-1..AP-7, traceability matrix; addendum
con D-MOD-001 + 5 gaps + DAG; gap-3-4-decision-rationale).

**Phase 7 DESIGN:** 10 artefactos producidos en 5 lotes (DAG con
paralelismo):

- L1 (commit ``cd224ee5``): ADR-BACK-008/009/010.
- L2 (commit ``8ed97a16``): CNST-032 v2.0.0 + Q9 ext + cache-strategy.
- L3 (commit ``86b1696f``): UC_ADM_04 + UC_PERM_08 ext.
- L4+L5 (commit ``43624501``): UC_ADM_05 + scheduled-tasks.

**Phase 11 TRACK:** 5 archivos en ``track/``:

- ``post-design-coverage-review.md`` (gaps G-1..G-10).
- ``dependency-graph-and-domain-model-coverage.md``
  (decision Opcion B 67/80 + DAG + gaps G-11..G-18).
- ``deep-review-coverage.md`` (DR-1..DR-4 + decisiones
  D-DR-001..003).
- ``menu-rbac-user-scope-docs-changelog.md`` (Keep a Changelog).
- ``lessons-learned.md`` (10 aprendizajes generalizables).

**Cierre formal:**

- Lote C-A (commit ``89ef4d61``): catalogo + mapeo + BR-006 + tests.
- Lotes C-B + C-C + C-D (commit ``92ebeb0e``): vista UC + 4 clases
  domain-model nuevas + 4 clases actualizadas + misc.
- Phase 11 deep-review fixes (este commit): D-DR-001 alineacion
  catalogo critico + D-DR-002 cross-refs ADR-BACK-008 + D-DR-003
  changelog + lessons learned + wp-state.

**Status de items diferidos (no bloqueantes):**

- G-8: CNST-033 cross-ref a CNST-032 v2.0.0 — diferido.
- TD-RBAC-03: ``manage_critical_function_flag`` sin titular runtime
  — registrada en ``.thyrox/context/technical-debt.md``.

**Build:** sphinx strict EXIT=0 sin warnings al cierre.
**Aprobacion del cierre:** pendiente del ejecutor.
