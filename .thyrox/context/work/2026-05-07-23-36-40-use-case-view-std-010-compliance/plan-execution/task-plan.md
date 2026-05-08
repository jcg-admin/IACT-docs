```yml
created_at: 2026-05-07 23:55:00
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Task Plan
```

# Task Plan — std-010-compliance + state alignment

> 35 tareas EXEC + 3 TR = 38 tareas atomicas.
> 1 archivo = 1 commit. Sin builds intermedios.

## Bloque 1: EXECUTE — cluster operator (10 archivos)

Cambio: `:estado: Reservado` → `:estado: Fuera del scope`.
Archivos uc-opr-08 ademas tiene Cat-C (rol User → usuario
autenticado).

- [ ] **T-001** — `operator/uc-opr-01-cambiar-estado-del-agente.rst` (estado).
- [ ] **T-002** — `operator/uc-opr-02-atender-llamada-entrante.rst` (estado).
- [ ] **T-003** — `operator/uc-opr-03-realizar-llamada-saliente.rst` (estado).
- [ ] **T-004** — `operator/uc-opr-04-hold-unhold-llamada.rst` (estado).
- [ ] **T-005** — `operator/uc-opr-05-transferir-llamada.rst` (estado).
- [ ] **T-006** — `operator/uc-opr-06-ingresar-disposition.rst` (estado).
- [ ] **T-007** — `operator/uc-opr-07-solicitar-break-pausa.rst` (estado).
- [ ] **T-008** — `operator/uc-opr-08-ver-propio-dashboard.rst` (estado + Cat-C).
- [ ] **T-009** — `operator/uc-opr-09-ver-propio-historial-de-llamadas.rst` (estado).
- [ ] **T-010** — `operator/uc-opr-10-recibir-notificacion-supervisor.rst` (estado).

## Bloque 2: EXECUTE — cluster caller (5 archivos)

Cambio: `:estado: Vigente` → `:estado: Fuera del scope`.

- [ ] **T-011** — `caller/uc-cli-01-iniciar-llamada-al-call-center.rst`.
- [ ] **T-012** — `caller/uc-cli-02-navegar-ivr.rst`.
- [ ] **T-013** — `caller/uc-cli-03-esperar-en-cola.rst`.
- [ ] **T-014** — `caller/uc-cli-04-solicitar-callback.rst`.
- [ ] **T-015** — `caller/uc-cli-05-calificar-atencion-post-call.rst`.

## Bloque 3: EXECUTE — cluster supervision (4 archivos)

- [ ] **T-016** — `supervision/uc-sup-01-monitorear-llamada-whisper.rst` (estado).
- [ ] **T-017** — `supervision/uc-sup-02-barge-in-en-llamada.rst` (estado).
- [ ] **T-018** — `supervision/uc-sup-03-mensaje-broadcast-al-equipo.rst` (estado).
- [ ] **T-019** — `supervision/index.rst` (Cat-C "rol Supervisor").

## Bloque 4: EXECUTE — cluster audit (2 archivos)

- [ ] **T-020** — `audit/index.rst` (Cat-A.1 PostgreSQL + Cat-C "rol").
- [ ] **T-021** — `audit/uc-aud-02-buscar-auditoria.rst` (Cat-A.3 Elasticsearch / Postgres FTS).

## Bloque 5: EXECUTE — cluster auth (2 archivos)

- [ ] **T-022** — `auth/uc-auth-02-cerrar-sesion.rst` (Cat-B Cron purga).
- [ ] **T-023** — `auth/uc-auth-05-gestionar-sesiones.rst` (Cat-C "rol User").

## Bloque 6: EXECUTE — cluster access (1 archivo)

- [ ] **T-024** — `access/uc-acc-08-permiso-temporal.rst` (Cat-B Cron).

## Bloque 7: EXECUTE — cluster permissions (2 archivos)

- [ ] **T-025** — `permissions/uc-perm-03-conceder-permiso-excepcional.rst` (Cat-B Cron).
- [ ] **T-026** — `permissions/uc-perm-08-generar-menu-dinamico.rst` (Cat-C "rol User").

## Bloque 8: EXECUTE — cluster pipeline (1 archivo)

- [ ] **T-027** — `pipeline/index.rst` (Cat-B cron / APScheduler).

## Bloque 9: EXECUTE — cluster reports (4 archivos)

- [ ] **T-028** — `reports/uc-rpt-07-programar-reporte.rst` (Cat-B Cron).
- [ ] **T-029** — `reports/uc-rpt-09-configurar-filtros.rst` (Cat-C "rol User").
- [ ] **T-030** — `reports/uc-inc-rpt-01-resolver-segmento.rst` (Cat-D actor User).
- [ ] **T-031** — `reports/uc-rpt-11-compartir-reporte.rst` (Cat-D actor User).

## Bloque 10: EXECUTE — cluster admin (2 archivos)

- [ ] **T-032** — `admin/index.rst` (Cat-A.5 Django RunPython).
- [ ] **T-033** — `admin/uc-adm-02-gestionar-catalogo-de-funciones.rst` (Cat-A.5 migraciones Django).

## Bloque 11: EXECUTE — cluster users + panorama (2 archivos)

- [ ] **T-034** — `users/index.rst` (Cat-C "rol UserAdmin", "rol autenticado").
- [ ] **T-035** — `panorama-iact.rst` (Cat-B cron / APScheduler).

## Bloque 12: TRACK (3)

- [ ] **TR-01** — Build clean serial deterministic (`-W -j 1`).
- [ ] **TR-02** — Verificar EXIT=0 + 0 warnings + grep validation.
- [ ] **TR-03** — Cierre WP: changelog + wp-state status=Cerrado.

## Convenciones de commit (Tim Pope)

- T-NNN estado-only: `Realign state to Fuera del scope in {archivo}`
- T-NNN vocabulario-only: `Apply STD-010 canonical vocabulary in {archivo}`
- T-NNN combinado: `Realign state and apply STD-010 vocabulary in {archivo}`
