```yml
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
created_at: 2026-05-06 21:42:06
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño-mediano (Stages 1, 3, 5, 7, 10, 11)
target: Documentar formalmente el WP frontend menu-rbac-user-scope en IACT-docs. Aterrizar el filtrado del sidebar por capabilities del user en artefactos del corpus (UC, BR, FR/NFR donde aplique) sin duplicar lo ya documentado (UC_PERM_08, CNST-032). Producir documentación que sirva como spec para el frontend.
predecessor_wp: 2026-05-06-21-19-26-rbac-v5-6-0-alignment-audit (cerrado, AGR-010 = 9 funciones explícitas)
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
