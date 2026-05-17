```yml
project: IACT-docs
work_package: 2026-05-06-20-26-07-close-all-technical-debt
created_at: 2026-05-06 20:26:07
current_phase: Phase 1 — DISCOVER → EXECUTE
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 3, 10, 11)
target: Cerrar TODAS las TDs pendientes en .thyrox/context/technical-debt.md (TD-001..007). Implementar fixes donde apliquen, marcar como Resueltos / Obsoletos / Aceptados según corresponda. Sin dejar deuda técnica.
predecessor_wp: 2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr (cerrado, ADR-BACK-007)
trigger: directiva del ejecutor "analiza todos los pendientes y los implementa, NO queremos deuda técnica".
```

# WP — Close All Technical Debt

## Trigger

Audit del corpus + technical-debt.md detectó 7 TDs pendientes
desde 2026-04-23. El ejecutor ordena cerrarlas todas.

## Inventario de TDs (estado descubierto)

| TD | Severidad | Estado real | Acción |
|---|---|---|---|
| TD-001 | ALTA | Obsoleta — el contenido "sensible" está hoy publicado intencionalmente como parte del corpus v5.6.0 | Marcar Aceptado/Obsoleto + nota |
| TD-002 | MEDIA | Pendiente real | Crear ADR `sensitive-info-policy` |
| TD-003 | MEDIA | Pendiente — `.githooks/` tiene `commit-msg`+`pre-push` pero no `pre-commit` para info sensible | Implementar `pre-commit` hook |
| TD-004 | BAJA | Pendiente — no existe README ni STRUCTURE.md | Crear `STRUCTURE.md` |
| TD-005 | MEDIA | RESUELTA — strict build pasa con `-W` en CI (validate.yml) | Marcar Resuelto |
| TD-006 | ALTA | RESUELTA — `.github/workflows/validate.yml` ya existe y valida cada PR | Marcar Resuelto |
| TD-007 | ALTA | Obsoleto — meta-task de WP DISCOVER inicial; las dependencies se cierran o son obsoletas | Marcar Obsoleto |

## Plan de batches

| Batch | TDs | Acción |
|---|---|---|
| **B-1** | TD-001 reclasificación + TD-007 obsoleto | Doc-only — actualizar technical-debt.md |
| **B-2** | TD-005 + TD-006 | Marcar Resueltas en technical-debt.md |
| **B-3** | TD-004 | Crear `STRUCTURE.md` raíz |
| **B-4** | TD-003 | Crear `.githooks/pre-commit` para info sensible |
| **B-5** | TD-002 | Crear ADR `adr-sensitive-info-policy.md` en `.thyrox/context/decisions/` |
| **B-6** | Update | technical-debt.md final con todas las resoluciones |

## Restricciones

- Cumplir R-2.0 — sin Monitor.
- Strict build (`sphinx -W`) tras cambios en source/.
- Tim Pope commits.
- TD-001: NO ejecutar git history rewrite (acción destructiva
  con force-push); reclasificar como aceptada porque el
  contenido es ahora parte normal del corpus público.

## Justificación TD-001 reclasificada

El TD-001 original (2026-04-23) reportaba que
`PROJECT_CONFIGURATION_REVIEW.md` expuso en git history:

- "RBAC model v5.1.1 (8 módulos, 44 funciones, 3 SoD)"
- "8 restricciones del sistema (CNST_001..008)"
- "Información de compliance: OWASP, NIST RBAC, ISO 27001"

**Estado en 2026-05-06:** este contenido está ahora **publicado
intencionalmente** en el corpus como parte de la documentación
del proyecto:

- RBAC v5.6.0 con 64 funciones documentadas en
  `source/arquitectura-tecnica/rbac/modelo-rbac-iact/`.
- 31 CNSTs documentados en `source/normativa/restricciones/`.
- BR-006 declara explícitamente cumplimiento NIST RBAC.

El "riesgo" original era exposición accidental; el estado actual
es **publicación deliberada y diseñada**. La severidad ya no es
ALTA — el contenido cumple su función como documentación.

**Acción:** reclasificar TD-001 como **Aceptado / Obsoleto** con
nota explicativa. El force-push de history rewrite **no es
necesario ni recomendable** dado que:

1. El contenido en cuestión es hoy parte legítima del corpus.
2. Force-push reescribiría el historial de un repo posiblemente
   compartido — riesgo de regresión > beneficio.

## Stopping points

- **SP-01**: gate humano declarado innecesario por ejecutor.
- **SP-02**: build strict 0 warnings tras cambios en source/.
- **SP-03**: technical-debt.md con todas las TDs cerradas.
