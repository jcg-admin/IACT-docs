```yml
created_at: 2026-05-05 21:12:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 6 — PLAN
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Plan / Scope Statement — `use-case-view-uml07-standalone-pass`

## 1. Scope Statement

> Crear **83 archivos uml-07 standalone** en `source/arquitectura-tecnica/use-case-view/<module>/uc-XXX-NN-<slug>.rst`,
> con funciones RBAC como actores (P-15) y entidades del **domain-model canónico** como
> sistemas referenciados. Adicionalmente, **completar el domain-model con 16 archivos
> nuevos** (9 clases + 5 repos + 2 patterns) que son referenciados por al menos un UC.
> Actualizar los **13 module index files** con xref tables apuntando a los nuevos
> archivos. Build strict + audit script con 0 violaciones.

## 2. In-Scope (lo que SÍ se hace)

### 2.1 Domain-model nuevos (16 archivos)

**9 clases nuevas:**

- `domain-model/authorization-guard.rst`
- `domain-model/blacklisted-token.rst`
- `domain-model/internal-message.rst`
- `domain-model/pipeline-execution-repo.rst`
- `domain-model/metrics-cache.rst`
- `domain-model/idempotency-policy.rst`
- `domain-model/expiration-policy.rst`
- `domain-model/password-generator.rst`
- `domain-model/effective-permissions-aggregator.rst`

**5 repos canónicos:**

- `domain-model/user-repo.rst`
- `domain-model/function-repo.rst`
- `domain-model/function-group-repo.rst`
- `domain-model/separation-rule-repo.rst`
- `domain-model/access-group-repo.rst`

**2 patterns documentales:**

- `domain-model/specification-pattern.rst`
- `domain-model/strategy-pattern.rst`

### 2.2 Use-case-view standalone uml-07 (83 archivos)

| Módulo | Cantidad | Archivos |
|---|---|---|
| access | 7 | uc-acc-01..05, 08, 09 |
| admin | 3 | uc-adm-01..03 |
| alerts | 5 | uc-alr-01..05 |
| audit | 4 | uc-aud-01..04 |
| auth | 5 | uc-auth-01..05 |
| caller | 5 | uc-cli-01..05 |
| logs | 7 | uc-log-01..07 |
| operator | 10 | uc-opr-01..10 |
| permissions | 10 | uc-perm-01..10 |
| pipeline | 4 | uc-pip-01..04 |
| reports | 16 | uc-rpt-01..04, 07..17 + uc-inc-rpt-01 |
| supervision | 3 | uc-sup-01..03 |
| users | 4 | uc-usr-01..04 |
| **TOTAL** | **83** | |

### 2.3 Module index updates (13 archivos)

Actualizar `source/arquitectura-tecnica/use-case-view/<module>/index.rst` para apuntar
las xref tables a los nuevos archivos auto-explicativos en lugar de a `casos-uso/`.

### 2.4 Domain-model index update (1 archivo)

Actualizar `source/arquitectura-tecnica/domain-model/index.rst` toctree para incluir
los 16 archivos nuevos.

### 2.5 Audit script

Crear `scripts/validate-uml07-standalone.sh` que verifica:

- R-01: Actor iniciador izq, beneficiario der.
- R-02: stick figure + elipse.
- R-03: Rectangle MOD_X.
- R-04: línea asociativa sin estereotipo.
- R-06: `<<include>>` con `..>`.
- R-07: UC included nunca solo.
- R-08: `<<extend>>` con `..>` (ext → base).
- R-09: extension points en label del UC base.
- R-10: generalización con `--|>` (opcional).
- R-12: NO codenames como UC.
- BR-006: NO `<|--` entre actores.

## 3. Out-of-Scope (lo que NO se hace)

- ❌ Modificar `source/requisitos/casos-uso/` (uml-06 embebido). Insumo, no target.
- ❌ Refactor estructural de `domain-model/` (renombrar archivos existentes, mover
  bounded contexts).
- ❌ Crear clases adicionales que no estén en la lista cerrada de 14 (sin nuevo SP gate).
- ❌ Otros tipos de diagrama UML por UC (secuencia, actividad, estados).
- ❌ Sweep de vocabulario `view_etl_*` → `view_pipeline_*` en metadata de UC specs
  (TD-N2 del predecesor).
- ❌ Agregar métodos masivos a clases existentes — solo on-demand durante Phase 10.

## 4. Deliverables

| ID | Deliverable | Cantidad | Tipo |
|---|---|---|---|
| D-01 | Archivos `domain-model/` nuevos (clases + repos) | 14 | RST |
| D-02 | Archivos `domain-model/` patterns | 2 | RST |
| D-03 | Archivos `use-case-view/<mod>/uc-XXX-NN-<slug>.rst` | 83 | RST |
| D-04 | `domain-model/index.rst` actualizado | 1 | RST |
| D-05 | `use-case-view/<mod>/index.rst` actualizados | 13 | RST |
| D-06 | `scripts/validate-uml07-standalone.sh` | 1 | Shell |
| D-07 | Build strict log con 0 warnings | 1 | LOG |
| D-08 | Lessons learned + changelog del WP | 2 | MD |
| **Total archivos nuevos/modificados** | | **117** | |

## 5. Success criteria

| Criterio | Cómo se valida |
|---|---|
| Build strict 0 warnings | `sphinx-build -W` con log en WP build-logs/ |
| 83 archivos uml-07 standalone existen | `find use-case-view -name "uc-*-*.rst" \| wc -l = 83` |
| 16 archivos domain-model existen | `find domain-model -name "*.rst" \| wc -l = 67+16+1 = 84` (con index) |
| 13 module index actualizados | grep verifica xref a `uc-XXX-NN-` en cada index.rst |
| 0 violaciones audit | `validate-uml07-standalone.sh` exit 0 |
| Cobertura `:doc:` cross-refs ≥ 90% | reportar % en track/lessons-learned |

## 6. Schedule

Estimación de effort por etapa (estilo "ideal hours"):

| Etapa | Tasks | Effort |
|---|---|---|
| 1. domain-model (14 archivos) | T-001..T-014 | 4-6h |
| 2. patterns (2 archivos) | T-015, T-016 | 1h |
| 3. SP-02 PILOT (5 sample) | T-017..T-021 | 1-2h |
| 4. uml-07 masivo (78 archivos) | T-022..T-100 | 12-18h |
| 5. module index (13 archivos) | T-101..T-113 | 1-2h |
| 6. audit + final build | T-114, T-115 | 1h |
| **TOTAL** | **115 tasks** | **20-30h** |

Distribuible en sesiones por módulo. Commits checkpoint per módulo (Tim Pope style).

## 7. Stakeholders y gates

| Gate | Quién decide | Cuándo |
|---|---|---|
| **SP-02 PILOT** (post 5 sample) | Ejecutor | Tras T-021, antes de T-022 |
| **SP-03 BUILD por módulo** | Auto (CI strict) | Tras cada módulo (commit checkpoint) |
| **SP-04 final** | Ejecutor | Tras T-115, antes de cerrar WP |

## 8. Dependencias externas

- PR #14 abierta sobre `feature/cnst-033-uml-conformance` no requiere merge antes de
  arrancar Phase 10. El trabajo de este WP suma a esa misma rama.
- Cuando PR #14 se mergee a `feature/solve-problem-docs`, este WP también queda
  integrado en el mismo merge.

## 9. ROADMAP update

Pendiente: agregar entrada en `ROADMAP.md` raíz para este WP. Diferido a Phase 10
(se actualiza cuando se completa el WP).

## 10. Próximas fases

- Phase 7 DESIGN — concentrado en strategy (templates ya definidos en sección 3 del
  solution-strategy). No se requiere requirements-spec formal Given/When/Then porque
  el target es generación de docs (no comportamiento de software).
- Phase 8 PLAN EXECUTION — task plan con T-001..T-115.
- Phase 10 EXECUTE — ejecutar.
