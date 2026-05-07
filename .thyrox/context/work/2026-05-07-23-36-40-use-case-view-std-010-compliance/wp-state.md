```yml
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
created_at: 2026-05-07 23:36:40
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano-grande (~36 archivos, ~46 ediciones, ~3-5 h)
target: Audit y remediacion COMBINADO (Opcion A) de (1) STD-010 vocabulario, (2) alineacion A-005 concepto rol, y (3) **18 UCs con estado desincronizado** entre use-case-view y casos-uso (operator/caller/supervision — deuda heredada del WP std-012). Aprobado por ejecutor.
predecessor_wp: 2026-05-07-23-30-26-use-case-view-users-alignment (en pausa Phase 1)
trigger: directiva del ejecutor "vamos a realizar un analisis para ver si se esta respetando std-010-vocabulario-abstracto.rst" antes de Phase 8/EXECUTE del WP previo
```

# WP — use-case-view STD-010 compliance

## Trigger

El ejecutor pidio verificar cumplimiento de STD-010 en
`use-case-view/` ANTES de proceder con la creacion de
placeholders Reservado del WP anterior. La auditoria
encontro 4 categorias de violaciones.

## Hallazgos del audit

### A. Tecnologia concreta de BD (§3.2 — PROHIBIDO)

| Archivo | Linea | Texto actual | Vocabulario canonico |
|---|---|---|---|
| audit/index.rst | 20 | `audit_log (PostgreSQL)` | `audit_log` (Almacen de Datos) o solo `audit_log` |
| audit/uc-aud-02-buscar-auditoria.rst | 20 | `Elasticsearch / Postgres FTS` | el motor de busqueda full-text |

**2 refs.**

### B. Procesamiento asincrono concreto (§3.5 — PROHIBIDO)

| Archivo | Refs | Termino | Canonico |
|---|---|---|---|
| panorama-iact.rst | 1 | `cron / APScheduler` | Planificador de Tareas |
| auth/uc-auth-02-cerrar-sesion.rst | 1 | `Cron purga` | Planificador de Tareas purga |
| access/uc-acc-08-permiso-temporal.rst | 3 | `Cron de expiracion`, `Cron expiracion`, `Cron consume` | Planificador de Tareas |
| permissions/uc-perm-03-conceder-permiso-excepcional.rst | 3 | `Cron expiracion`, `Cron consume` | Planificador de Tareas |
| pipeline/index.rst | 1 | `cron / APScheduler` | Planificador de Tareas |
| reports/uc-rpt-07-programar-reporte.rst | 2 | `Cron expiracion`, `Cron-->RUN_CRON` | Planificador de Tareas |

**11 refs en 6 archivos.**

### C. Concepto "rol" / "role" (legacy post-A-005 — DESALINEADO)

Backend A-005 elimino el concepto `role` de `constants.py`,
`models.py`. RBAC v5.6.x es **function-based**, NO role-based.
Los textos que dicen "el rol X" estan desactualizados.

| Archivo | Linea | Texto actual | Reemplazo |
|---|---|---|---|
| auth/uc-auth-05-gestionar-sesiones.rst | 23 | `auto al rol User` | auto a usuarios autenticados |
| audit/index.rst | 64 | `Auditor (AGR-008) es el unico rol` | `Auditor (AGR-008) es el unico AGR` |
| reports/uc-rpt-09-configurar-filtros.rst | 21 | `auto al rol User` | auto a usuarios autenticados |
| permissions/uc-perm-08-generar-menu-dinamico.rst | 23, 64 | `auto-otorgada al rol User`, `rol User` | a usuarios autenticados |
| users/index.rst | 20, 25 | `Solo el rol UserAdmin`, `cualquier rol autenticado` | `usuarios con codename manage_users` / `cualquier usuario autenticado` |
| operator/uc-opr-08-ver-propio-dashboard.rst | 21, 63 | `al rol User` | a usuarios autenticados |
| supervision/index.rst | 33 | `rol Supervisor (AGR-003 quality_supervisor)` | `usuarios con AGR-003 quality_supervisor` |

**~10 refs en 7 archivos.**

### D. Actor "User" sin codename (§4 — PROHIBIDO en diagramas UML)

| Archivo | Linea | Texto actual | Reemplazo |
|---|---|---|---|
| reports/uc-inc-rpt-01-resolver-segmento.rst | 35 | `actor "User" as User <<sistema>>` | actor con codename especifico segun contexto |
| reports/uc-rpt-11-compartir-reporte.rst | 38 | `actor "User" as User <<sistema>>` | actor con codename especifico |

**2 refs en 2 archivos.**

## Casos NO violacion (preservar)

- `actor "Caller <<external>>"` — actor externo no-RBAC,
  representa al cliente que llama al call center. NO es
  identidad autenticada del sistema.
- `actor "AlertEngine <<system>>"`, `actor "IvrSwitch <<system>>"`,
  `actor "Scheduler <<system>>"` — sistemas externos legitimos.
- `actor "User <<authenticated>>"` y `<<unauthenticated>>`
  en panorama / index globales — usados para representar
  la abstraccion conceptual de usuario en panoramas, no
  en flujos especificos.

## Output esperado del WP

**Phase 1 DISCOVER (este artefacto):** audit detallado.

**Phase 8 PLAN EXECUTION:** task-plan con T-NNN (1 archivo
= 1 commit, ~17 archivos).

**Phase 10 EXECUTE:** aplicar vocabulario canonico
archivo-por-archivo.

**Phase 11 TRACK:** build clean serial + cierre.

## Restricciones

- NO modificar `implementacion-tecnica.rst` (esta exento
  por STD-010 §5.1).
- NO modificar `domain-model/` clases (puede usar nombres
  tecnicos por contrato — §2 exempt).
- Preservar actores genuinamente externos
  (`<<external>>`, `<<sistema>>`).
- Strict build (`-W -j 1`) tras los cambios.

## Stopping points

- **SP-01** (humano): aprobar lista de cambios antes de
  Phase 7/8.
- **SP-02:** strict build EXIT=0.
- **SP-03** (humano): aprobar cierre.

## Hipotesis iniciales

1. ~17 archivos a modificar.
2. ~25-30 ediciones individuales.
3. 0 cross-refs rotos esperados (solo cambios de prosa).
4. Esfuerzo: 1-2 h.

## Heredado / siguiente

Tras cerrar este WP, retomar
`2026-05-07-23-30-26-use-case-view-users-alignment` Phase 8
+ EXECUTE para crear los 3 placeholders Reservado
(uc-usr-05/06/07) ya con vocabulario canonico aplicado.

## Refs

- STD-010: `source/normativa/estandares/std-010-vocabulario-abstracto.rst`.
- Backend A-005: rename concepto rol -> codenames RBAC.
- WP previo: `2026-05-07-23-30-26-use-case-view-users-alignment`.
