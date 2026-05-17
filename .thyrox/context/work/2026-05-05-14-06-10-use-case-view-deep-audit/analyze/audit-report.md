```yml
created_at: 2026-05-05 14:10:00
project: IACT-docs
work_package: 2026-05-05-14-06-10-use-case-view-deep-audit
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Audit Report — Use Case View 7-layer Deep Audit

## Resumen ejecutivo

| Capa | Status | Evidencia |
|------|--------|-----------|
| L1 inventario casos-uso | ✓ | 13 módulos · 83 UCs |
| L2 inventario use-case-view | ✓ | 13 archivos uc-*.rst |
| L3 pureza tipo de diagrama | **✓ PASS** | 0 elementos prohibidos |
| L4 cobertura UCs | **⚠ 98.9%** | 1 UC faltante (UC_RPT_09) |
| L5 paridad módulos | **✓ PASS** | 13:13, nombres exactos |
| L6 cross-references | ✓ | 7 archivos con `:doc:` válidos |
| L7 relations `<<include>>` / `<<extend>>` | ✓ | xrefs a otros módulos válidos |

**Veredicto:** la vista está **estructuralmente correcta**
pero tiene **1 UC faltante** (`UC_RPT_09 Configurar Filtros`)
en `uc-reports.rst`. El issue es trivial — 1 línea por agregar.

----

## L1 — Inventario casos-uso (canon)

13 módulos · 83 UC dirs (sub-directorios `uc-*` que
representan casos de uso completos):

| Módulo | UCs | Identificadores |
|--------|-----|-----------------|
| access | 7 | UC_ACC_01..07 |
| admin | 3 | UC_ADM_01..03 |
| alerts | 5 | UC_ALR_01..05 |
| audit | 4 | UC_AUD_01..04 |
| auth | 5 | UC_AUTH_01..05 |
| caller | 5 | UC_CLI_01..05 |
| logs | 7 | UC_LOG_01..07 |
| operator | 10 | UC_OPR_01..10 |
| permissions | 10 | UC_PERM_01..10 |
| pipeline | 4 | UC_PIP_01..04 |
| reports | 16 | UC_INC_RPT_01, UC_RPT_01..17 (no 05/06) |
| supervision | 3 | UC_SUP_01..03 |
| users | 4 | UC_USR_01..04 |
| **TOTAL** | **83** | |

----

## L2 — Inventario use-case-view

13 archivos uc-*.rst (paridad 1:1 con módulos):

```
uc-access.rst, uc-admin.rst, uc-alerts.rst,
uc-audit.rst, uc-auth.rst, uc-caller.rst,
uc-logs.rst, uc-operator.rst, uc-permissions.rst,
uc-pipeline.rst, uc-reports.rst, uc-supervision.rst,
uc-users.rst
```

Plus `index.rst` (toctree de los 13).

----

## L3 — Pureza de tipo de diagrama (uml-07 only)

**Criterio:** un diagrama de caso de uso por uml-07 puede
contener solo:

- `actor` (con o sin estereotipo)
- `usecase`
- `rectangle` (system boundary)
- `package` (agrupamiento)
- `note`
- `left to right direction`, `skinparam`

**Prohibidos** (pertenecen a otros tipos UML):

- `class`, `abstract class` (uml-02 clases)
- `participant` (uml-09 secuencias)
- `component`, `interface`, `database`, `queue` (uml-12
  componentes)
- `control`, `entity`, `boundary` (uml-10 colaboraciones)
- `state` (uml-08 estados)
- `object` (diagrama de objetos)

**Resultado:** ✓ **PASS estricto** — los 13 archivos
contienen solo elementos uml-07. 0 elementos prohibidos.

----

## L4 — Cobertura de UCs

**Definición:** un UC del módulo M en casos-uso está
"cubierto" si su ID `UC_XXX_NN` aparece como `usecase`
dentro del rectangle `MOD_M` del diagrama
`use-case-view/uc-M.rst`.

| Módulo | UCs canon | en view | Missing | Cross-ref legítimo |
|--------|-----------|---------|---------|---------------------|
| access | 7 | 7 | — | — |
| admin | 3 | 3 | — | — |
| alerts | 5 | 5 | — | — |
| audit | 4 | 4 | — | — |
| auth | 5 | 6 | — | UC_PERM_08 (`<<include>>` válido) |
| caller | 5 | 5 | — | — |
| logs | 7 | 7 | — | — |
| operator | 10 | 10 | — | — |
| permissions | 10 | 10 | — | — |
| pipeline | 4 | 4 | — | — |
| **reports** | **16** | **15** | **UC_RPT_09** | — |
| supervision | 3 | 3 | — | — |
| users | 4 | 4 | — | — |

### Issue F-01 — UC_RPT_09 ausente en uc-reports.rst

**Severidad:** MAJOR (cobertura incompleta).
**UC ausente:** `UC_RPT_09 Configurar Filtros` (CRUD de
filtros guardados aplicables a UC_RPT_03).

**Causa raíz:** durante el rewrite del WP predecesor, el
diagrama heredó la lista de UCs del archivo v1, que ya
omitía el UC_RPT_09. El WP de rewrite NO validó cobertura
contra `casos-uso/reports/`.

**Lección:** el script de auditoría debió correrse al final
del WP predecesor antes de marcar como completo.

**Fix:** agregar `usecase "UC_RPT_09\nConfigurar Filtros"`
al rectangle `MOD_Reports` con la asociación al actor
`Operator` y la relación `<<extend>>` desde
`UC_RPT_03 Ver Reportes Historicos` (los filtros se
aplican sobre vistas históricas).

### Cross-reference legítimo F-02 (no es bug)

`UC_PERM_08 Generar Menu Dinamico` aparece en
`uc-auth.rst` como destino de `<<include>>` desde
`UC_AUTH_01`. NO es un UC del módulo Auth — pertenece a
Permissions — pero su inclusión es necesaria para mostrar
la dependencia. Este patrón (UC de otro módulo
referenciado vía `<<include>>` para clarity) es válido
por uml-07 (`inclusion.rst`).

----

## L5 — Paridad de módulos

13 módulos casos-uso ↔ 13 archivos use-case-view, nombres
exactos:

```
casos-uso = view = {access, admin, alerts, audit, auth,
                   caller, logs, operator, permissions,
                   pipeline, reports, supervision, users}
```

✓ **PASS** — sin missing, sin extras.

----

## L6 — Cross-references `:doc:`

7 archivos linkean a `use-case-view/uc-*`:

```
source/requisitos/casos-uso/admin/index.rst
source/requisitos/casos-uso/admin/uc-adm-01/informacion-general.rst
source/requisitos/casos-uso/admin/uc-adm-02/informacion-general.rst
source/requisitos/casos-uso/admin/uc-adm-03/informacion-general.rst
source/arquitectura-tecnica/diagramas-uc-por-modulo.rst (toctree)
source/arquitectura-tecnica/design-view/seq-caller.rst
source/arquitectura-tecnica/implementation-view/impl-caller.rst
```

Los nombres de archivo (`uc-access.rst`, etc.) no
cambiaron en el rewrite, así que **todos los `:doc:`
siguen siendo válidos**. ✓ **PASS**.

----

## L7 — Relations `<<include>>` / `<<extend>>`

Verificación de que cada relación apunta a un UC
existente:

- `<<include>>` desde UCs operativos a UC_INC_RPT_01 en
  uc-reports: el UC incluido existe. ✓
- `<<include>>` UC_AUTH_01 → UC_PERM_08: cross-module
  legítimo (F-02). ✓
- `<<include>>` UC_PERM_08 → UC_PERM_07 en uc-permissions:
  ambos en mismo módulo. ✓
- `<<extend>>` UC_RPT_03 → UC_RPT_04 / UC_RPT_07: ambos
  presentes. ✓
- `<<include>>` write-side audit en uc-permissions: target
  UC_PERM_09 presente. ✓
- `<<extend>>` UC_OPR_02 ← UC_OPR_04/05/06: targets
  presentes. ✓
- `<<extend>>` UC_CLI_02 → UC_CLI_03 → UC_CLI_04: cadena
  válida en uc-caller. ✓

✓ **PASS** — todas las relaciones referencian UCs
existentes.

----

## Plan de remediación

| ID | Acción | Severidad | Archivo |
|----|--------|-----------|---------|
| F-01 | Agregar `UC_RPT_09 Configurar Filtros` al diagrama de uc-reports.rst con relación `<<extend>>` desde UC_RPT_03 | MAJOR | uc-reports.rst |

Una vez aplicado F-01: re-ejecutar el script de auditoría
para confirmar 100% cobertura → cerrar WP.
