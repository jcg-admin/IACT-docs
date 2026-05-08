```yml
created_at: 2026-05-08 21:10:00
project: IACT-docs
work_package: 2026-05-08-20-43-35-implementation-view-restructure
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — implementation-view-restructure (con rename retroactivo DesignView + uml-14 doc)

## [1.0.0] — 2026-05-08

### Resumen

WP que originalmente solo migraba ImplementationView a estructura
modular fue **expandido** durante DISCOVER tras hallazgo critico:
los nombres de archivo aplicados en DesignView ya restructurado
(`class.rst`, `sequence.rst`, `state.rst`, `activity.rst`)
**violan el mismo principio CLEAN_CODE §6.2** que prohibe
sufijos como `Factory`, `Serializer`. El nombre describe el
tipo de artefacto UML, no el contenido/proposito.

Este WP corrige retroactivamente los nombres en DesignView,
aplica naming correcto desde el inicio en ImplementationView,
y agrega un doc nuevo en `uml-14` documentando el DAG de
dependencias entre vistas arquitectonicas IACT.

### Added

#### Nuevo doc — `uml-14/relaciones-dependencia-iact.rst`

288 lineas. Documenta:
- Mapeo Vista IACT ↔ Viewpoint Rozanski (7 vistas)
- DAG de dependencias entre vistas con UML
- Detalle de dependencias por categoria (5 categorias)
- Orden optimo de lectura del corpus IACT
- Estado actual de cada vista
- Implicaciones para la documentacion (no duplicacion,
  lectura cruzada)

Agregado al toctree de `uml-14/index.rst`.

#### 10 module index.rst en ImplementationView

Cada modulo: meta + label `_at_impl_mod_<m>_index` + titulo +
intro + UML panoramico curated (capas API/service/repo/orm) +
lectura + toctree a `layer-structure` + seealso a UCs +
DesignView + domain-model.

#### Nuevo `implementation-view/index.rst` v3.0.0

Refactor completo: dos secciones de toctree (modulos in-scope +
out-of-scope preservados flat), notes de scope y de
reorganizacion v3.0.0, seealso a relaciones-dependencia-iact.

### Renamed (retroactivo en DesignView — 31 git mv)

Aplicacion del principio "nombre describe contenido, no tipo
de artefacto":

#### Genericos (todos los modulos)

| Antes | Despues |
|---|---|
| `<modulo>/class.rst` | `<modulo>/bounded-context.rst` |
| `<modulo>/sequence.rst` | `<modulo>/interaction-pattern.rst` |

10 modulos x 2 = **20 renames genericos.**

#### Especificos por modulo (state -> entity-lifecycle)

| Antes | Despues |
|---|---|
| `access/state.rst` | `access/assignment-lifecycle.rst` |
| `alerts/state.rst` | `alerts/alert-event-lifecycle.rst` |
| `auth/state.rst` | `auth/session-lifecycle.rst` |
| `pipeline/state.rst` | `pipeline/pipeline-execution-lifecycle.rst` |
| `reports/state.rst` | `reports/export-job-lifecycle.rst` |

**5 renames de state.**

#### Especificos por modulo (activity -> flow-name-flow)

| Antes | Despues |
|---|---|
| `access/activity.rst` | `access/separation-check-flow.rst` |
| `alerts/activity.rst` | `alerts/alert-evaluation-flow.rst` |
| `auth/activity.rst` | `auth/jwt-authentication-flow.rst` |
| `permissions/activity.rst` | `permissions/effective-set-evaluation-flow.rst` |
| `pipeline/activity.rst` | `pipeline/etl-execution-flow.rst` |
| `reports/activity.rst` | `reports/async-export-flow.rst` |

**6 renames de activity.**

**Total renames retroactivos DesignView: 31 git mv.**

### Renamed (ImplementationView — 10 git mv)

Naming basado en contenido desde el inicio:

| Antes | Despues |
|---|---|
| `impl-access.rst` | `access/layer-structure.rst` |
| `impl-admin.rst` | `admin/layer-structure.rst` |
| `impl-alerts.rst` | `alerts/layer-structure.rst` |
| `impl-audit.rst` | `audit/layer-structure.rst` |
| `impl-auth.rst` | `auth/layer-structure.rst` |
| `impl-logs.rst` | `logs/layer-structure.rst` |
| `impl-permissions.rst` | `permissions/layer-structure.rst` |
| `impl-pipeline.rst` | `pipeline/layer-structure.rst` |
| `impl-reports.rst` | `reports/layer-structure.rst` |
| `impl-users.rst` | `users/layer-structure.rst` |

`layer-structure.rst` (no `components.rst`) — el archivo
documenta la estructura de capas API/service/repository/ORM,
no es solo un diagrama de componentes UML.

### Preserved (out-of-scope)

`impl-caller.rst`, `impl-operator.rst`, `impl-supervision.rst`
preservados como flat al raiz de implementation-view por
decision SP-D1 (Opcion A — preservar contenido sustantivo,
mismo criterio que DesignView).

### Cross-refs migration

Updates aplicados:
- ~30+ seealso refs internos en archivos DesignView
  re-targeteados a los nuevos nombres
- 10 toctrees de DesignView module index.rst actualizados
- 10 in-text :doc: refs (`:doc:\`class\``, `:doc:\`sequence\``,
  etc.) en DesignView module index.rst actualizados
- 1 ref externo en `system-view/clases-sistema-iact.rst`
  re-targeteado de `pipeline/state` a
  `pipeline/pipeline-execution-lifecycle`
- Cross-cluster ref `access/assignment-lifecycle.rst` →
  `permissions/activity` re-targeteada a
  `permissions/effective-set-evaluation-flow`

### Hallazgos durante EXECUTE

- **Naming meta-violation detectada y corregida:** este WP
  expandido es la correccion del antipattern aplicado en
  el WP previo design-view-restructure. Aprendizaje:
  validar el naming **semantico** de los archivos (no solo
  estructural) antes de propagar a la vista siguiente.
- **Duplicate labels:** los module index.rst tenian el mismo
  label `_at_impl_mod_<m>` que los layer-structure.rst
  (heredado del impl-X.rst original). Fix: cambiar label
  del index.rst a `_at_impl_mod_<m>_index`.
- **Title overlines em-dash:** el em-dash `—` cuenta
  distinto en el counter de docutils. Patron repetido del
  pilot. Fix: extender overlines de 60 a 64 chars
  (permissions) o de 66 a 70 (uml-14 doc).
- **Estructura de overline mal aplicada por script Python:**
  edicion automatica que escribio overline + underline + un
  segundo "==" suelto. Fix manual.

### Verification

```bash
# Build strict canonico
$ make html SPHINXOPTS='-W -j auto'
build succeeded.
EXIT=0
0 warnings

# DesignView estructura
$ ls source/arquitectura-tecnica/design-view/access/
assignment-lifecycle.rst
bounded-context.rst
index.rst
interaction-pattern.rst
separation-check-flow.rst

# ImplementationView estructura
$ ls source/arquitectura-tecnica/implementation-view/
access/  admin/  alerts/  audit/  auth/
impl-caller.rst  impl-operator.rst  impl-supervision.rst
index.rst  logs/  permissions/  pipeline/  reports/  users/

# 0 refs viejas
$ grep -rE "design-view/[a-z]+/(class|sequence|state|activity)\b" source/
(empty)
```

### Conteo total

- 31 git mv en DesignView (rename retroactivo)
- 10 git mv en ImplementationView (impl-X → modulo/layer-structure)
- 10 archivos nuevos: 10 module index.rst en ImplementationView
- 1 archivo nuevo: uml-14/relaciones-dependencia-iact.rst
- 2 archivos rewrite: implementation-view/index.rst v3.0.0,
  uml-14/index.rst (toctree update)
- ~40+ updates de cross-refs (seealso + toctrees)
- **Total: ~95 cambios + 11 archivos nuevos**

### Commits del WP

1. (este commit) — todo el batch del WP

### Roadmap status

| WP | Estado |
|---|---|
| design-view-restructure (precedente) | ✅ Completado |
| implementation-view-restructure + uml-14 doc + DesignView rename retroactivo | ✅ Completado |

Proximas vistas Kruchten 4+1 a abordar segun el DAG ya
documentado en `uml-14/relaciones-dependencia-iact.rst`:
- ProcessView → requiere UseCaseView ✓ + DesignView ✓
- DeployView → requiere UseCaseView ✓ + ImplementationView ✓

### Refs

- WP `design-view-restructure` (precedente).
- CLEAN_CODE_NAMING_PRINCIPLES.md §6.2 — principio que motiva
  el rename retroactivo.
- `uml-14/relaciones-dependencia-iact.rst` v1.0.0 (creado en
  este WP).
