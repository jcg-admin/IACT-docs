```yml
created_at: 2026-05-05 20:58:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis de gaps en domain-model — auditoría desde UC specs

## 1. Propósito

Auditar las 67 clases canónicas del `source/arquitectura-tecnica/domain-model/` contra
las clases referenciadas en los specs textuales de los 83 UCs (`flujo-principal.rst`,
`implementacion-tecnica.rst`, `informacion-general.rst`, `patrones-diseno.rst`).

**Output**: lista priorizada de:

1. Clases nuevas a **crear** en domain-model.
2. Naming variants a **unificar** (legacy → canónico).
3. Métodos a **agregar** a clases existentes.
4. Falsos positivos (enum values, specifications, strategies — no son clases).

## 2. Metodología

Script Python con regex `\`\`([A-Z][A-Za-z]{3,})\`\`` sobre los 4 specs de cada UC,
agrupando por:

- Match contra archivos `domain-model/<entity>.rst` (PascalCase de filename kebab).
- Match contra `Class.method` con regex `\`\`([A-Z][A-Za-z]+)\.([a-z_][a-z_0-9]*)\`\``.

Output machine-readable: `analyze/domain-model-gap-extraction.json`.

## 3. Resultados crudos

| Métrica | Valor |
|---|---|
| Clases canónicas en domain-model | 67 |
| Clases mencionadas en specs y existentes en domain-model | 12 |
| Clases mencionadas en specs y NO en domain-model | **81** |
| Métodos detectados en clases existentes | 5 (en User, Session, Assignment) |

## 4. Clasificación de las 81 "no-en-domain-model"

Tras revisar manualmente, las 81 clases se distribuyen así:

| Categoría | Count | Naturaleza | Acción |
|---|---|---|---|
| **Clases reales faltantes** | 9 | Componentes de dominio referenciados por UCs como sistemas/repos | **Crear archivo en domain-model/** |
| **Naming variants legacy** | 7 | Nombres alternativos de clases que sí existen | Documentar mapping canónico, NO crear |
| **Repos no existentes** | 5 | Repositorios canónicos para entities existentes | **Crear archivo de repo** |
| **Falsos positivos: enum values** | 11 | Strings UPPER_CASE como ACTIVE, INACTIVE, ELIMINATED, REVOKED | Ignorar (son valores, no clases) |
| **Falsos positivos: Specification/Strategy patterns** | ~20 | Implementaciones de patrones (CriticalFunctionSpec, LastHolderSpec, NotifyOnAssignStrategy, etc.) | Ignorar (son implementaciones del pattern, viven en código no en modelo) |
| **Otras (single-mention, baja relevancia)** | ~29 | Clases efímeras, helpers internos, DTOs | Evaluar caso por caso |

## 5. Lista priorizada de adiciones

### 5.1 Clases nuevas a crear (9 — confirmadas)

Top usadas por UCs distintos. Todas tienen ≥2 UCs, alta probabilidad de ser entidades
de dominio reales:

| Clase | UCs distintos | Bounded Context | Justificación |
|---|---|---|---|
| **AuthorizationGuard** | 10 | RBAC | Guard/middleware que verifica función RBAC en cada request HTTP. Componente cross-cutting referenciado por toda la app. |
| **BlacklistedToken** | 5 | Auth | Lista de tokens JWT revocados (post-logout). Entity con TTL hasta `exp` del token original. |
| **InternalMessage** | 4 | Mailbox | Item dentro de InternalMailbox. Diferente del container — representa cada mensaje individual con sender, target, body, read_state, urgency. |
| **PipelineExecutionRepo** | 4 | Pipeline | Repositorio de PipelineExecution. Existe la entity (`pipeline-execution.rst`) pero no su repo canónico. |
| **MetricsCache** | 4 | Cross-cutting | Cache de cálculos KPI/métricas (TTL configurable, invalidation por dataset). |
| **IdempotencyPolicy** | 3 | Cross-cutting | Política de idempotencia para POSTs (request_id + dedup ventana). |
| **ExpirationPolicy** | 2 | RBAC / Auth | Política de expiración para ExceptionalPermission y otros (1h-30d, configurable). |
| **PasswordGenerator** | 2 | Auth / Users | Generador de passwords iniciales (UC_USR_01) y temporales. |
| **EffectivePermissionsAggregator** | 1 | RBAC | Agregador que computa el `effective_set` de un User combinando AGRs + ExceptionalPermissions. |

**Total:** 9 archivos nuevos en `domain-model/`:

```
domain-model/authorization-guard.rst
domain-model/blacklisted-token.rst
domain-model/internal-message.rst
domain-model/pipeline-execution-repo.rst
domain-model/metrics-cache.rst
domain-model/idempotency-policy.rst
domain-model/expiration-policy.rst
domain-model/password-generator.rst
domain-model/effective-permissions-aggregator.rst
```

### 5.2 Repos canónicos a crear (5 — falta repo de entity existente)

Para entidades que tienen archivo pero no su repo canónico:

| Clase repo | Entity asociada | UCs que lo refieren (vía variant `XxxRepository`) |
|---|---|---|
| **UserRepo** | `user.rst` | 11 (mencionado como UserRepository) |
| **FunctionRepo** | `function.rst` | 2 (FunctionRepository) |
| **FunctionGroupRepo** | `function-group.rst` | 1 (variant) |
| **SeparationRuleRepo** | `separation-rule.rst` | 3 (SoDRuleRepository) |
| **AccessGroupRepo** | `access-group.rst` | 1 (AGRRepository) |

**Total:** 5 archivos nuevos:

```
domain-model/user-repo.rst
domain-model/function-repo.rst
domain-model/function-group-repo.rst
domain-model/separation-rule-repo.rst
domain-model/access-group-repo.rst
```

### 5.3 Naming variants a unificar (7 — sin crear archivo)

Documentar mapping canónico. Los specs textuales referencian estos nombres legacy;
los uml-07 standalone usarán los canónicos:

| Variant legacy en specs | Canónico (existe) |
|---|---|
| `AssignmentRepository` | `AssignmentRepo` (`assignment-repo.rst`) |
| `SoDRule` | `SeparationRule` (`separation-rule.rst`) |
| `SoDRuleRepository` | `SeparationRuleRepo` (a crear, ver 5.2) |
| `FunctionRepository` | `FunctionRepo` (a crear, ver 5.2) |
| `UserRepository` | `UserRepo` (a crear, ver 5.2) |
| `ExceptionalPermissionRepository` | `ExceptionalPermissionRepo` (`exceptional-permission-repo.rst`) |
| `AGRRepository` | `AccessGroupRepo` (a crear, ver 5.2) |

**Acción:** ningún archivo nuevo por variants; los uml-07 usarán nombres canónicos.

### 5.4 Falsos positivos — ignorar

#### 5.4.1 Enum values (11)

```
ACTIVE, INACTIVE, BLOCKED, ELIMINATED, REVOKED, FIRING, ACKNOWLEDGED, RESOLVED,
SUCCESS, FAILED, ETC.
```

Son strings/constants, NO clases. No requieren archivo.

#### 5.4.2 Specification pattern (~10)

```
Specification, CriticalFunctionSpec, LastHolderSpec, ...
```

Son implementaciones del pattern Specification. Viven en código (no son entidades
de dominio per se). Si el ejecutor quiere documentarlas, sería en un archivo
single dedicado al pattern (e.g. `domain-model/specification-pattern.rst`) — fuera
del scope de este WP.

#### 5.4.3 Strategy pattern (~7)

```
NotifyOnAssignStrategy, NotifyOnRevokeStrategy, LastHolderPolicy, ...
```

Implementaciones del pattern Strategy. Mismo análisis: viven en código, opcional
documentar como pattern doc separado.

### 5.5 Métodos detectados en clases existentes (5)

```
Assignment.state    ← atributo/getter
Session.id          ← atributo/getter
Session.state       ← atributo/getter
User.password_hash  ← atributo/getter
User.state          ← atributo/getter
```

**Hallazgo:** los specs no usan la sintaxis ``Class.method()`` con backticks de forma
sistemática. Los 5 detectados son **getters de atributos**, no métodos verdaderos.

**Implicación:** la hipótesis heredada Q4 del predecesor de "~30 métodos faltantes"
**no se confirma desde la extracción automatizada**. Probablemente el predecesor
auditó manualmente sin contar el formato consistente.

**Acción:** auditoría manual incremental durante Phase 10 EXECUTE. Si al generar un
uml-07 standalone aparece un método claramente referenciado en flujo-principal y
no documentado, se agrega al archivo del domain-model entonces (no en bloque
adelantado).

## 6. Plan de acción

### 6.1 Crear 14 archivos nuevos en domain-model (9 clases + 5 repos)

Spec mínima por archivo (template):

```rst
.. meta::
 :artefacto: AT_DM_CLASS_<ENTITY>
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: <Auth | RBAC | Reports | Pipeline | etc.>
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_class_<entity_snake>:

==========
EntityName
==========

<Descripción 1-2 párrafos: qué es, por qué existe, qué responsabilidades tiene>

.. uml::
 :caption: Clase EntityName.

 @startuml

 class EntityName {
  + atributo : Tipo
  ...
  + operacion()
  ...
 }

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/<mod>/<uc>/index` — descripción del uso.
...

Relaciones
==========

<dependencies hacia/desde otras clases del domain-model>
```

### 6.2 Update seealso en los 53 uml-06 existentes (opcional)

Los 53 uml-06 del predecesor referencian solo entidades canónicas existentes (verificado
en `actor-vocabulary-analysis.md` §3.3). Si las 14 nuevas son referenciadas también, se
agregan a sus `seealso` cuando aplique. Pero solo si SE GENERAN nuevos refs en uml-07
standalone — los uml-06 no se tocan (out-of-scope L-01).

### 6.3 No agregar métodos masivamente

Auditoría manual durante Phase 10. Solo agregar método a clase existente cuando el
uml-07 standalone lo referencia explícitamente y no está en el archivo del domain-model.

## 7. Resumen ejecutivo

| Trabajo | Count | Status |
|---|---|---|
| Clases nuevas a crear | 9 | Propuesto |
| Repos canónicos a crear | 5 | Propuesto |
| **Total archivos nuevos en domain-model** | **14** | Pendiente SP-02 PILOT |
| Naming variants a documentar (no crear) | 7 | Documentado en 5.3 |
| Métodos a agregar | TBD durante Phase 10 | Diferido |
| Falsos positivos identificados | ~40 | Ignorar |

**Reducción significativa vs. estimación heredada del predecesor:**

| Predecesor (Q3) | Este análisis |
|---|---|
| ~18 clases nuevas | 9 clases nuevas + 5 repos = 14 archivos |
| ~30 métodos faltantes | TBD durante Phase 10 (no detectados sistemáticamente) |

## 8. Output

- `domain-model-gap-extraction.json` — extracción machine-readable.
- Este documento — análisis curado y plan de acción.

## 9. Decisiones pendientes para SP-02 PILOT

1. ¿Aprobar lista de **9 clases nuevas** propuestas? Especialmente:
   - `AuthorizationGuard` — ¿como entity de domain o como infrastructure component?
   - `EffectivePermissionsAggregator` — ¿amerita archivo o vive como método de
     `PermissionService`?
2. ¿Aprobar lista de **5 repos canónicos** a crear?
3. ¿Documentar Specification/Strategy patterns en archivo dedicado o ignorar?
4. ¿En qué orden crear: primero los 14 archivos de domain-model, luego los 83 uml-07
   que los refieren? O al revés (uml-07 primero, ajustar refs si una clase nueva no
   se aprueba)?

## 10. Próxima fase

**Phase 5 STRATEGY**: definir template canónico del archivo `uc-XXX-NN-<slug>.rst`
con todas las decisiones de Phase 3 (vocabulario actor + cross-refs domain-model +
estilo de notas) consolidadas.
