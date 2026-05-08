```yml
created_at: 2026-05-08 00:05:00
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — std-010-compliance + state alignment

## [1.0.0] — 2026-05-07 / 2026-05-08

### Changed (state alignment, 18 archivos)

**Cluster operator (10 archivos)** — `:estado: Reservado` → `Fuera del scope`:

- uc-opr-01..10 (T-001..T-010).
- T-008 ademas: 'rol User' → 'usuario autenticado'.

**Cluster caller (5 archivos)** — `:estado: Vigente` → `Fuera del scope`:

- uc-cli-01..05 (T-011..T-015).

**Cluster supervision (3 archivos)** — `:estado: Reservado` → `Fuera del scope`:

- uc-sup-01..03 (T-016..T-018).

### Changed (STD-010 vocabulario, 18 archivos / 28 ediciones)

**Cat-A.1 PostgreSQL (1 archivo):**

- audit/index.rst (T-020): 'audit_log (PostgreSQL)' →
  'audit_log (Almacen de Datos centralizado)'.

**Cat-A.3 Elasticsearch / Postgres FTS (1 archivo):**

- audit/uc-aud-02 (T-021): 'Elasticsearch / Postgres FTS' →
  'motor de busqueda full-text del Almacen de Datos'.

**Cat-A.5 Django (2 archivos):**

- admin/index.rst (T-032): 'Django RunPython data migration' →
  'migracion de datos del Servicio de Aplicacion'.
- admin/uc-adm-02 (T-033): 'migraciones Django' →
  'migraciones de datos del Servicio de Aplicacion'.

**Cat-B Cron/APScheduler (8 archivos / 11+ refs):**

- panorama-iact.rst (T-035).
- pipeline/index.rst (T-027).
- auth/uc-auth-02 (T-022).
- access/uc-acc-08 (T-024) — 5 refs (descripcion + actor +
  usecase + relacion + nota).
- permissions/uc-perm-03 (T-025) — 4 refs.
- reports/uc-rpt-07 (T-028) — 4 refs.
- (uc-opr-08 T-008 — incluido en estado).

**Cat-C concepto rol (8 archivos / 12 refs):**

- supervision/index.rst (T-019): 'rol Supervisor (AGR-003
  quality_supervisor)' → 'AGR-003 quality_supervisor (Supervisor)'.
- audit/index.rst (T-020): 'el unico rol' → 'el unico AGR'.
- auth/uc-auth-05 (T-023): 'auto al rol User' → 'auto-otorgadas
  a usuarios autenticados'.
- permissions/uc-perm-08 (T-026): 'rol User' → 'usuarios
  autenticados' (2 refs).
- reports/uc-rpt-09 (T-029): 'auto al rol User' → 'auto-otorgada
  a usuarios autenticados'.
- users/index.rst (T-034): 'el rol UserAdmin' + 'cualquier rol
  autenticado' → 'usuarios con UserAdmin' + 'cualquier usuario
  autenticado'.
- operator/uc-opr-08 (T-008): incluido en estado.
- access/uc-acc-03 (T-036, post-validation): 2 refs 'auto al
  rol User'.

**Cat-D actor User (1 archivo):**

- reports/uc-inc-rpt-01 (T-030): `actor "User" as User <<sistema>>`
  → `actor "view_reports" as view_reports <<beneficiario>>`.
- reports/uc-rpt-11 (T-031): NO renombrado — semanticamente es
  entidad domain-model, no actor humano (decision documentada
  en `execute/t-031-decision-not-violation.md`).

### Verification

```bash
# Cat-A/A.5: cero hits ✅
grep -rn -E "PostgreSQL|Postgres FTS|MariaDB|MySQL|Elasticsearch|\bDjango\b" source/arquitectura-tecnica/use-case-view/

# Cat-B: cero hits ✅
grep -rn -E "\bCron\b|APScheduler|\bcron\b" source/arquitectura-tecnica/use-case-view/

# Cat-C: cero hits ✅
grep -rnE 'rol User|rol UserAdmin|rol Supervisor|rol autenticado|rol con acceso' source/arquitectura-tecnica/use-case-view/

# Estados desalineados: 0 ✅ (todos los UCs en use-case-view tienen
# mismo :estado: que en casos-uso)
```

## Commits del WP (~38 commits totales)

- WP setup + audit (3): wp-state, audits, task-plan.
- EXECUTE T-001..T-036 (~37 commits).
- TR-03: este commit + cierre.

## Excluded / preservado

- `access:view_sod`, `access:update_sod` (catalogo-funciones) —
  tokens opacos del contrato API, NO se renombran.
- `actor "User" as User <<sistema>>` en uc-rpt-11 — entidad
  domain-model, no actor humano (T-031 doc).
- `FTS bounded` como termino de capacidad funcional — vocabulario
  de dominio, no tecnologia.
- `HMAC` en uc-aud-04 — algoritmo estandar de seguridad,
  vocabulario de dominio.

## TR omitido por directiva del ejecutor

TR-01 (build clean serial -W -j 1) NO ejecutado en este WP por
directiva: "el build solo cuando termines TODO". Se diferira al
final de la cola de WPs (post users-alignment).

## Refs

- WP previo: 2026-05-07-23-30-26-use-case-view-users-alignment
  (en pausa, retomar despues).
- WP std-012-prefix-normalization (origen de la
  reclasificacion OPR/SUP/CLI a Fuera del scope).
- STD-010 v1.0.0.
- Backend A-005 (eliminacion concepto role).
- discover/std-010-audit.md + deep-audit-extended.md.
- execute/t-031-decision-not-violation.md.
