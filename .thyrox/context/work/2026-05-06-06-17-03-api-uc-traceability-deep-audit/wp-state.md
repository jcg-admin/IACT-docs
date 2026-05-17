```yml
project: IACT-docs
work_package: 2026-05-06-06-17-03-api-uc-traceability-deep-audit
created_at: 2026-05-06 06:17:03
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 3, 5, 6, 8, 10, 11)
target: Verificar trazabilidad UC-a-endpoint para los 65 UCs in-scope. Producir tabla canonical {UC_id | endpoint | view_class | url_pattern | docstring_present} + propuesta de docstring estandar para anchor tecnico.
predecessor_analysis: analisis informal compartido por el ejecutor que mapea dominio→app pero NO UC→endpoint
related_wps:
  - 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass (los 99 UCs)
  - 2026-05-06-05-28-57-design-view-buildout (DesignView con 65 UCs in-scope)
out_of_scope: uc-opr-* + uc-sup-* + uc-cli-* (decision del ejecutor — no implementados)
```

# WP — API ↔ UC Traceability Deep Audit

## Trigger

Analisis previo del ejecutor afirmo que "los 65 UCs in-scope tienen
app en el API". Critica adversarial revelo que la verificacion fue
a nivel **dominio → app**, no a nivel **UC → endpoint**:

> Coverage por dominio ≠ coverage por UC. La afirmacion correcta
> seria: "los 10 dominios in-scope tienen una app correspondiente
> en el API".

Para tomar decisiones de implementacion basadas en cobertura real,
se requiere verificacion granular UC-a-endpoint.

## Objetivo

Producir tabla canonica con una fila por cada uno de los 65 UCs
in-scope. Cada fila debe responder:

| Columna | Significado |
|---|---|
| UC_id | UC_AUTH_01, UC_PERM_07, etc. |
| modulo | dominio doc (auth, access, ...) |
| app_django | app del backend que lo implementa |
| endpoint | ruta URL (e.g. POST /api/auth/login) |
| view_class | clase de Django REST Framework (e.g. LoginView) |
| serializer | serializador asociado |
| docstring_uc_id | true/false: ¿la docstring del view menciona el UC? |
| status | implementado / parcial / faltante / no-aplica |

## Hallazgos a verificar (heredados del analisis informal)

| ID | Hallazgo | Severidad | Verificacion requerida |
|---|---|---|---|
| H-1 | uc-rpt-05 y uc-rpt-06 ausentes del docs | media | git log para identificar si fueron eliminados/renombrados |
| H-2 | App `dashboard` en API sin UC documentado | alta | ¿es funcionalidad nueva o subset de UC_RPT_01/02? |
| H-3 | App `ivr` (caller) out-of-scope por diseno | nota | ya documentado en WP design-view-buildout |
| H-4 | Sin UC-ID en docstrings/comentarios | baja | propuesta de docstring estandar |

## Mapeos sospechosos del analisis informal

El analisis previo presento estos mapeos sin justificacion:

- `admin (3 UCs) → users app` — UC_ADM_01..03 son **gestion del
  catalogo RBAC** (SoD rules, function catalog, system groups),
  no gestion de usuarios. ¿Por que esta bajo `users`?
- `logs (7) → pipeline app` — observabilidad tecnica vs ETL.
  ¿Reuso intencional o mapeo accidental?

Estos mappings deben validarse con evidencia del codigo.

## Output esperado

1. `discover/api-uc-traceability-deep-audit-analysis.md` — Phase 1
   con scope, hipotesis, plan.
2. `analyze/uc-endpoint-coverage-matrix.md` — tabla canonica de
   65 filas con verificacion granular.
3. `analyze/dashboard-feature-gap-analysis.md` — H-2 expandido:
   ¿es UC nuevo o subset?
4. `analyze/uc-rpt-05-06-investigation.md` — H-1 git archaeology.
5. `analyze/admin-logs-mapping-validation.md` — validacion de los
   mappings sospechosos.
6. `track/recommendations.md` — propuesta:
   - Docstring estandar con UC-ID anchor.
   - WPs sucesores para UCs faltantes (si los hay).
   - Decision sobre dashboard (backfill UC vs ADR).

## Restricciones

- **Sin scripts** invasivos al codigo del API (read-only).
- **Sin asumir** que existencia de app == implementacion completa.
- **Verificacion bidireccional**:
  - UC → endpoint (cobertura).
  - endpoint → UC (over-implementation, dashboard gap).

## Stopping points

- **SP-01** (gate humano): aprobar bootstrap + access al codigo del API.
- **SP-02** (gate humano): aprobar matriz despues de muestra (5 UCs).
- **SP-03** (gate humano): aprobar recomendaciones.

## Pre-requisitos

- Acceso de lectura al repositorio del backend (Django) para
  inspeccionar `urls.py`, `views.py`, `serializers.py` por app.
- Sin acceso al backend, este WP queda en Phase 1 DISCOVER hasta
  que el ejecutor provea contexto.

## Anatomia del WP

```
2026-05-06-06-17-03-api-uc-traceability-deep-audit/
├── wp-state.md
├── discover/
│   └── api-uc-traceability-deep-audit-analysis.md
├── analyze/
│   ├── uc-endpoint-coverage-matrix.md      ← tabla 65 filas
│   ├── dashboard-feature-gap-analysis.md
│   ├── uc-rpt-05-06-investigation.md
│   └── admin-logs-mapping-validation.md
└── track/
    ├── recommendations.md
    └── api-uc-traceability-deep-audit-changelog.md
```

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | No se tiene acceso al codigo del API en este repo | WP queda DISCOVER-only hasta que ejecutor provea acceso o transcript del codigo |
| R-02 | Mappings ambiguos UC-endpoint (1:N) | Documentar todas las relaciones, no forzar 1:1 |
| R-03 | Dashboard gap genera scope creep (nuevos UCs) | Solo identificar el gap, NO documentar UCs aqui |
| R-04 | Sesgo del analisis previo (mismo autor de docs) | Verificacion adversarial: cada claim contra evidencia textual del codigo |
