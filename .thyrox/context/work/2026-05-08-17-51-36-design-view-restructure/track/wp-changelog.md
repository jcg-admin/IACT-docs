```yml
created_at: 2026-05-08 20:15:00
project: IACT-docs
work_package: 2026-05-08-17-51-36-design-view-restructure
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — design-view-restructure

## [1.0.0] — 2026-05-08

### Resumen

Reorganización completa de `source/arquitectura-tecnica/design-view/`
de 33 archivos planos a estructura de cajas por módulo,
siguiendo la convención ya establecida en `use-case-view/`.

10 directorios módulo (`access/`, `admin/`, `alerts/`, `audit/`,
`auth/`, `logs/`, `permissions/`, `pipeline/`, `reports/`, `users/`),
cada uno con su `index.rst` (caja Kruchten) + sub-archivos
(`class.rst`, `sequence.rst`, opcionalmente `state.rst` y
`activity.rst`).

Modulos excluidos del DesignView (preservados como out-of-scope
en `use-case-view/` solamente): `caller/`, `operator/`,
`supervision/` — caller es externo IVR, operator/supervision
deferidos a WPs futuros.

### Renamed (31 archivos via `git mv`, history preservada)

#### Bloque pilot (commit 842cae8b — access)
- `class-access.rst`              → `access/class.rst`
- `seq-access.rst`                → `access/sequence.rst`
- `state-assignment.rst`          → `access/state.rst`
- `act-validacion-separacion.rst` → `access/activity.rst`

#### Bloque 1 (commits T-011..T-014)
- `class-admin.rst` / `seq-admin.rst`     → `admin/{class,sequence}.rst`
- `class-audit.rst` / `seq-audit.rst`     → `audit/{class,sequence}.rst`
- `class-logs.rst` / `seq-logs.rst`       → `logs/{class,sequence}.rst`
- `class-users.rst` / `seq-users.rst`     → `users/{class,sequence}.rst`

#### Bloque 2 (T-015 permissions)
- `class-permissions.rst`            → `permissions/class.rst`
- `seq-permissions.rst`              → `permissions/sequence.rst`
- `act-rbac-effective-set-eval.rst`  → `permissions/activity.rst`

#### Bloque 3 (T-016..T-019 con state + activity)
- `class-auth.rst` / `seq-auth.rst` /
  `state-session.rst` / `act-jwt-auth.rst` →
  `auth/{class,sequence,state,activity}.rst`
- `class-alerts.rst` / `seq-alerts.rst` /
  `state-alert-event.rst` / `act-alert-evaluation.rst` →
  `alerts/{class,sequence,state,activity}.rst`
- `class-pipeline.rst` / `seq-pipeline.rst` /
  `state-pipeline-execution.rst` / `act-etl-pipeline-execution.rst` →
  `pipeline/{class,sequence,state,activity}.rst`
- `class-reports.rst` / `seq-reports.rst` /
  `state-export-job.rst` / `act-export-async.rst` →
  `reports/{class,sequence,state,activity}.rst`

### Added (10 nuevos `index.rst` por módulo)

Cada `<module>/index.rst` sigue pattern de 8 secciones:
1. meta block (artefacto, tipo Module Box, modulo, version)
2. label `.. _at_design_mod_<modulo>:`
3. título "Design View — MOD_X: Vista de Diseño"
4. intro paragraph (rol del módulo + ref a UCs)
5. **UML panorámico CURATED** — subset enfocado en
   relaciones inter-módulo (NO duplica `class.rst`)
6. "Lectura del diagrama"
7. "Clases canónicas que materializan el módulo"
   (`:doc:` a domain-model)
8. toctree a sub-vistas + seealso

### Changed

- `design-view/index.rst` v3.1.0 → **v4.0.0** (MAJOR):
  - Removidas 4 secciones de toctree flat (Class, Sequence,
    Activity, State) — todas vacías post-migración.
  - Única sección activa: "Módulos del DesignView" con los
    10 módulos en orden alfabético.
  - Tabla "Tipos de diagramas" extendida con "Module box
    (caja)" como tipo principal.
  - Note nuevo documenta la reorganización v4.0.0.
  - Note de scope (Operator/Supervision/Caller excluidos)
    preservado.

### Cross-refs migration

- **Intra-cluster** (refs entre archivos del mismo módulo):
  ~30 seealso re-targeteados a las nuevas paths
  `design-view/<module>/<sub>` via sed scoped.
- **Cross-cluster** (1 caso): `access/state.rst` →
  `act-rbac-effective-set-eval` re-targeteado a
  `permissions/activity` durante T-015.
- **Externos** (1 caso): `system-view/clases-sistema-iact.rst`
  → `state-pipeline-execution` re-targeteado a
  `pipeline/state` durante T-018.

### Hallazgos durante EXECUTE

Documentados en `track/findings-log.md`:

- **H-00 / H-01** Pluralización tras inline literal:
  `\`\`X\`\`s` (sufijo plural sin escape) genera warning
  "Inline literal start-string without end-string". Pattern
  detectado en pilot y repetido en `admin/index.rst:69`.
  Fix in-band: reescribir como "instancias de X".
- **H-01** Forward refs entre módulos hermanos en seealso
  causan strict build fail si se intenta build intermedio
  con módulos parcialmente migrados. Decisión: omitir
  build checkpoint tras T-014 y T-019; build strict única
  vez al final.
- **H-02..H-05** Sin warnings adicionales ni hallazgos
  bloqueantes.

### Verification (T-021 build strict final)

```bash
$ make html SPHINXOPTS='-W -j auto'
build succeeded.
EXIT=0
```

```bash
$ ls source/arquitectura-tecnica/design-view/
access/  admin/  alerts/  audit/  auth/  index.rst
logs/  package-overview.rst  permissions/  pipeline/
reports/  users/

$ find source/arquitectura-tecnica/design-view -name '*.rst' | wc -l
43
```

```
33 archivos planos antes → 43 archivos en estructura modular:
  +10 index.rst nuevos por módulo
  -0 contenido sustantivo perdido (git mv preserva history)
```

### Commits del WP (en orden)

1. `6c90d862` — Phase 1 DISCOVER initial
2. `b2663ec5` — DISCOVER deep + SP-D1 closed
3. `842cae8b` — Pilot access/ (validó pattern)
4. `96685b82` — Phase 8 PLAN
5. (este commit batch) — T-011..T-021 + TRACK

### Roadmap status

| WP | Estado |
|---|---|
| design-view-restructure (este) | ✅ Completado |

10/10 módulos in-scope migrados a cajas. DesignView
v4.0.0 publicado. Próximas vistas Kruchten 4+1 a abordar
según DAG (siguen DesignView en el orden propuesto):
- ProcessView → requiere UseCaseView ✓ + DesignView ✓ +
  DeployView
- ImplementationView → requiere UseCaseView ✓ + DesignView ✓
- DeployView → requiere UseCaseView ✓

### Refs

- DISCOVER: `wp-state.md`
- PLAN: `plan-execution/task-plan.md`
- Findings: `track/findings-log.md`
- Build evidence: `track/build-logs/sphinx-strict-final-*.log`
- Pattern reference: `source/arquitectura-tecnica/design-view/access/index.rst` v1.0.0
