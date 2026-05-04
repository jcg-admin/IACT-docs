```yml
created_at: 2026-05-04 07:50:12
project: IACT-docs
work_package: 2026-05-04-07-50-12-mod-admin-requisitos-integration
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — MOD_Admin Integración en source/requisitos/*

Integrar el nuevo módulo MOD_Admin en todos los puntos de la documentación
de requisitos que aún referencian los phantom UCs 043-047 o que requieren
los nuevos UC specs completos.

---

## Bloque A — Phantom UC refs en requisitos-funcionales y base-cognitiva

- [x] **T-001** `fr-010-02-validar-sod-antes-asignar.rst`: `UC_043`→`UC_ADM_01`
  (2 ocurrencias).
- [x] **T-002** `fnd-03-casos-de-uso.rst`: UC-043→UC_ADM_01, UC-044→UC_ACC_03,
  UC-045→UC_ADM_03, UC-046→UC_ADM_02, UC-047→UC_ACC_09 (todas las
  ocurrencias como UCs de SoD/acceso — NO tocar UCs de reports).
- [x] **T-003** `fnd-04-trazabilidad.rst`: idem + actualizar etiqueta
  `.. _uc-043:` → `.. _uc-adm-01:` y `:artefacto: UC_043` → `UC_ADM_01`.
- [x] **T-004** `fnd-05-jerarquia-4-niveles.rst`: UC-043→UC_ADM_01,
  UC-044→UC_ACC_03, UC-047→UC_ACC_09.
- [x] **T-005** `txm-01-taxonomia-requisitos.rst`: actualizar referencia
  UC-043 en lista de UC de access/admin.

## Bloque B — Arquitectura técnica

- [ ] **T-006** `rbac-core/responsabilidades.rst`: UC_043..047 son responsabilidades
  de distinto módulo (assign_roles, configure_segments, etc.) — requieren revisión
  separada para mapping correcto a domain UCs. [PENDIENTE revisión]
- [ ] **T-007** `rbac-core/casos-uso.rst`: idem T-006. [PENDIENTE revisión]
- [x] **T-008** `mapeo-uc.rst`: `UC-043`→`UC_ADM_01` (3 ocurrencias + módulo → Admin).

## Bloque C — Normativa

- [x] **T-009** `tpl-uc-casos-de-uso.rst`: `UC_043_Configurar_SoD`→
  `UC_ADM_01_Gestionar_Ciclo_Vida_SoD`.

## Bloque D — UC specs completas para MOD_Admin

- [x] **T-010** `admin/uc-adm-01/`: crear 10 archivos faltantes de spec
  (actores-precondiciones, criterios-aceptacion, datos-involucrados,
  excepciones, flujo-principal, flujos-alternos, implementacion-tecnica,
  patrones-diseno, requisitos-no-funcionales, testing). Actualizar index.rst.
- [x] **T-011** `admin/uc-adm-02/`: idem 10 archivos.
- [x] **T-012** `admin/uc-adm-03/`: idem 10 archivos.

## Bloque E — Cierre

- [ ] **T-013** Commit y push.

---

## Orden de ejecución

```
T-001..T-005 (paralelo, bloques A) →
T-006..T-008 (paralelo, bloque B) →
T-009 (bloque C) →
T-010..T-012 (paralelo, bloque D) →
T-013
```
