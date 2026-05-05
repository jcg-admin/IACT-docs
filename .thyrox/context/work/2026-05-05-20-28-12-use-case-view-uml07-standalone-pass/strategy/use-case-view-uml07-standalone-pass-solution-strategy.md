```yml
created_at: 2026-05-05 21:08:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Solution Strategy — `use-case-view-uml07-standalone-pass`

## 1. Key Ideas

### KI-1 — Generación en dos fases (domain-model PRIMERO, uml-07 DESPUÉS)

Decisión SP Phase 3: crear los 14 archivos nuevos en `domain-model/` antes de los 83
uml-07 standalone, para que estos últimos puedan referenciarlos vía `:doc:` desde el
primer commit sin romper builds.

### KI-2 — Funciones RBAC como actores (P-15 granular)

No se introduce mapping a roles. Los actores en uml-07 standalone son **funciones
RBAC específicas** (igual que en los uml-06 del predecesor), preservando la trazabilidad
RBAC del sistema. Stereotypes:

| Stereotype | Uso |
|---|---|
| (sin) | Función RBAC iniciadora |
| `<<beneficiario>>` | Función RBAC receptora |
| `<<sistema>>` | Entidad del domain-model (nombre canónico) |
| `<<sistema_externo>>` | Frontera externa (Trunk SIP, Cron) — **decisión nueva** |
| `<<externo>>` | Caller no autenticado |

### KI-3 — Lectura completa de specs por UC (sin scripts ni atajos)

**Decisión explícita del ejecutor (post Phase 8):** NO se usan scripts de generación
masiva. Cada uno de los 83 archivos uml-07 standalone se construye **manualmente**,
con lectura completa de todos los specs textuales del UC:

1. `casos-uso/<mod>/<uc>/index.rst` (toctree de las 12 partes).
2. `casos-uso/<mod>/<uc>/informacion-general.rst` (Parte 1).
3. `casos-uso/<mod>/<uc>/actores-precondiciones.rst` (Parte 2).
4. `casos-uso/<mod>/<uc>/flujo-principal.rst` (Parte 3).
5. `casos-uso/<mod>/<uc>/flujos-alternos.rst` (Parte 4).
6. `casos-uso/<mod>/<uc>/excepciones.rst` (Parte 5).
7. `casos-uso/<mod>/<uc>/criterios-aceptacion.rst` (Parte 9).
8. (Opcional) `casos-uso/<mod>/<uc>/patrones-diseno.rst` y
   `casos-uso/<mod>/<uc>/implementacion-tecnica.rst`.

El uml-06 existente (`diagramas-uml/diagrama-de-caso-de-uso.rst`) se consulta como
referencia inicial pero NO se confía ciegamente — se valida cada decisión contra los
specs textuales.

**Razón:** la lección del predecesor (L-03) demostró que la compresión de tiempo en
generación masiva produce diagramas "shallow" con extends incompletos y notas BR/CNST
parciales. La velocidad introduce más errores que soluciones.

### KI-4 — Specification y Strategy patterns documentados en archivos dedicados

En lugar de crear N archivos por cada subclase del pattern, se crean DOS archivos
documentales agregando la lista de implementaciones:

```
domain-model/specification-pattern.rst   ← lista CriticalFunctionSpec, LastHolderSpec, etc.
domain-model/strategy-pattern.rst        ← lista NotifyOnAssignStrategy, etc.
```

Los uml-07 que mencionan estos patterns referenciarán estos dos archivos en `seealso`.

### KI-5 — Auditoría incremental durante Phase 10 EXECUTE

Métodos faltantes en clases existentes se agregan **on-demand** cuando un uml-07
estandalone los referencia. No se hace bloque adelantado de "agregar 30 métodos".

## 2. Research

### 2.1 Templates analizados

Revisé estructura canónica de 2 archivos representativos del domain-model:

- `separation-rule.rst` (entity) — versión 1.2.0, estructura: meta + título + descripción
  + bloque `@startuml class { atributos / métodos }` + `enum` + relaciones + (a veces)
  notas + sección "Trazabilidad a UCs".
- `assignment-repo.rst` (repo) — versión 1.0.0, estructura igual pero con clase `Repo`
  con métodos CRUD + filters.

### 2.2 Conventions uml-07 leídas

- Material adaptado de "Aprendiendo UML en 24 horas" — Hora 7.
- Refs: `source/base-cognitiva/_uml/uml-07-*` (10 lessons).

## 3. Decision

### 3.1 Template canónico — archivo `domain-model/<entity>.rst` (clase nueva)

```rst
.. meta::
 :artefacto: AT_DM_CLASS_<ENTITY_UPPER>
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: <Auth|RBAC|Reports|Pipeline|Mailbox|CrossCutting>
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: <Critico|Importante|Interno>

.. _dm_class_<entity_snake>:

============
<EntityName>
============

<Descripción 1-3 párrafos: qué es, responsabilidad, restricciones BR/CNST/P relevantes>

.. uml::
 :caption: Clase <EntityName> — <descripción breve>.

 @startuml

 class <EntityName> {
   + atributo : Tipo
   ...
   --
   + operacion(args) : ReturnType
   ...
 }

 ' Enums asociados:
 enum <EntityName>State {
   STATE_A
   STATE_B
 }

 <EntityName> -- <EntityName>State

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/<mod>/<uc>/index` — descripción del uso.
...

Relaciones
==========

<deps hacia/desde otras clases del domain-model>
```

### 3.2 Template canónico — archivo `domain-model/<entity>-repo.rst` (repo)

Igual al anterior pero la clase tiene métodos CRUD + queries:

```rst
class <EntityName>Repo {
  - storage_backend : StorageBackend
  --
  + create(entity : <EntityName>) : UUID
  + get_by_id(id : UUID) : <EntityName>
  + find_by_<field>(value : Type) : List<<EntityName>>
  + update(id : UUID, changes : Map) : <EntityName>
  + delete_logical(id : UUID, actor_id : UUID) : void
}
```

### 3.3 Template canónico — archivo `use-case-view/<mod>/uc-XXX-NN-<slug>.rst`

```rst
.. meta::
 :artefacto: AT_UC_<MOD_UPPER>_<UC_NN>
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: <module>
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: <Critico|Importante>

.. _at_uc_<mod>_<uc_id_snake>:

==========================================
UC_XXX_NN — <Título descriptivo del UC>
==========================================

<Resumen 2-3 líneas del UC>

.. uml::
 :caption: UC_XXX_NN — actores y casos asociados.

 @startuml

 left to right direction

 ' Funciones RBAC iniciadoras (STD-011: alias = nombre función exacto)
 actor "<funcion_rbac>" as <funcion_rbac>
 actor "<otra_funcion>" as <otra_funcion>
 ' Funciones RBAC beneficiarias
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 ' Sistemas (entidades del domain-model — STD-011: alias = CamelCase clase)
 actor "<EntityCanonical>" as <EntityCanonical> <<sistema>>
 ' Sistemas externos (fuera del dominio)
 actor "<Boundary>" as <Boundary> <<sistema_externo>>

 rectangle "MOD_<Module>" {
   usecase "UC_XXX_NN\n<Titulo>" as UC_XXX_NN
   usecase "Validar..." as VAL_X
   ...
 }

 INVOKER --> UC_XXX_NN
 F_OTHER --> UC_XXX_NN
 UC_XXX_NN ..> VAL_X : <<include>>
 ...

 note bottom of UC_XXX_NN
   <Notas BR/CNST/P/ADR relevantes>
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/<entity-1>` — <breve descripción>.
 - :doc:`/arquitectura-tecnica/domain-model/<entity-2>` — <breve descripción>.
 ...

 **UC backing** (si es vista alternativa):

 - :doc:`/requisitos/casos-uso/<mod>/<uc-backing>/index` — operación realizada.

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/<mod>/<uc>/index` — Parte 1-12.
```

## 4. Pipeline de generación (Phase 10 EXECUTE)

### 4.1 Etapa 1 — domain-model nuevas clases (T-001..T-014)

| Task | Archivo | Bounded |
|---|---|---|
| T-001 | `domain-model/authorization-guard.rst` | RBAC |
| T-002 | `domain-model/blacklisted-token.rst` | Auth |
| T-003 | `domain-model/internal-message.rst` | Mailbox |
| T-004 | `domain-model/pipeline-execution-repo.rst` | Pipeline |
| T-005 | `domain-model/metrics-cache.rst` | CrossCutting |
| T-006 | `domain-model/idempotency-policy.rst` | CrossCutting |
| T-007 | `domain-model/expiration-policy.rst` | RBAC/Auth |
| T-008 | `domain-model/password-generator.rst` | Auth/Users |
| T-009 | `domain-model/effective-permissions-aggregator.rst` | RBAC |
| T-010 | `domain-model/user-repo.rst` | RBAC |
| T-011 | `domain-model/function-repo.rst` | RBAC |
| T-012 | `domain-model/function-group-repo.rst` | RBAC |
| T-013 | `domain-model/separation-rule-repo.rst` | RBAC |
| T-014 | `domain-model/access-group-repo.rst` | RBAC |

**Validación post Etapa 1:**

- T-VAL-1A: build `sphinx-build -W` con 0 warnings nuevos.
- T-VAL-1B: actualizar `domain-model/index.rst` toctree con los 14 nuevos.

### 4.2 Etapa 2 — patrones documentales (T-015, T-016)

| Task | Archivo |
|---|---|
| T-015 | `domain-model/specification-pattern.rst` |
| T-016 | `domain-model/strategy-pattern.rst` |

### 4.3 Etapa 3 — pilot 5 sample UC (T-017..T-021)

Selección representativa por familia semántica:

| Task | Archivo | Razón |
|---|---|---|
| T-017 | `use-case-view/admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` | Multi-invoker (4 funciones), validaciones complejas |
| T-018 | `use-case-view/operator/uc-opr-02-atender-llamada-entrante.rst` | Caller externo, telephony, audit obligatorio |
| T-019 | `use-case-view/reports/uc-rpt-12-reporte-de-agentes.rst` | UC_INC_RPT_01 included, multi-service |
| T-020 | `use-case-view/supervision/uc-sup-01-monitorear-llamada-whisper.rst` | P-39 audit reforzado, compliance legal |
| T-021 | `use-case-view/audit/uc-aud-03-exportar-auditoria.rst` | ExportWorker async, mailbox, P-39 |

**SP-02 PILOT gate**: ejecutor valida los 5 antes de propagar.

### 4.4 Etapa 4 — generación manual UC por UC (T-022..T-100+)

**Sin scripts. Sin atajos. Sin prisa.** Cada UC se construye así:

1. **Leer specs completos** (KI-3): 7 archivos del UC.
2. **Identificar actores RBAC** invocadores y beneficiarios desde
   `actores-precondiciones.rst` y referencias cruzadas en otros UCs.
3. **Identificar sub-usecases** del flujo principal + flujos alternos.
4. **Identificar extends candidatos** desde `flujos-alternos.rst` y `excepciones.rst`.
5. **Identificar entidades del domain-model** referenciadas y verificar nombre canónico.
6. **Construir el `@startuml`** siguiendo template canónico de Phase 5.
7. **Escribir notas BR/CNST/P/ADR** completas (incluyendo `criterios-aceptacion.rst`).
8. **Construir `seealso`** con `:doc:` a domain-model + UC backing + spec textual.
9. **Build local strict** del archivo individual (verificar 0 warnings).
10. **Audit script** sobre el archivo individual (R-01..R-12 + BR-006).

Solo cuando los 10 pasos pasan, se procede al siguiente UC.

**Cadencia:** un UC tarda 20-40 min (vs 2-3 min "shallow" del predecesor). Estimación
total Phase 10: 30-50h sostenidas. Distribuible en sesiones por módulo o por chunks
de 3-5 UCs.

**Commits:** un commit por cada 3-5 UCs (no por UC individual — demasiada granularidad,
ni por módulo entero — demasiado coarse). Tim Pope style con scope `(use-case-view)`.

Orden propuesto (de menor a mayor riesgo):

1. **admin** (3 UCs restantes — uc-adm-02, uc-adm-03)
2. **permissions** (10 — incluye 7 con uml-06 pre-existente)
3. **users** (4)
4. **auth** (5)
5. **access** (7)
6. **audit** (3 restantes)
7. **alerts** (5)
8. **pipeline** (4)
9. **caller** (5)
10. **supervision** (2 restantes)
11. **logs** (7)
12. **operator** (10)
13. **reports** (16 — incluye uc-inc-rpt-01)

### 4.5 Etapa 5 — module index updates (T-101..T-113)

Actualizar `use-case-view/<module>/index.rst` para que las xref tables apunten a los
nuevos archivos auto-explicativos en lugar de a `casos-uso/`.

### 4.6 Etapa 6 — audit script + final build (T-114, T-115)

| Task | Acción |
|---|---|
| T-114 | Script `validate-uml07-standalone.sh` que verifica R-01..R-12 + BR-006 |
| T-115 | Build strict final + 0 warnings + audit script 0 issues |

## 5. Riesgos mitigados por la estrategia

| Riesgo | Mitigación |
|---|---|
| R-01 (uml-06 base shallow) | KI-3 reusa pero releyendo flujos-alternos |
| R-02 (sistemas no canónicos) | KI-2 + tabla canonical en actor-vocabulary-analysis |
| R-03 (83 archivos × revisión) | Etapas + commits checkpoint + SP-02 pilot |
| R-04 (drift de scope) | wp-state.md::target re-leído en cada Etapa |
| R-06 (build break en index updates) | Etapa 5 separada; index updates después de 83 archivos generados |
| R-08 (PlantUML sintaxis) | SP-02 valida 5 sample antes de masivo |
| R-11 (over-engineering domain-model) | Lista cerrada de 9 + 5 + 2 = 16 archivos. NO crear más sin SP gate. |
| R-12 (métodos vs código real) | KI-5: agregar on-demand, documentar como spec |

## 6. Métricas de éxito

| Métrica | Target |
|---|---|
| Archivos uml-07 standalone | 83 / 83 |
| Archivos domain-model nuevos (clases + repos + patterns) | 16 / 16 |
| Module index files actualizados | 13 / 13 |
| Build strict warnings | 0 nuevos |
| Audit script violations | 0 |
| Cobertura `:doc:` cross-refs domain-model | ≥ 90% (mejora vs 85% actual) |

## 7. Próxima fase

Phase 6 PLAN: definir scope statement formal, in/out-of-scope detallado, ROADMAP update.
Phase 7 DESIGN: requirements-spec con Given/When/Then para los archivos de domain-model
y para los uml-07 standalone (template formal).
Phase 8 PLAN EXECUTION: task plan T-001..T-115 con DAG y trazabilidad.
