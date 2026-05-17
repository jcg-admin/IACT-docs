```yml
created_at: 2026-05-05 21:56:47
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Borrador
```

# DISCOVER — Functional Decomposition Antipattern Audit

## 1. Lo que se espera

Auditar el **modelo de dominio** (`domain-model/*` + `use-case-view/*/uc-XXX-NN-*.rst`)
del proyecto IACT contra el antipatron **Functional Decomposition** documentado por
William Brown en *AntiPatterns* (1998), produciendo:

1. **Reporte por archivo** con veredicto OK / Revision / Antipatron.
2. **Resumen agregado** con metricas y patrones recurrentes.
3. **Lista de hallazgos confirmados** (si los hay) para WP de remediacion separado.

## 2. Definicion del antipatron

Brown describe el antipatron como **"estructurar un sistema OOP como si fuera un
programa procedural"**. Los simptomas observables son 4:

| ID | Sintoma | Como observar en docs |
|---|---|---|
| S-1 | Nombres de clase reflejan funciones, no entidades | Verbos en infinitivo (`Calcular*`, `Procesar*`, `Validar*`) o gerundios |
| S-2 | Clases con un unico metodo "ejecutar/procesar/correr" | Solo 1 operacion en el bloque `class` del PlantUML |
| S-3 | Uso excesivo de `static` | Atributos/metodos sin estado de instancia |
| S-4 | Ausencia de OOP fundamentals (herencia, polimorfismo, encapsulamiento) | Sin relaciones de tipo `--\|>`, sin variantes polimorficas |

## 3. Insumos heredados del proyecto

### 3.1 Normativa relevante

- `source/normativa/estandares/std-008-naming-identificadores.rst` — naming de
  identificadores tecnicos (clases, metodos, etc.).
- `source/normativa/estandares/metodologia-oop-para-ucs.rst` — si existe, contiene
  reglas de aplicacion de OOP a UCs (a verificar).
- `source/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/` — material de
  referencia OOP del proyecto.

### 3.2 Catalogo a auditar

**Domain-model existente (67 archivos pre-WP predecesor):**

```
abandonment-report-service, access-group, access-group-function, action,
agent-daily-stat-repo, agent-report-service, alert, alert-hook, alert-repo,
alert-rule, application-log, assignment, assignment-repo, audit-event,
audit-query-service, audit-repo, audit-service, audit-validator,
base-report-service, bucket, call, caller-report-service, campaign,
column-catalog, comparative, cursor-encoder, evaluator-reloader,
exceptional-permission, exceptional-permission-repo, export-job, export-worker,
filter-validator, function, function-group, historical-report,
infrastructure-log, internal-mailbox, ivr-navigation-report-service,
kpi-calculator, menu, metric, nav-domain, permission-cache,
permission-service, pii-scanner, pipeline-execution, pipeline-log, rbac-repo,
report, rule-validator, sanitizer, saved-filter, saved-view,
scheduled-report, scheduled-report-list-service, scheduled-report-repo,
section, segment-resolver, separation-rule, session, subscription,
system-health, technical-metric, threshold, timing-calculator,
transfer-report-service, user
```

**Domain-model nuevo (16 del WP predecesor):**

```
authorization-guard, blacklisted-token, internal-message,
pipeline-execution-repo, metrics-cache, idempotency-policy, expiration-policy,
password-generator, effective-permissions-aggregator, user-repo, function-repo,
function-group-repo, separation-rule-repo, access-group-repo,
specification-pattern, strategy-pattern
```

**Use-case-view standalone uml-07 (83 del WP predecesor):**

83 archivos `uc-XXX-NN-<slug>.rst` con bloque `@startuml ... @enduml`. Estos NO
son clases — son diagramas de caso de uso. **NO aplica directamente** el
antipatron Functional Decomposition (que es sobre clases). Quedan **fuera del
audit principal** pero pueden auditarse por sub-usecases con nombres
funcionales si el ejecutor lo decide.

## 4. Heuristica de auditoria — adaptada al proyecto

### 4.1 Nombres sospechosos por prefijo (S-1)

```
PROHIBIDO_PREFIX = {
  "Calcular", "Calculate", "Compute",
  "Procesar", "Process",
  "Validar", "Validate",  ← DUDA: filter-validator existe; pero como repo del Validator pattern es OK
  "Ejecutar", "Execute",
  "Generar", "Generate",  ← DUDA: password-generator es nuevo; clarificar
  "Realizar", "Perform",
  "Crear", "Create",  ← DUDA: solo si es la unica responsabilidad
  "Obtener", "Get",
  "Hacer", "Do",
}
```

### 4.2 Nombres sospechosos por sufijo (S-1)

```
SUFIJOS_REVISAR = {
  "*Service",  ← DUDA: domain services son legitimos en DDD
  "*Validator",  ← DUDA: pattern Validator
  "*Calculator",  ← DUDA: KpiCalculator, TimingCalculator
  "*Generator",  ← DUDA: PasswordGenerator
  "*Aggregator",  ← DUDA: EffectivePermissionsAggregator
  "*Resolver",  ← DUDA: SegmentResolver
  "*Worker",  ← DUDA: ExportWorker
  "*Reloader",  ← DUDA: EvaluatorReloader
  "*Scanner",  ← DUDA: PIIScanner
  "*Sanitizer",  ← DUDA: Sanitizer
  "*Encoder",  ← DUDA: CursorEncoder
  "*Hook",  ← DUDA: AlertHook
  "*Guard",  ← DUDA: AuthorizationGuard
  "*Policy",  ← DUDA: IdempotencyPolicy, ExpirationPolicy
}
```

**Heuristica de desambiguacion** (R-01 mitigacion):

> Si la clase con sufijo sospechoso **declara explicitamente ser un pattern conocido**
> (Repository, Validator, Strategy, Service, Generator) y **respeta la spec del pattern**
> (interfaz, multiples metodos relevantes, atributos de configuracion), es **OK**.
>
> Si es solo un agrupador con `def execute()` o `def process()` y nada mas, es
> **antipatron**.

### 4.3 Single-method classes (S-2)

Auditar bloques PlantUML `class XxxName { ... }`:

- Si tiene **1 solo metodo** y es `execute`/`process`/`run`/`apply`/`handle` →
  **❌ Antipatron** (a menos que sea Strategy pattern declarado).
- Si tiene **1 solo metodo** pero es `compute(x, y)` con multiples atributos
  de configuracion (state) → **⚠ Revision** (puede ser legitimo).
- Si tiene **≥2 metodos relevantes** + atributos → **✓ OK**.

### 4.4 Static/stateless classes (S-3)

Si el archivo `domain-model/<entity>.rst` describe una clase **sin atributos
de instancia** (solo `+ metodo()` sin campos antes del `--`), evaluar:

- Si la operacion necesita state implicito (e.g. dependency injection en repos)
  → **✓ OK** (lo declara la nota).
- Si es realmente stateless y deberia ser un module/utility → **⚠ Revision**.

### 4.5 Ausencia OOP (S-4)

Buscar clases que harian sentido como:

- **Abstraccion base** + variantes (e.g. `BaseReportService` ya existe — bien!).
- **Polimorfismo** sobre tipo (en lugar de if-cadenas en el caller).
- **Encapsulamiento** (campos privados con getters declarados explicitamente).

**No es necesario tener TODAS** las 3 — falta de jerarquia es OK si el dominio
es plano.

## 5. Casos sospechosos identificados a priori (para chequeo riguroso)

Sin haber auditado aun, los 16 nuevos del predecesor + algunos pre-existentes
merecen examen riguroso:

### 5.1 Sufijos -Repo (5 nuevos + 7 pre-existentes)

`AssignmentRepo`, `ExceptionalPermissionRepo`, `RbacRepo`, `AlertRepo`,
`AuditRepo`, `AgentDailyStatRepo`, `ScheduledReportRepo`, `UserRepo`,
`FunctionRepo`, `FunctionGroupRepo`, `SeparationRuleRepo`, `AccessGroupRepo`,
`PipelineExecutionRepo`.

**Hipotesis:** todas implementan **Repository Pattern** (Eric Evans / Fowler).
Repository es un **patron OOP legitimo**: encapsula acceso a persistencia,
tiene multiples queries (CRUD + finders custom), tiene state implicito
(storage_backend). Veredicto esperado: ✓ OK por C-5 (declaran ser Repos).

### 5.2 Sufijos -Service (8 archivos)

`AuditService`, `AuditQueryService`, `AbandonmentReportService`,
`AgentReportService`, `BaseReportService`, `CallerReportService`,
`IvrNavigationReportService`, `TransferReportService`, `PermissionService`,
`ScheduledReportListService`.

**Hipotesis:** Domain Services en DDD — operaciones que no encajan en una
sola entidad. Veredicto esperado: ✓ OK si tienen ≥2 metodos relevantes.

### 5.3 Sufijos -Validator, -Calculator, -Generator, -Resolver, -Encoder, -Worker, -Hook, -Scanner, -Sanitizer, -Reloader, -Aggregator (varios)

`AuditValidator`, `RuleValidator`, `FilterValidator`, `KpiCalculator`,
`TimingCalculator`, `PasswordGenerator`, `SegmentResolver`, `CursorEncoder`,
`ExportWorker`, `AlertHook`, `PIIScanner`, `Sanitizer`, `EvaluatorReloader`,
`EffectivePermissionsAggregator`.

**Hipotesis:** mezcla — algunos son legitimos (Strategy/Patterns), otros
podrian caer en S-2 (single-method). El audit detallado clarificara.

### 5.4 Sufijos -Policy, -Guard (3 nuevos)

`IdempotencyPolicy`, `ExpirationPolicy`, `AuthorizationGuard`.

**Hipotesis:** Policy pattern + Guard middleware. Legitimos si tienen
multiples queries/operaciones encapsulando logica de negocio.

### 5.5 -Cache (2)

`PermissionCache`, `MetricsCache`.

**Hipotesis:** Cache es estructural (storage), tipicamente con `get/set/
invalidate` (≥3 metodos) y state (storage_backend, TTL). ✓ OK.

### 5.6 -Loader, -Reloader (1)

`EvaluatorReloader`.

**Riesgo S-2:** si solo tiene `reload()`, podria ser antipatron. Si tiene
`reload_config()`, `reload_catalog()`, `recalculate(id)` (≥2 metodos),
✓ OK.

### 5.7 Entities tradicionales (sin sufijo funcional)

`User`, `Session`, `Call`, `Campaign`, `Action`, `Alert`, `Threshold`,
`Subscription`, `Function`, `FunctionGroup`, `AccessGroup`,
`AccessGroupFunction`, `Assignment`, `ExceptionalPermission`,
`SeparationRule`, `Menu`, `NavDomain`, `Section`, `Bucket`, `Comparative`,
`SavedView`, `SavedFilter`, `Report`, `HistoricalReport`,
`ScheduledReport`, `Metric`, `TechnicalMetric`, `ApplicationLog`,
`InfrastructureLog`, `PipelineLog`, `PipelineExecution`, `AuditEvent`,
`AlertRule`, `ColumnCatalog`, `SystemHealth`, `InternalMailbox`,
`InternalMessage`, `ExportJob`, `BlacklistedToken`.

**Hipotesis:** entities canonicas de dominio. ✓ OK por C-1, evaluar C-2..C-4.

## 6. Plan de fases

### Phase 1 DISCOVER (este documento)

- [x] Bootstrap WP.
- [x] `wp-state.md` con scope + criterios.
- [x] Este analysis con hipotesis a priori.
- [ ] **SP-01:** ejecutor aprueba scope + responde 3 preguntas pendientes.

### Phase 3 ANALYZE

- Auditar los 99 archivos `domain-model/`:
  - Per archivo: aplicar C-1..C-5.
  - Producir veredicto OK / Revision / Antipatron.
  - Documentar evidencia.
- **SP-02 sample:** validar metodologia con 5 archivos antes del resto.
- Producir `audit-summary.md` con metricas + patrones recurrentes.

### Phase 11 TRACK

- Lessons + changelog.
- Si hay ❌ Antipatron, crear WP sucesor de remediacion.

## 7. Out of scope

- ❌ NO modificar archivos del domain-model en este WP.
- ❌ NO auditar codigo Python del backend.
- ❌ NO auditar `casos-uso/` 12 partes (no son clases).
- ❌ NO auditar uml-07 standalone (son diagramas de UC, no clases).
- ❌ NO auditar contra otros antipatrones de Brown (Blob, Lava Flow, etc.) —
  uno por WP.

## 8. Riesgos (resumen)

Ver `wp-state.md` seccion Riesgos. R-01 (falsos positivos) es el mas probable;
mitigacion: aplicar C-5 antes de C-1 cuando el sufijo es de pattern conocido.

## 9. Preguntas para SP-01

1. **Scope final**: ¿auditar solo 16 nuevos, los 99 totales del domain-model,
   o incluir tambien los 83 uml-07?
2. **Profundidad**: ¿auditar metodos dentro de clases (e.g. `User.calculate_age()`
   OK vs `Calculate.user_age()` antipatron)?
3. **Referencias internas**: ¿hay un `metodologia-oop-para-ucs.rst` u otro doc
   que define como debe ser el modelado OOP en IACT? Lo busco en proxima sesion.
