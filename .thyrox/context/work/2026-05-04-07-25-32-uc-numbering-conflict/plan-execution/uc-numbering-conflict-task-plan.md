```yml
created_at: 2026-05-04 07:25:32
project: IACT-docs
work_package: 2026-05-04-07-25-32-uc-numbering-conflict
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecucion
```

# Task Plan — UC-043..047 Numbering Conflict

Renumerar los 5 UCs phantom de Access/SoD del rango 043-047 al rango
libre 078-082. Los UCs de reports conservan sus números.

Mapa de sustitución:
- UC-043 (Configurar SoD)              → UC-078
- UC-044 (Consultar Permisos Efectivos) → UC-079
- UC-045 (Gestionar Catalogo AGR)       → UC-080
- UC-046 (Gestionar Catalogo Funciones) → UC-081
- UC-047 (Auditar Cambios de Permisos)  → UC-082

Archivos afectados (14 archivos, ~35 ocurrencias):

---

## Bloque A — Reglas de negocio

- [x] **T-001** `br-006-rbac-flat-nist.rst`: UC-044→UC-079, UC-045→UC-080,
  UC-046→UC-081 en §5.3.
- [ ] **T-002** `br-007-separacion-funciones-sod.rst`: UC-043→UC-078 en
  §3.2 y §5.3; UC-044→UC-079 en §5.3.

## Bloque B — Requisitos funcionales

- [ ] **T-003** `fr-010-02-validar-sod-antes-asignar.rst`: UC_043→UC_078
  (2 ocurrencias).

## Bloque C — Base cognitiva

- [ ] **T-004** `fnd-03-casos-de-uso.rst`: UC-043→UC-078, UC-044→UC-079,
  UC-045→UC-080, UC-046→UC-081, UC-047→UC-082 (todas las ocurrencias
  como UCs de SoD/acceso — NO tocar las de reports UC-043..047).
- [ ] **T-005** `fnd-04-trazabilidad.rst`: ídem + actualizar etiqueta
  `.. _uc-043:` → `.. _uc-078:` y `:artefacto: UC_043` → `UC_078`.
- [ ] **T-006** `fnd-05-jerarquia-4-niveles.rst`: UC-043→UC-078,
  UC-044→UC-079, UC-047→UC-082 (todas las ocurrencias SoD).
- [ ] **T-007** `txm-01-taxonomia-requisitos.rst`: actualizar referencia
  UC-043 en lista de UC de access.

## Bloque D — Arquitectura técnica

- [ ] **T-008** `rbac-core/responsabilidades.rst`: UC_043→UC_078.
- [ ] **T-009** `rbac-core/casos-uso.rst`: UC_043→UC_078.
- [ ] **T-010** `mapeo-uc.rst`: UC-043→UC-078 (3 ocurrencias).
- [ ] **T-011** `catalogo-funciones.rst`: UC-043→UC-078 (3 ocurrencias).

## Bloque E — Normativa

- [ ] **T-012** `tpl-uc-casos-de-uso.rst`: UC_043_Configurar_SoD→
  UC_078_Configurar_SoD.

## Bloque F — Cierre

- [ ] **T-013** Commit y push.

---

## Orden de ejecución

```
T-001 → T-002 → T-003 (paralelo con T-004..T-007) → T-008..T-012 → T-013
```
