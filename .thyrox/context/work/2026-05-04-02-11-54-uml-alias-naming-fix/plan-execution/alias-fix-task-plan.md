```yml
created_at: 2026-05-04 02:16:24
project: IACT-docs
work_package: 2026-05-04-02-11-54-uml-alias-naming-fix
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En progreso
```

# Task Plan — UML Alias Naming Fix

Corregir todos los aliases PlantUML crípticos conforme D-ALIAS-001..003 y STD_011.

---

## Bloque A — Normativa y WP setup

- [x] **T-001** Crear `std-011-alias-diagramas-uml.rst` con D-ALIAS-001..003
  - Commit: "Add STD_011 alias naming standard for PlantUML diagrams"

- [x] **T-002** Agregar STD_011 al toctree de `normativa/estandares/index.rst`
  - Commit incluido en T-001

- [x] **T-003** Crear WP discover artifacts (analysis + decisions)
  - Commit: incluido en T-001

---

## Bloque B — diagramas-uml-sistema.rst (prioridad alta)

- [x] **T-004** Corregir 13 aliases en `source/arquitectura-tecnica/diagramas-uml-sistema.rst`

  Tabla de correcciones:

  | Violación | Corrección | Regla |
  |-----------|------------|-------|
  | `as RVG` | `as view_reports` | D-ALIAS-002 |
  | `as QSG` | `as view_pipeline_status` | D-ALIAS-002 |
  | `as PAG` | `as request_pipeline_retry` | D-ALIAS-002 |
  | `as UAG` | `as assign_functions` | D-ALIAS-002 |
  | `as AUG` | `as view_audit_log` | D-ALIAS-002 |
  | `as SCH` | `as APScheduler` | D-ALIAS-003 |
  | `as USR` (actor) | `as view_reports` | D-ALIAS-002 |
  | `as AE` | `as AuthEndpoint` | D-ALIAS-003 |
  | `as DE` | `as DashboardEndpoint` | D-ALIAS-003 |
  | `as SR` | `as SegmentResolver` | D-ALIAS-003 |
  | `as SRP` | `as ServicioReportes` | D-ALIAS-003 |
  | `as FAIL` | `as AutenticacionFallida` | D-ALIAS-001 |
  | `as USR` (object) | `as UserRBAC` | D-ALIAS-003 |

  Importante: también actualizar referencias en flechas (→) y activate/deactivate
  - Commit: "Fix cryptic aliases in diagramas-uml-sistema.rst"

---

## Bloque C — diagramas-uc-por-modulo.rst

- [x] **T-005** Auditar y corregir aliases en
  `source/arquitectura-tecnica/diagramas-uc-por-modulo.rst`
  - Archivo convertido a index/toctree — sin PlantUML directo. Sin violaciones.

---

## Bloque D — UC diagramas-uml.rst sweep (~80 archivos)

- [x] **T-006** Sweep de aliases en `source/requisitos/casos-uso/**/diagramas-uml/`
  - Nota: archivos fueron divididos en `diagramas-uml/` subdirectorios (1 diagrama por archivo)
  - 41 archivos corregidos: EMI→AuditEmitter, NOT→NotificacionMailbox, INS→RegistrarDatos,
    CSE→CerrarSesiones, LST→VistaListado, BLK→TokensRevocados, y 30+ otros
  - 0 violaciones restantes globalmente

---

## Bloque E — Módulos arquitectura diagramas.rst

- [x] **T-007** Revisar `source/arquitectura-tecnica/modulos/**/diagramas/`
  - Nota: archivos divididos en `diagramas/` subdirectorios (1 diagrama por archivo)
  - 7 archivos corregidos: IVR→SistemaIVR, SUP→SupervisorSistema, ANA→AnalistaReportes,
    SCH→DisparadorScheduler, ETL→ProcesoETL, INC→ResolverSegmento

---

## Bloque F — Validación final

- [x] **T-008** Ejecutar validación grep del STD_011

  ```bash
  grep -rn " as [A-Z][A-Z]\?$\| as [a-z][a-z]\?$" \
    source/ \
    --include="*.rst" | grep -v "base-cognitiva"
  ```

  Resultado esperado: vacío (0 violaciones)

- [ ] **T-009** Ejecutar `make html SPHINXOPTS="-j1"` y verificar 0 errores [GATE — pendiente autorización]
  - Commit changelog con resultado

---

## Orden de ejecución

```
A (done) → B (T-004) → C (T-005) → D (T-006) → E (T-007) → F (T-008, T-009)
```

Cada bloque = 1 commit. Push después de cada bloque.
