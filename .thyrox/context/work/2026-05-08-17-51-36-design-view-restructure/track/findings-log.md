```yml
created_at: 2026-05-08 18:30:00
project: IACT-docs
work_package: 2026-05-08-17-51-36-design-view-restructure
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: En progreso
```

# Findings log — Phase 10 EXECUTE

Hallazgos en orden cronologico durante la migracion de los
9 modulos restantes (T-011..T-021).

## H-00 — Pilot access (commit 842cae8b)

- 1 warning de docutils detectado y fix in-band: `Assignment``s`
  (sufijo plural tras inline literal) en `access/index.rst:80`.
  Reescrito como "instancias de Assignment".
- 0 refs externos a romper en los 4 archivos del cluster.
- Pattern de 8 secciones del module index.rst validado.


## H-01 — Block 1 (T-011..T-014) admin/audit/logs/users

- **Pluralizacion tras inline literal** (mismo pattern que pilot):
  `admin/index.rst:69` `\`\`Function\`\`s` → fix in-band a
  "instancias de Function".
- **Forward refs a modulos no migrados:** `users/index.rst`
  referencia `auth/index` (no creado aun); fail strict build.
  Decision: continuar T-015..T-019 sin build intermedio
  (los forward refs se resuelven cuando todos los modulos
  esten migrados). Build strict definitivo tras T-019.
- **Cambio al plan:** removido el "build checkpoint tras T-014"
  ya que los module index.rst tienen seealso cruzados a
  modulos hermanos. Build strict solo posible cuando los 10
  estan en su nuevo lugar.


## H-02 — Block 2 (T-015 permissions)

- Cross-cluster fix aplicado correctamente: `access/state.rst`
  re-targeteado de `act-rbac-effective-set-eval` a
  `permissions/activity` durante T-015 (sed scoped).

## H-03 — Block 3 (T-016..T-019 auth/alerts/pipeline/reports)

- **T-018 ext fix:** `system-view/clases-sistema-iact.rst:124`
  re-targeteado de `state-pipeline-execution` a
  `pipeline/state` (la unica ref a design-view fuera de
  design-view).
- 0 warnings adicionales en estos 4 modulos (5 archivos
  c/u, 4 modulos = 20 archivos migrados sin problemas
  markup).

## H-04 — T-020 cleanup design-view/index.rst

- Bumped 3.1.0 → 4.0.0 (MAJOR — cambio estructural completo).
- Removidas 4 secciones de toctree flat (Class, Sequence,
  Activity, State) — todas vacias post-migracion.
- Unica seccion activa de toctree: "Modulos del DesignView"
  con los 10 modulos en orden alfabetico.
- Tabla "Tipos de diagramas" actualizada: agregada fila
  "Module box (caja)" como punto de entrada.
- Note de scope (Operator/Supervision/Caller excluidos) preservada.
- Note nuevo documenta la reorganizacion v4.0.0.

## H-05 — Build strict final (T-021)

- `make html SPHINXOPTS='-W -j auto'` EXIT=0, 0 warnings.
- 43 archivos en design-view tree (vs 33 originales = +10
  index.rst nuevos — coincide con estimacion).
- 0 refs huerfanas detectadas pre-build:

```
class-{admin,audit,logs,users,permissions,auth,alerts,pipeline,reports}: 0
seq-* : 0
state-{session,alert-event,pipeline-execution,export-job,assignment}: 0
act-{rbac-*,jwt-auth,alert-evaluation,etl-*,export-async,validacion-*}: 0
```

## Resumen final del WP

| Metrica | Antes | Despues |
|---|---|---|
| Top-level archivos en design-view | 33 (planos) | 2 (index + package-overview) |
| Directorios de modulo | 0 | 10 |
| Archivos totales en design-view | 33 | 43 (+10 index.rst nuevos) |
| Refs externas a design-view | 1 (system-view) | 1 (re-targeteada) |
| Refs internas inter-archivo | ~30+ flat | 100% reorganizadas |

**0 contenido sustantivo perdido.** Todos los UML diagrams,
tablas, notas y narrativa preservados via git mv.
