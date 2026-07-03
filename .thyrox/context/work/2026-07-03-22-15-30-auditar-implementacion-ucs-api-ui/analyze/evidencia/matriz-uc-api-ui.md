```yml
created_at: 2026-07-03 22:15:30
project: IACT-docs
work_package: 2026-07-03-22-15-30-auditar-implementacion-ucs-api-ui
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
```

# Evidencia — matriz UC docs × api × ui

Registro de comandos exactos y observables que sustentan los conteos
publicados en la iniciativa (protocolo grep-validated-audit).

## Comandos de inventario (PROVEN)

```bash
# 88 UCs en docs
find source/requisitos/requisitos-funcionales -mindepth 2 -maxdepth 2 \
  -type d -name "uc-*" | wc -l                     # => 88

# markers api / ui con compuestos y rangos
grep -rhoE 'UC[_-][A-Z]{2,5}[_-][0-9]{1,2}([./,-]+[0-9]{1,2})*' \
  --include='*.py' /home/user/IACT-api
grep -rhoE 'UC[_-][A-Z]{2,5}[_-][0-9]{1,2}([./,-]+[0-9]{1,2})*' \
  --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' \
  /home/user/IACT-ui/src
# normalizados y expandidos → api 73 fuertes / ui 73 fuertes
# (clasificador fuerte/débil: número explícito vs interior de rango)

# OUT sin rastro en código
grep -rliE 'UC[_-](OPR|SUP|CLI)[_-][0-9]' --include='*.py' /home/user/IACT-api   # 0
grep -rliE 'UC[_-](OPR|SUP|CLI)[_-][0-9]' /home/user/IACT-ui/src                 # 0
```

## Diferencias entre conjuntos fuertes (PROVEN)

- api-only: `UC_DSH_01`, `UC_DSH_04` (+02/03 por rango `UC_DSH_01..04`
  en `config/urls.py:41`), `UC_PERM_09`, `UC_USR_08` → deuda inversa F-05.
- ui-only: `UC_ACC_06`, `UC_ACC_07`, `UC_ADM_02`, `UC_ALR_06` → F-03/F-04/F-07.

## Inspecciones de bucket negativo (observables)

| Claim ingenuo | Observable que lo refuta | Archivo:línea |
|---|---|---|
| "uc-037 sin ui" | marker compuesto `UC_RPT_07/08` + llamadas reales a `/api/reports/schedules/` | `IACT-ui/src/services/reportsGateway.js:21,111`; `src/router/AppRouter.jsx` ruta `/reports/scheduled` |
| "uc-086/087 sin api" | endpoints `separation-rules/` y `functions/` registrados | `IACT-api/callcentersite/apps/access/urls.py:94,131` |
| "uc-091 sin implementar" | `class ETLScheduler` presente | `IACT-api/callcentersite/apps/pipeline/scheduler.py` |
| "uc-088 sin api" | marker explícito `UC_ADM_03` en AccessGroup ViewSet | `IACT-api/callcentersite/apps/access/views.py:169,190` |
| "uc-054 ui divergente" | api sirve `/api/alerts/me/subscriptions/` (UC_ALR_05); ui lo marca UC_ALR_06 | `IACT-api/callcentersite/apps/alerts/urls.py:52`; `IACT-ui/src/services/alertsGateway.js:25-27` |
| OUT operator | "Modulo reservado (out-of-scope para v5.6.0)" | `source/requisitos/requisitos-funcionales/operator/index.rst` |

## Hallazgo F-04 (observable)

`IACT-ui/src/services/accessGateway.js:10-12` declara:
`getSegments() → /access/segments no existe`,
`assignSegment() → /access/segments/assign no existe` — las pantallas
ui `UC_ACC_06/07` no tienen backend ni UC docs.

## Hallazgo F-06 (observable)

`IACT-ui/src/components/pages/Analytics/ScheduledReports.jsx` define
`mockSchedules` hardcodeados; la ruta `/reports/scheduled` monta
`ScheduledReportPage` (INFERRED: componente legacy no ruteado).

## Matriz completa

Generada programáticamente (88 filas) en
`source/gestion/pm/iniciativas/auditar-implementacion-ucs-api-ui/matriz-implementacion-uc-api-ui.rst`.
Conteos: 18 OUT · 70 in-scope · api 70/70 · ui 69/69 aplicables · 0 gaps.
