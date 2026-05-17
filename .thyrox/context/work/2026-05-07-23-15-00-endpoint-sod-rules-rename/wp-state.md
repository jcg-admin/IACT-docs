```yml
project: IACT-docs
work_package: 2026-05-07-23-15-00-endpoint-sod-rules-rename
created_at: 2026-05-07 23:15:00
closed_at: 2026-05-07 23:30:00
current_phase: Phase 11 — TRACK
status: Cerrado
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeno (10 commits ejecucion + 3 commits planning/track = 13 commits)
target: Renombrar el endpoint REST legacy `/api/admin/sod-rules/` y `/api/access/sod-rules/` a `/api/admin/separation-rules/` y `/api/access/separation-rules/` en los 11 archivos de UCs que aun lo referencian. Backend ya migrado segun A-003 (SodRuleViewSet -> SeparationRuleViewSet). STD-013 ya declara separation-rules como path canonico. Solo falta aplicarlo en archivos de UCs.
predecessor_wp: 2026-05-07-14-49-04-uml-diagrams-deep-audit (cerrado)
trigger: el ejecutor verifico alineacion frontend-docs y detecto 20 referencias al endpoint legacy en 11 archivos
```

# WP — Endpoint sod-rules → separation-rules rename

## Trigger

El ejecutor pidio verificar la alineacion del frontend (que
ya migro segun A-001..A-005 del backend) con la documentacion
del proyecto. La verificacion encontro:

- ✅ `SodRule` clase: 0 referencias (migrado a `SeparationRule`).
- ✅ Tokens opacos `access:update_sod`, `access:view_sod`:
  preservados (son contrato API, NO se renombran).
- ❌ **Endpoint `sod-rules` (legacy)**: 20 referencias en 11
  archivos de UCs.
- ✅ Endpoint `separation-rules` (canonico): declarado en
  STD-013.

Este WP cubre la deuda detectada.

## Distincion conceptual clave

**Renombrar (este WP):**

- Path REST `/api/admin/sod-rules/` -> `/api/admin/separation-rules/`.
- Path REST `/api/access/sod-rules/` -> `/api/access/separation-rules/`.

**NO renombrar (preservar):**

- Tokens opacos de capability del backend RBAC:
  `access:update_sod`, `access:view_sod`. Son strings que el
  servidor valida en produccion. Cambiarlos rompe la
  integracion sin beneficio. NO aparecen en UI ni en
  identificadores de codigo del frontend.

## Output esperado del WP

**Phase 1 DISCOVER:** inventario exacto archivo-por-archivo
con linea + texto antes/despues.

**Phase 8 PLAN EXECUTION:** task-plan con T-NNN, 1 archivo
= 1 tarea.

**Phase 10 EXECUTE:** rename con sed o Edit por archivo,
1 commit por archivo.

**Phase 11 TRACK:** build clean serial + cierre.

## Restricciones

- **NO tocar tokens opacos de capability** (access:*_sod).
- **NO modificar STD-013** (ya canoniza separation-rules).
- **Preservar texto historico** en metamodelos (`mtm-*`) si
  documentan la migracion como contexto educativo.
- Strict build (`-W -j 1`) tras los cambios.

## Archivos in-scope (11)

**uc-adm-01 (admin/SoD rule mgmt):**

1. `source/requisitos/casos-uso/admin/uc-adm-01/actores-precondiciones.rst`
2. `source/requisitos/casos-uso/admin/uc-adm-01/flujo-principal.rst`
3. `source/requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst`

**uc-acc-05 (access/SoD rule view):**

4. `source/requisitos/casos-uso/access/uc-acc-05/actores-precondiciones.rst`
5. `source/requisitos/casos-uso/access/uc-acc-05/testing.rst`
6. `source/requisitos/casos-uso/access/uc-acc-05/implementacion-tecnica.rst`
7. `source/requisitos/casos-uso/access/uc-acc-05/flujo-principal.rst`
8. `source/requisitos/casos-uso/access/uc-acc-05/datos-involucrados.rst`
9. `source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-secuencia-crear-regla.rst`
10. `source/requisitos/casos-uso/access/uc-acc-05/criterios-aceptacion.rst`

**Norma (verificar consistencia, no rename):**

11. `source/normativa/estandares/std-013-rest-api-conventions.rst`

## Out-of-scope

- Tokens opacos `access:update_sod`, `access:view_sod` en
  `catalogo-funciones.rst` — NO se cambian.
- Concepto `role_id` en `mtm-03-metamodelo-rbac.rst` — a
  verificar como tarea separada (probablemente histórico
  educativo, no desalineado).

## Stopping points

- **SP-01:** discover/inventario aprobado antes de execute.
- **SP-02:** strict build EXIT=0 tras los renames.
- **SP-03** (humano): aprobar cierre del WP.

## Hipotesis iniciales

1. Total references a renombrar: 20 (verificadas con grep).
2. Total archivos: 11.
3. Esfuerzo estimado: 30-60 min (find/replace simple +
   build serial deterministic).
