```yml
created_at: 2026-05-07 07:30:00
project: IACT-docs
work_package: 2026-05-07-04-50-49-std-012-prefix-normalization
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — STD-012 v1.1.0 Prefix Normalization

> Consolidacion del WP en formato Keep a Changelog.
> Inicio: 2026-05-07 04:50. Cierre: 2026-05-07 07:30.

## [1.0.0] — 2026-05-07 (cierre del WP)

### Changed (normativo)

- ``source/normativa/estandares/std-012-tipos-de-diagramas-uml.rst``
  v1.0.0 → v1.1.0:

  - Tabla maestra §3.1: nombres canonicos con prefijo
    ``diagrama-de-`` para todos los tipos.
  - Nueva seccion §7 "Convencion de nomenclatura de
    archivos" formalizando el prefijo obligatorio +
    excepcion para archivos auxiliares de texto sin
    ``@startuml``.
  - Historial §9: entrada 1.1.0 con razon (alineamiento
    con STD-011 + practica reciente).

### Changed (estado de UCs)

- 18 UCs reclasificados de ``Vigente``/``Reservado`` a
  ``Fuera del scope``:

  - caller (5): uc-cli-01..05.
  - operator (10): uc-opr-01..10.
  - supervision (3): uc-sup-01..03.

- 3 cluster index.rst actualizados con warning de
  out-of-scope:

  - caller/index.rst v1.1.0.
  - operator/index.rst v1.2.0.
  - supervision/index.rst v1.2.0.

### Removed (legacy)

**31 archivos ``caso-de-uso.rst`` legacy eliminados** (con
canonical existente en mismo dir):

- admin (3): uc-adm-01/02/03.
- alerts (5): uc-alr-01..05.
- audit (4): uc-aud-01..04.
- logs (7): uc-log-01..07.
- pipeline (4): uc-pip-01..04.
- reports (8): uc-rpt-10..17 + uc-inc-rpt-01.

(NO se eliminaron los 18 caso-de-uso.rst de
caller/operator/supervision — out-of-scope, preservados
en backup).

### Renamed/Recreated

**93 archivos legacy recreados a nombres canonicos**
``diagrama-de-X.rst``:

**Cluster access (1):**

- uc-acc-04: diagrama-agr-como-agregacion →
  diagrama-de-agr-como-agregacion (recreate con
  UserAccessGroupAssignment + FunctionGroupMembership +
  Function.is_critical).

**Cluster admin (5 UCs, 9 archivos):**

- uc-adm-01 (3): diagrama-de-actividad,
  diagrama-de-estados-sod-rule, recreate
  diagrama-de-caso-de-uso (aliases STD-011).
- uc-adm-02 (3): diagrama-de-actividad,
  diagrama-de-estados-funcion, recreate
  diagrama-de-caso-de-uso.
- uc-adm-03 (3): diagrama-de-actividad,
  diagrama-de-impacto, recreate
  diagrama-de-caso-de-uso.

**Cluster alerts (5 UCs, 20 archivos):**

- uc-alr-01..05: actividad/secuencia/clases/estados-X.rst
  → diagrama-de-actividad/secuencia/clases/estados-X.rst.

**Cluster audit (4 UCs, 16 archivos):**

- uc-aud-01..04: actividad/secuencia/clases/estados/
  componentes/flujo-firma/verify legacy → canonicos
  diagrama-de-*.

**Cluster logs (7 UCs, 26 archivos):**

- uc-log-01..07: actividad/secuencia/pipeline/clases/
  componentes/estado/tail/etc legacy → canonicos
  diagrama-de-*.

**Cluster permissions (2 UCs, 2 archivos):**

- uc-perm-04: estados-exceptionalpermission →
  diagrama-de-estados-exceptionalpermission.
- uc-perm-05: estados-accessgroup →
  diagrama-de-estados-accessgroup.

**Cluster pipeline (4 UCs, 16 archivos):**

- uc-pip-01..04: actividad/secuencia/clases/componentes/
  estados-X legacy → canonicos diagrama-de-*.

**Cluster reports (9 UCs, 34 archivos):**

- uc-inc-rpt-01 (3): actividad,
  caso-de-uso-relacion-de-inclusion, clases.
- uc-rpt-10..17 (31): actividad/secuencia/clases/estados-X/
  distribucion/flujo-anonimizacion legacy → canonicos.

### Excluded (auxiliary, no diagram)

- ``auth/uc-auth-01/diagramas-uml/notas-sobre-los-diagramas.rst``
  preservado (texto sin ``@startuml``, excepcion STD-012
  §7.3).

- ``logs/uc-log-07/diagramas-uml/tail-sse.rst`` eliminado
  (era texto auxiliar referenciando UC_LOG_01 SSE).

### Excluded (out-of-scope)

70 archivos legacy en caller/operator/supervision NO
procesados — clusters fuera del scope del proyecto.
Archivos preservados intactos en source/ (sin canonicos
adicionales) + backup completo en WP.

### Added (backup)

- ``backup/`` en el WP: 195 archivos legacy preservados
  con estructura ``{cluster}/{uc}/diagramas-uml/{file}``.
  Disponibles para consulta en caso de duda durante
  revisiones futuras.

### Added (build logs)

- ``track/build-logs/``: 8+ logs de builds intermedios
  + build serial final post-make-clean.

### Cleaned

- ``source/_generated_diagrams/``: 1198 SVGs de cache
  eliminados. Cache regenerado automaticamente en
  proximos builds.

- ``source/_ext/plantuml_cached.py``: verificado
  funcional (extension de Sphinx para cache PlantUML).

## Verification

- Build incremental sphinx strict EXIT=0, 0 warnings
  tras cada commit por cluster.
- Build clean serial post-cierre EXIT=0 (run en
  background al cierre del WP).
- 0 archivos legacy in-scope restantes (excepto 1
  auxiliar de texto en uc-auth-01).
- 0 cross-refs rotos.
- STD-010 vocabulario canonico aplicado en todos los
  diagramas recreados.
- STD-011 aliases auto-documentados en todos los
  diagramas recreados.
- STD-012 v1.1.0 nomenclatura aplicada universalmente.

## Commits del WP

1. ``09064784`` — STD-012 v1.1.0 normativo.
2. ``8cc0598e`` — Backup completo 195 archivos.
3. ``a2b7da02`` — OPR/SUP/CLI → Fuera del scope.
4. ``b057b049`` — uc-acc-04.
5. ``51faefdf`` — uc-adm-01.
6. ``9adc09b4`` — uc-adm-02 + uc-adm-03.
7. ``94718a8a`` — cluster alerts.
8. ``db14a343`` — cluster audit.
9. ``4b93e9f0`` — cluster permissions.
10. ``9d52876d`` — cluster pipeline.
11. ``5de43294`` — cluster logs.
12. ``7e4a6463`` — cluster reports.
13. ``3ebebeab`` — cleanup _generated_diagrams.
14. (este commit) — closure: changelog + lessons + wp-state.

**Total: 14 commits.**
