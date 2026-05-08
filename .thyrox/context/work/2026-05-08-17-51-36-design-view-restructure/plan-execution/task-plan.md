```yml
created_at: 2026-05-08 18:25:00
project: IACT-docs
work_package: 2026-05-08-17-51-36-design-view-restructure
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Task plan — design-view restructure (9 módulos restantes)

Pattern validado en pilot `access/` (commit `842cae8b`).
Este plan replica el mismo pattern atómicamente a los 9
módulos restantes en orden de menor a mayor complejidad.

## Resumen de refs entrantes (pre-EXECUTE)

Mapeo verificado por `grep`:

- **0 refs externos** salvo 1 caso: `state-pipeline-execution`
  desde `source/arquitectura-tecnica/system-view/clases-sistema-iact.rst`
  → se actualiza en T-021 (bloque pipeline).
- **1 cross-cluster** desde access ya migrado:
  `access/state.rst` referencia `act-rbac-effective-set-eval`
  → se actualiza al final de T-013 (bloque permissions) y se
  re-targeta a `permissions/activity`.
- **Resto:** intra-cluster (mismo módulo's archivos
  referenciándose entre sí vía seealso).

## Pattern por bloque (DAG horizontal — bloques independientes)

Cada bloque (módulo) se ejecuta como un commit atómico:

```
T-XXX | Migrate <module>/
  Step 1: git mv <flat-files> <module>/<sub>.rst
  Step 2: sed update intra-cluster refs en archivos movidos
  Step 3: (si aplica) sed update cross-cluster refs desde
          módulos ya migrados que apuntan al actual
  Step 4: write <module>/index.rst (curated panorama)
  Step 5: update design-view/index.rst toctree (remove
          flat entries, add <module>/index a la sección Módulos)
  Step 6: verificar grep — 0 refs a archivos viejos
  Step 7: build strict (cada 3-4 bloques) — EXIT=0 expected
```

---

## Bloque 1 — Módulos simples (3 archivos cada uno)

- [ ] **T-011** | Migrate `admin/` (3 archivos: class + sequence)
  - `class-admin.rst` → `admin/class.rst`
  - `seq-admin.rst` → `admin/sequence.rst`
  - `admin/index.rst` (NUEVO — panorama curated del módulo
    catálogo de funciones, AGRs y reglas de separación)
  - Update `design-view/index.rst`: remove `class-admin`,
    `seq-admin` de toctrees flat; add `admin/index` a
    Módulos.
  - Verificación: `grep -rE ':doc:.*design-view/(class-admin|seq-admin)' source/` = 0

- [ ] **T-012** | Migrate `audit/` (3 archivos: class + sequence)
  - `class-audit.rst` → `audit/class.rst`
  - `seq-audit.rst` → `audit/sequence.rst`
  - `audit/index.rst` (NUEVO — AuditEvent, AuditService,
    GeneralAuditService, ExportWorker)
  - Update toctree.
  - Verificación: 0 refs viejas.

- [ ] **T-013** | Migrate `logs/` (3 archivos)
  - `class-logs.rst` → `logs/class.rst`
  - `seq-logs.rst` → `logs/sequence.rst`
  - `logs/index.rst` (NUEVO — LogStore, ApplicationLog,
    InfraLogStore, InfrastructureLog)
  - Update toctree.

- [ ] **T-014** | Migrate `users/` (3 archivos)
  - `class-users.rst` → `users/class.rst`
  - `seq-users.rst` → `users/sequence.rst`
  - `users/index.rst` (NUEVO — User, UserRepo,
    UserOnboardingService)
  - Update toctree.

**Build strict checkpoint** tras T-014 (4 bloques simples
completados).

---

## Bloque 2 — Módulos con activity transversal

- [ ] **T-015** | Migrate `permissions/` (4 archivos: class + sequence + activity)
  - `class-permissions.rst` → `permissions/class.rst`
  - `seq-permissions.rst` → `permissions/sequence.rst`
  - `act-rbac-effective-set-eval.rst` → `permissions/activity.rst`
  - `permissions/index.rst` (NUEVO — RBACRepo, GranularAccessPolicy,
    ExceptionalPermission, EffectivePermissionsAggregator)
  - **Cross-cluster fix:** sed en `access/state.rst` para
    re-targetar `act-rbac-effective-set-eval` →
    `permissions/activity`.
  - Update toctree.
  - Verificación: 0 refs viejas + 0 refs `access/state` →
    `act-rbac-effective-set-eval`.

---

## Bloque 3 — Módulos con state + activity (5 archivos cada uno)

- [ ] **T-016** | Migrate `auth/` (5 archivos)
  - `class-auth.rst` → `auth/class.rst`
  - `seq-auth.rst` → `auth/sequence.rst`
  - `state-session.rst` → `auth/state.rst`
  - `act-jwt-auth.rst` → `auth/activity.rst`
  - `auth/index.rst` (NUEVO — Session, AuthorizationGuard,
    BlacklistedToken, FunctionAuthProvider)
  - Update toctree.

- [ ] **T-017** | Migrate `alerts/` (5 archivos)
  - `class-alerts.rst` → `alerts/class.rst`
  - `seq-alerts.rst` → `alerts/sequence.rst`
  - `state-alert-event.rst` → `alerts/state.rst`
  - `act-alert-evaluation.rst` → `alerts/activity.rst`
  - `alerts/index.rst` (NUEVO — Alert, AlertRule,
    Subscription, EvaluatorReloader, AlertHook)
  - Update toctree.

- [ ] **T-018** | Migrate `pipeline/` (5 archivos)
  - `class-pipeline.rst` → `pipeline/class.rst`
  - `seq-pipeline.rst` → `pipeline/sequence.rst`
  - `state-pipeline-execution.rst` → `pipeline/state.rst`
  - `act-etl-pipeline-execution.rst` → `pipeline/activity.rst`
  - `pipeline/index.rst` (NUEVO — PipelineExecution,
    PipelineExecutionRepo, DisparadorETL, ErroresETLService)
  - **Ref externa fix:** sed en
    `source/arquitectura-tecnica/system-view/clases-sistema-iact.rst`
    para re-targetar `state-pipeline-execution` →
    `pipeline/state`.
  - Update toctree.
  - Verificación adicional:
    `grep ':doc:.*design-view/state-pipeline-execution' source/` = 0.

- [ ] **T-019** | Migrate `reports/` (5 archivos)
  - `class-reports.rst` → `reports/class.rst`
  - `seq-reports.rst` → `reports/sequence.rst`
  - `state-export-job.rst` → `reports/state.rst`
  - `act-export-async.rst` → `reports/activity.rst`
  - `reports/index.rst` (NUEVO — Report, SavedView,
    ScheduledReport, ExportJob, ExportWorker, ReportTypeRegistry)
  - Update toctree.

**Build strict checkpoint** tras T-019.

---

## Bloque 4 — Cierre

- [ ] **T-020** | Cleanup `design-view/index.rst`
  - Remove las 4 secciones de toctrees flat (Class diagrams,
    Sequence diagrams, Activity diagrams, State diagrams) que
    ahora están vacías o tienen 0 entries.
  - Mantener única sección "Módulos (cajas por módulo)" con
    los 10 módulos completos:
    `access/index, admin/index, alerts/index, audit/index,
    auth/index, logs/index, permissions/index, pipeline/index,
    reports/index, users/index`.
  - Actualizar el note de scope (Operator/Supervision/Caller
    siguen excluidos — preservar).
  - Bump `index.rst` version a `4.0.0` (MAJOR — cambio
    estructural completo del DesignView).

- [ ] **T-021** | Build strict final + TRACK changelog
  - `make html SPHINXOPTS='-W -j auto'` → EXIT=0, 0 warnings
  - Verificar inventario final:
    - 10 directorios módulo con sus respectivos sub-archivos
    - 0 archivos planos `class-*.rst`, `seq-*.rst`, `state-*.rst`,
      `act-*.rst` en `design-view/`
    - 0 refs `:doc:` rotas
  - Crear `track/wp-changelog.md`

---

## DAG de dependencias

```
T-011 (admin) ──┐
T-012 (audit) ──┤
T-013 (logs)  ──┤
T-014 (users) ──┴── checkpoint build
T-015 (permissions) [actualiza access/state] ── checkpoint build
T-016 (auth) ───┐
T-017 (alerts)──┤
T-018 (pipeline) [actualiza system-view/clases-sistema-iact]
T-019 (reports)─┴── checkpoint build
T-020 (cleanup index)
T-021 (build strict + TRACK)
```

T-011..T-014 son independientes entre sí (módulos disjuntos).
T-015 actualiza `access/state.rst` (ya migrado en pilot) →
debe ir antes de T-021 final.
T-018 actualiza `system-view/clases-sistema-iact.rst` →
único cambio fuera de design-view.
T-016, T-017, T-019 independientes.

## Estimación

| Bloque | Tasks | Archivos a tocar | Archivos nuevos |
|---|---|---|---|
| 1 (simples) | 4 | 8 mv + 4 toctree edits | 4 index.rst |
| 2 (permissions) | 1 | 3 mv + 1 cross-cluster sed + 1 toctree | 1 index.rst |
| 3 (state+activity) | 4 | 16 mv + 1 ext sed + 4 toctree | 4 index.rst |
| 4 (cierre) | 2 | 1 toctree refactor + 1 changelog | 1 changelog |
| **Total** | **11 tasks** | **~38 cambios** | **9 index + 1 changelog** |

Más ~1-3 fixes incidentales esperados (warnings de docutils
similares al pilot — markup edge cases con `*` o ``\`\`X\`\`s`
pluralización tras inline literal). Resolver caso por caso.

## Pattern del `<module>/index.rst` (referencia)

Validado en `access/index.rst` v1.0.0 (commit `842cae8b`).
8 secciones:

1. meta block (`:artefacto:`, `:tipo: ... Module Box`,
   `:modulo:`, `:estado: Vigente`, `:version: 1.0.0`)
2. label `.. _at_design_mod_<modulo>:`
3. título `Design View — MOD_X: Vista de Diseño`
4. intro paragraph (rol del módulo + ref a UCs)
5. UML panorámico CURATED (subset de class.rst — entidades
   centrales + servicios externos como puntos de contacto;
   NO duplicar repositories ni detalles internos)
6. "Lectura del diagrama" (narrativa de relaciones)
7. "Clases canónicas" (refs `:doc:` a domain-model)
8. toctree a sub-vistas + seealso a use-case-view del módulo
   y a design-view raíz

## Stopping points

- **SP-1:** revisión del task plan antes de T-011.
- **SP-2:** tras T-014 — checkpoint build strict.
- **SP-3:** tras T-019 — checkpoint build strict.
- **SP-4:** tras T-021 — final build strict + reporte TRACK.

## Refs

- DISCOVER: `wp-state.md`
- Pilot: commit `842cae8b` — pattern validado en `access/`
- Pattern reference: `source/arquitectura-tecnica/design-view/access/index.rst` v1.0.0
