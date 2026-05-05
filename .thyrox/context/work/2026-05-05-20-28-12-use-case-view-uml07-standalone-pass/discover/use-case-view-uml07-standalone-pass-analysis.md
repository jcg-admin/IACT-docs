```yml
created_at: 2026-05-05 20:28:12
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Borrador
```

# DISCOVER — `use-case-view-uml07-standalone-pass`

## 1. Lo que se espera (Target del WP)

**Construir 83 archivos de diagrama de caso de uso UML-07 standalone**, uno por cada UC
del sistema IACT, en la siguiente ubicación canónica:

```
source/arquitectura-tecnica/use-case-view/<module>/uc-XXX-NN-<slug>.rst
```

### Visualización del estado esperado

```
ANTES (estado actual, post WP previo):
  source/arquitectura-tecnica/use-case-view/access/
    └── index.rst    ← solo el índice del módulo

DESPUÉS (target):
  source/arquitectura-tecnica/use-case-view/access/
    ├── index.rst                                       ← actualizado: xref a los 7 nuevos
    ├── uc-acc-01-asignar-funciones.rst                 ← NUEVO
    ├── uc-acc-02-revocar-funciones.rst                 ← NUEVO
    ├── uc-acc-03-consultar-permisos-efectivos.rst      ← NUEVO
    ├── uc-acc-04-asignar-agrupador.rst                 ← NUEVO
    ├── uc-acc-05-...rst                                ← NUEVO
    ├── uc-acc-08-...rst                                ← NUEVO
    └── uc-acc-09-...rst                                ← NUEVO
```

Repetido para los 13 módulos: `access` (7), `auth` (5), `users` (4), `permissions` (10),
`reports` (16), `admin` (3), `alerts` (5), `audit` (4), `caller` (5), `logs` (7),
`operator` (10), `pipeline` (4), `supervision` (3) = **83 archivos totales**.

### Cada archivo `uc-XXX-NN-<slug>.rst` contiene

1. **Título auto-explicativo** que matchea el nombre del archivo.
2. **Bloque `@startuml`/`@enduml`** conforme a uml-07 (refs `source/base-cognitiva/_uml/uml-07-*`):
   - `left to right direction`
   - **Actores = funciones RBAC** (P-15 granular, **igual que uml-06** del predecesor —
     coherencia con sistema RBAC). Stereotypes:
     - `<<beneficiario>>` para funciones que reciben del UC (R-01 uml-07).
     - `<<sistema>>` para entidades del **domain-model canónico** (servicios, repos,
       engines) — usar **nombre exacto del archivo** del domain-model.
     - `<<externo>>` para Caller (no autenticado).
   - **Rectangle `MOD_<Module>`** con UC principal + sub-usecases necesarios.
   - **Relaciones uml-07**:
     - `-->` línea asociativa (actor ↔ UC).
     - `..>` con `<<include>>` (uml-07 inclusion).
     - `..>` con `<<extend>>` (uml-07 extension, ext → base, con extension point en label del base).
     - `--|>` generalización entre UCs (R-10, opcional).
   - **Extension points** declarados en label del UC base donde aplique (R-09).
   - **Notas** referenciando BR-NN, CNST-NN, P-NN, ADR-NN.
   - **NO `<|--` entre actores** (BR-006 Flat NIST).
3. **Sección `.. seealso::`** con `:doc:` cross-refs a:
   - **Domain-model entities** referenciadas como actores `<<sistema>>` —
     debe existir el archivo en `source/arquitectura-tecnica/domain-model/<entity>.rst`.
     Si no existe, **se crea como parte de este WP** (ver scope ampliado abajo).
   - UC backing si es vista alternativa (e.g. UC_PERM_01 → UC_ACC_04).
   - Spec textual del UC (`/requisitos/casos-uso/<mod>/<uc>/index`).

### Plus: 13 module index actualizados

Cada `use-case-view/<module>/index.rst` actualiza su tabla de cross-references para apuntar
a los nuevos archivos auto-explicativos en lugar de a `casos-uso/`.

## 2. Análisis previo heredado (WP `use-case-view-uml07-rebuild`)

### 2.1 Inventario completo (83 UCs)

| Módulo | UCs | Con uml-06 base | Notas |
|--------|-----|-----------------|-------|
| access | 7 | 7 | uc-acc-01..05, 08, 09 |
| admin | 3 | 3 | uc-adm-01..03 |
| alerts | 5 | 5 | uc-alr-01..05 |
| audit | 4 | 4 | uc-aud-01..04 |
| auth | 5 | 5 | uc-auth-01..05 |
| caller | 5 | 5 | uc-cli-01..05 |
| logs | 7 | 7 | uc-log-01..07 |
| operator | 10 | 10 | uc-opr-01..10 |
| permissions | 10 | 10 | uc-perm-01..10 |
| pipeline | 4 | 4 | uc-pip-01..04 |
| reports | 16 | 16 | uc-rpt-01..04, 07..17 + uc-inc-rpt-01 |
| supervision | 3 | 3 | uc-sup-01..03 |
| users | 4 | 4 | uc-usr-01..04 |
| **TOTAL** | **83** | **83** | Todos con base uml-06 |

Inventario machine-readable: `discover/inventory.json` (heredado del predecesor con shape:
`{module, uc_dir, title, short, slug, target, src_diagram}`).

### 2.2 Trabajo del predecesor que sirve de insumo

El WP `use-case-view-uml07-rebuild` no completó el target de uml-07 standalone, pero
**produjo 53 nuevos archivos uml-06 embebidos** que ahora sirven de base para este WP:

| Archivo predecesor | Aporta a este WP |
|---|---|
| `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` (53 nuevos + 30 pre-existentes = 83 totales) | Modelo base de actores, includes, extends, notas — para sanitizar y promover a uml-07 standalone |
| Cross-refs `:doc:` a domain-model en los 53 nuevos | Mapping UC → entidades canónicas ya identificado (≈250 refs) |
| `discover/inventory.json` | Inventario de 83 UCs con paths target |
| 5 build logs en formato ISO 8601 | Baseline para validar 0-warning state |
| `.claude/rules/build-logs.md` | Convención ISO 8601 obligatoria |
| `.claude/rules/git-flow.md` | Política de branching para este WP |

### 2.3 Lecciones del predecesor (L-01..L-07)

Heredadas como guías de proceso para evitar repetir errores. Detalle en `wp-state.md`
sección "Flow + lecciones heredadas del predecesor".

### 2.5 Convenciones uml-07 leídas en `source/base-cognitiva/_uml/uml-07-*`

El módulo `uml-07-diagramas-casos-uso` del proyecto (referencia adaptada de "Aprendiendo
UML en 24 horas" — Hora 7) define las convenciones canónicas:

| Lección | Convención clave |
|---|---|
| `representacion-de-un-modelo-de-caso-de-uso` | Actor (stick figure) izquierda inicia, derecha recibe. UC = elipse. Sistema = rectángulo. Línea asociativa entre actor y UC. |
| `inclusion` | `..>` con `<<include>>` apuntando del caso de uso base al UC incluido. UC incluido nunca aparece solo. |
| `extension` | `..>` con `<<extend>>` apuntando del UC extensor al UC base. Extension points declarados en label del UC base. |
| `generalizacion` | `--\|>` línea continua con triángulo sin rellenar (como herencia de clases). Aplica a UCs Y a actores. |
| `comprension-del-dominio` | Análisis del dominio precede a la elaboración de UCs. |
| `comprension-de-los-usuarios` | Identificar tipos de usuarios (en IACT: funciones RBAC granulares — P-15). |
| `comprension-de-los-casos-de-uso` | UCs son lo que el sistema hace para el actor; no detalles de implementación. |

**Restricciones IACT que sobrescriben uml-07 puro:**

- BR-006 (NIST RBAC Flat) prohibe la generalización entre actores que uml-07 sí permite
  (`<\|--`). Los diagramas no usarán esa relación entre actores. Sí entre UCs (R-10).
- Los actores son **funciones RBAC** (P-15 granular), no roles agregados — coherente con
  el modelo de assignments del sistema.

### 2.4 Diferencias claves con el predecesor

| Aspecto | Predecesor (uml-06 embebido) | Este WP (uml-07 standalone) |
|---|---|---|
| Ubicación | `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` | `use-case-view/<mod>/uc-XXX-NN-<slug>.rst` |
| Reference UML | uml-06 (introducción) | **uml-07 (diagramas)** |
| Naturaleza | Embebido en spec textual del UC (12 partes) | Standalone, vista arquitectónica |
| Actores | Funciones RBAC (P-15 granular) | **Funciones RBAC (mismo P-15)** — coherencia |
| Naming | `diagrama-de-caso-de-uso.rst` (mismo en cada UC) | `uc-XXX-NN-<slug>.rst` (auto-explicativo) |
| Extends | Mínimos (los del flujo principal) | Enriquecidos con `flujos-alternos` + `excepciones` |
| Notas BR/CNST | Las del flujo principal | Exhaustivas (incluyen `criterios-aceptacion`) |
| Sistemas como actores | Mezcla (algunos canónicos, algunos inventados) | **Solo nombres exactos de domain-model** |
| Domain-model gaps | Detectados pero diferidos | **Completados como parte del WP** |

## 3. Naturaleza del trabajo

Es **trabajo analítico**, no scripted puro. Cada archivo requiere:

1. **Lectura del spec textual** del UC (5 archivos por UC: informacion-general, actores-
   precondiciones, flujo-principal, flujos-alternos, excepciones, criterios-aceptacion).
2. **Lectura del uml-06 base** (`casos-uso/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst`)
   como punto de partida.
3. **Sanitización** función RBAC → rol canónico.
4. **Enriquecimiento** con extends de flujos alternos.
5. **Cross-references** a domain-model + UC backing + spec.
6. **Validación** sintaxis PlantUML + R-01..R-12 + BR-006.

**Tiempo estimado por UC**: 15-30 min (más rápido que el plan original de 30 min porque
hay base uml-06; más lento que el shallow del predecesor de 2-3 min porque hay que leer
flujos-alternos y excepciones).

**Tiempo total estimado**: 21-42 horas para 83 UCs. Distribuido en sesiones por módulo.

## 4. Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | uml-06 base "shallow" del predecesor (extends incompletos) | Alta | Medio | Releer flujos-alternos + excepciones para enriquecer |
| R-02 | Mapping función → rol con casos ambiguos | Media | Bajo | Tabla canónica en wp-state.md; documentar excepciones en decisions-log |
| R-03 | 83 archivos × revisión = mucho effort | Alta | Alto | Generación por lotes módulo; SP-02 valida pattern con 5 sample antes de propagar |
| R-04 | Drift de scope (repetir error del predecesor) | Media | Crítico | L-01: re-leer wp-state.md::target en cada Phase; auditoría que NO se tocan casos-uso/ |
| R-05 | Conflictos con PR #14 sin merge | Baja | Medio | Esperar merge a feature/solve-problem-docs antes de bifurcar nueva rama |
| R-06 | Build break cuando se actualizan 13 module index para apuntar a los 83 nuevos | Media | Alto | Generar 83 archivos PRIMERO, después actualizar index files (orden importa) |

## 5. Stakeholders

- **Ejecutor (NestorMonroy)**: aprueba bootstrap, sample (5 UCs), pattern, y final.
- **Reviewers humanos**: revisan los 83 archivos en chunks por módulo (estimado 1-2h
  por módulo de revisión).
- **CI**: valida build strict 0 warnings, prerender PlantUML 0 errors,
  validate-plantuml.sh 0 issues.
- **Dependientes downstream**: los `casos-uso/` modules que vinculan a use-case-view via
  `:seealso:` se mantendrán (no requieren cambio).

## 6. Quality goals

| Goal | Métrica | Target |
|---|---|---|
| **Cobertura** | UCs con archivo standalone / 83 | 83/83 |
| **Conformidad uml-07** | Violaciones R-01..R-12 detectadas por audit script | 0 |
| **Conformidad BR-006** | `<\|--` entre actores en archivos standalone | 0 |
| **Build limpio** | Warnings de strict build sphinx-build -W | 0 nuevos |
| **PlantUML render** | Errors de prerender | 0 |
| **Cross-refs válidos** | `:doc:` rotos a domain-model o spec | 0 |
| **Vocabulario CNST-033** | Funciones RBAC apareciendo como ACTORES (no en notas) | 0 |
| **Naming auto-explicativo** | Archivos sin slug descriptivo | 0 |

## 7. Constraints

### Técnicas

- **Sphinx 8.2.3** + sphinxcontrib-plantuml.
- **PlantUML JAR** (pre-rendered SVG strategy via Alt-A — heredado).
- **build-logs ISO 8601** obligatorio.
- **tim-pope commit style** con scope `(use-case-view)`.

### De negocio

- **CNST-033** — vocabulario unificado RBAC.
- **BR-006** — RBAC Flat NIST (no jerarquía actores).
- **CNST-005** — SoD evaluado sobre funciones, no AGRs.
- **BR-009** — bajas lógicas (ningún DELETE).
- **CNST-008** — segment isolation.
- **CNST-026** — sin PII en logs/exports.

### De plataforma

- **Branch protection** en `feature/solve-problem-docs` y `develop`.
- **PR-based integration** per `.claude/rules/git-flow.md`.
- **`.claude/rules/build-logs.md`** — logs en WP activo, ISO 8601.

## 8. Scope ampliado — Domain-model completion (NUEVO vs predecesor)

A diferencia del predecesor que diferia los gaps de domain-model a WPs futuros, este
WP **completa** los gaps detectados durante la generación de los 83 archivos uml-07.

### 8.1 Lo que SE INCLUYE en scope

- ✅ **Crear clases faltantes** en `source/arquitectura-tecnica/domain-model/`. Estimación
  inicial heredada del predecesor (Q3): ~18 clases. Top esperado:

  | Clase | UCs que la referencian | Bounded context |
  |---|---|---|
  | `AuthorizationGuard` | 53 UCs | RBAC |
  | `AuthenticationGuard` | 16 | Auth |
  | `ThrottlePolicy` | 16 | Cross-cutting |
  | `TransactionManager` | 16 | Cross-cutting |
  | `InternalMessage` | 14 | Mailbox |
  | `UserRepo` | 11 | RBAC |
  | `MetricsCache` | 11 | Cross-cutting |
  | `AccessService` | 10 | RBAC |
  | (otras ~10) | varios | varios |

- ✅ **Agregar métodos faltantes** a clases existentes. Estimación heredada (Q4): ~30
  métodos. Ejemplos:

  | Clase | Métodos faltantes |
  |---|---|
  | `PermissionService` | `check_bulk_with_cache`, `warm_user_cache`, `invalidate_for_function` |
  | `AssignmentRepo` | `find_by_function_id`, `count_active_globally` |
  | `AuditService` | `emit_async`, `flush_pending` |
  | `Session` | `rotate_token`, `mark_compromised` |
  | `User` | `record_login_attempt`, `increment_failed_attempts` |

- ✅ **Audit de naming canonico**: 7 variants identificados por predecesor
  (`AssignmentRepository` → `AssignmentRepo`, etc.) — corregir refs en los 83 uml-07.

- ✅ **Análisis Phase 3 dedicado**: `analyze/domain-model-completion-analysis.md` con
  inventory machine-readable de los gaps detectados al leer los 83 specs.

### 8.2 Lo que SIGUE OUT-of-scope

- ❌ Modificar `source/requisitos/casos-uso/` (uml-06 embebido en specs textuales). Esos
  son insumo, no target.
- ❌ Sweep de vocabulario `view_etl_*` → `view_pipeline_*` en metadata de UC specs
  (TD-N2 del predecesor) — WP futuro `casos-uso-cnst-033-vocabulary-cleanup-pass`.
- ❌ Otros tipos de diagrama UML por UC (secuencia, actividad, estados) — solo el
  diagrama de caso de uso uml-07.
- ❌ Refactor estructural de `domain-model/` (renombrar archivos, mover bounded contexts,
  etc.) — solo creación de clases faltantes y métodos faltantes referenciados por UCs.

## 9. Próximos pasos (Phase 1 → Phase 5)

### Phase 1 DISCOVER (en curso)

- [x] Bootstrap WP directory.
- [x] `wp-state.md` con target + insumos + lecciones heredadas.
- [x] `discover/{wp}-analysis.md` (este documento).
- [ ] Copiar `inventory.json` del predecesor.
- [ ] Crear `risk-register.md`.
- [ ] **SP-01**: ejecutor responde 5 preguntas pendientes y aprueba bootstrap.

### Phase 3 ANALYZE (próxima)

- [ ] `analyze/role-mapping-deep-analysis.md` — validar tabla función RBAC → rol con
  casos por módulo, identificar ambigüedades.

### Phase 5 STRATEGY

- [ ] `strategy/{wp}-solution-strategy.md` — Key Ideas, alternativas evaluadas,
  decisión final del template + pipeline de generación.

### Phase 7 DESIGN/SPECIFY

- [ ] `design/{wp}-requirements-spec.md` con Given/When/Then.
- [ ] `design/template-uc-standalone.md` — plantilla canónica.

### Phase 8 PLAN EXECUTION

- [ ] `plan-execution/{wp}-task-plan.md` con T-001..T-NNN (1 task por UC + 1 task
  por module index update + tasks de validación).

### Phase 9 PILOT/VALIDATE

- [ ] 5 sample UCs (admin, operator, reports, supervision, caller — uno por familia
  semántica).
- [ ] **SP-02**: ejecutor valida pattern.

### Phase 10 EXECUTE

- [ ] Generación masiva por módulo (10 commits checkpoint).
- [ ] **SP-03 por módulo**: build strict + audit script.

### Phase 11 + 12 → cierre.

## 10. Decisiones tomadas (resueltas) y pendientes

### Resueltas por el ejecutor

1. **Naming**: ✅ formato `uc-XXX-NN-<slug-descriptivo>.rst` (kebab-case castellano).
2. **Actores**: ✅ funciones RBAC (P-15), NO roles. Coherente con uml-06 predecesor y
   con sistema RBAC granular del proyecto.
3. **Granularidad**: ✅ por módulos con SP-02 sample + SP-03 build incremental.
4. **Rama**: ✅ `feature/cnst-033-uml-conformance` (la actual del PR #14, pre-merge).
5. **Domain-model completion**: ✅ INCLUIDO en scope (no diferido a WP futuro).
6. **uml-07 conventions**: ✅ basadas en `source/base-cognitiva/_uml/uml-07-*` lecciones
   1.0.0 (representacion-de-un-modelo, inclusion, extension, generalizacion, etc.).

### Pendientes para SP-01

- ¿`status: Vigente v1.0.0` o `status: Borrador v0.9` para los 83 archivos iniciales?
- ¿Aprobar el plan completo y avanzar a Phase 3 ANALYZE?
