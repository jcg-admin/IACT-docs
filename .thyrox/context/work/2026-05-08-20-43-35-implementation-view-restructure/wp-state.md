```yml
project: IACT-docs
work_package: 2026-05-08-20-43-35-implementation-view-restructure
created_at: 2026-05-08 20:43:35
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano-grande (rename retroactivo DesignView + nuevo ImplementationView modular + nuevo uml-14 doc)
target: 1) Crear `uml-14/relaciones-dependencia-iact.rst` documentando el DAG de vistas arquitectonicas IACT. 2) Renombrar archivos de DesignView ya restructurado de nombres-tipo-de-artefacto (class/sequence/state/activity) a nombres-de-contenido (bounded-context, interaction-pattern, <entity>-lifecycle, <flow-name>-flow). 3) Restructurar ImplementationView de archivos planos a directorios por modulo usando nombres-de-contenido desde el inicio (layer-structure en lugar de components).
predecessor_wp: 2026-05-08-17-51-36-design-view-restructure (cerrado)
trigger: directiva del ejecutor — naming actual viola CLEAN_CODE; corregir DesignView + aplicar correcto a ImplementationView en el mismo WP
```

# WP — Implementation-View restructure (con rename retroactivo DesignView)

## Phase 1 — DISCOVER (consolidado tras directiva expandida)

### Hallazgo critico — naming meta-violation en DesignView ya restructurado

El naming aplicado en DesignView (`class.rst`, `sequence.rst`,
`state.rst`, `activity.rst`) viola el mismo principio de
CLEAN_CODE §6.2 que prohibe sufijos de tipo de artefacto
(`Factory`, `Serializer`, `ViewSet`):

> El nombre debe describir el **proposito/contenido**, no
> el tipo de artefacto/mecanismo.

`class.rst` solo dice "esto es un diagrama de clases" — pero
no dice **que clases ni para que**. Igual que `Factory` solo
dice "esto es un factory" sin decir el rol del dominio.

**Decision (per directiva del ejecutor):** corregir en este
mismo WP, antes de propagar el antipattern a ImplementationView.

### Tabla de renames retroactivos en DesignView

| Tipo actual | Razón violacion | Nombre correcto |
|---|---|---|
| `class.rst` | nombre del tipo UML, no del contenido | `bounded-context.rst` |
| `sequence.rst` | idem | `interaction-pattern.rst` |
| `state.rst` | idem; ademas varia por modulo | `<entity>-lifecycle.rst` |
| `activity.rst` | idem; varia por modulo | `<flow-name>-flow.rst` |

**Renames especificos por modulo en DesignView:**

| Modulo | class → | sequence → | state → | activity → |
|---|---|---|---|---|
| access | bounded-context | interaction-pattern | assignment-lifecycle | separation-check-flow |
| admin | bounded-context | interaction-pattern | — | — |
| alerts | bounded-context | interaction-pattern | alert-event-lifecycle | alert-evaluation-flow |
| audit | bounded-context | interaction-pattern | — | — |
| auth | bounded-context | interaction-pattern | session-lifecycle | jwt-authentication-flow |
| logs | bounded-context | interaction-pattern | — | — |
| permissions | bounded-context | interaction-pattern | — | effective-set-evaluation-flow |
| pipeline | bounded-context | interaction-pattern | pipeline-execution-lifecycle | etl-execution-flow |
| reports | bounded-context | interaction-pattern | export-job-lifecycle | async-export-flow |
| users | bounded-context | interaction-pattern | — | — |

**Conteo renames retroactivos:**
- 10 class → bounded-context
- 10 sequence → interaction-pattern
- 5 state → <entity>-lifecycle
- 6 activity → <flow-name>-flow
- **Total: 31 git mv en DesignView**

Plus updates:
- 10 module index.rst toctrees (refs a class/sequence/state/activity)
- ~30+ seealso refs internos entre archivos del mismo modulo

### ImplementationView — naming desde el inicio

| Tipo del archivo | Nombre incorrecto inicial | Nombre correcto |
|---|---|---|
| Archivo unico de componentes (api, service, repo, orm) | `components.rst` | `layer-structure.rst` |

**Estructura objetivo de implementation-view/<modulo>/:**

```
<modulo>/
  index.rst              ← caja del modulo
  layer-structure.rst    ← contenido de impl-<modulo>.rst (renamed)
```

### Nuevo doc uml-14: `relaciones-dependencia-iact.rst`

Documenta el DAG de dependencias entre vistas arquitectonicas
del proyecto IACT, adaptando el framework Rozanski a las
vistas reales del corpus. Mapeo:

| Vista IACT | Equivalente Rozanski | Diagramas usados |
|---|---|---|
| DomainModel | Information viewpoint | Clases, objetos, estados |
| UseCaseView | Functional viewpoint | Casos de uso |
| DesignView | Functional + Information | Clases, secuencias, actividades, estados |
| ImplementationView | Development viewpoint | Componentes |
| ProcessView | Concurrency viewpoint | Actividades, secuencias |
| DeployView | Deployment viewpoint | Distribucion |
| ContextView | Context viewpoint | Componentes, casos de uso |

Vocabulario STD-010 compliant (sin mencionar Django, Redis,
PostgreSQL, etc. en la narrativa pedagogica).

### Estado actual de ImplementationView (14 archivos planos)

| Categoria | Cuenta | Archivos |
|---|---|---|
| Indice | 1 | `index.rst` v2.0.0 |
| in-scope (10 modulos) | 10 | impl-{access, admin, alerts, audit, auth, logs, permissions, pipeline, reports, users}.rst |
| out-of-scope preservar flat | 3 | impl-{caller, operator, supervision}.rst |

### Cross-refs (ImplementationView)

- 0 refs externos
- 0 refs internos entre impl-X.rst

### Decisiones cerradas

- **SP-D1 (out-of-scope archivos):** Opcion A — preservar
  los 3 archivos flat (caller, operator, supervision). Mismo
  criterio que DesignView. Sin perdida de contenido.
- **SP-D2 (naming archivo unico):** `layer-structure.rst`
  (no `components.rst`) — describe el contenido (estructura
  de capas API/service/repo/ORM), no el tipo de diagrama UML.
- **SP-D3 (pilot):** ejecutar DesignView rename pilot en
  `access/` primero, validar build, replicar a 9 restantes.
  ImplementationView pilot en `access/` segundo.

### Conteo global del WP expandido

| Bloque | Cambios |
|---|---|
| 1. Crear `uml-14/relaciones-dependencia-iact.rst` + agregar a toctree | 1 nuevo + 1 edit |
| 2. Rename retroactivo DesignView (31 git mv) | 31 mv |
| 3. Update DesignView module index.rst (10) | 10 edits |
| 4. Update DesignView seealso internos (~30+) | ~30 sed |
| 5. Crear ImplementationView modular (10 git mv + 10 index.rst nuevos + 1 implementation-view/index v3.0.0) | 21 cambios |
| **Total** | **~95 cambios + 11 nuevos** |

### Plan de ejecucion (alto nivel)

1. **T-1 uml-14 doc** (nueva, low risk, sin dependencia)
2. **T-2 pilot DesignView access/** rename (validar pattern)
3. **T-3..T-11 replicar DesignView 9 modulos**
4. **T-12 pilot ImplementationView access/** rename
5. **T-13..T-21 replicar ImplementationView 9 modulos**
6. **T-22 ImplementationView/index.rst v3.0.0**
7. **T-23 build strict final**
8. **T-24 TRACK changelog**

### Refs

- WP `design-view-restructure` (precedente) — pattern de cajas.
- `design-view/index.rst` v4.0.0 — referencia de scope.
- CLEAN_CODE_NAMING_PRINCIPLES.md — principio §6.2 que motiva
  el rename retroactivo.

### Stopping points

- **SP-D2:** confirmados los nombres especificos por modulo
  (especialmente activity → flow-name; verificar si los
  flow-names son aceptables al ejecutor antes de massive
  rename).
- **SP-D3:** validar pattern del rename via build strict tras
  pilot DesignView access/ antes de replicar.
- **SP-D4:** validar pattern del ImplementationView pilot.
- **SP-D5:** build strict final EXIT=0 con 0 warnings.
