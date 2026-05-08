```yml
project: IACT-docs
work_package: 2026-05-08-17-51-36-design-view-restructure
created_at: 2026-05-08 17:51:36
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (33 archivos a reorganizar + ~30 cross-refs entrantes a actualizar)
target: Restructurar `source/arquitectura-tecnica/design-view/` de archivos planos a directorios por modulo, siguiendo la convencion ya establecida en `use-case-view/`. Cada modulo gana su `index.rst` (caja Kruchten 4+1 — DesignView), con `class.rst`, `sequence.rst`, y opcionalmente `state.rst` / `activity.rst`.
predecessor_wp: 2026-05-08-04-10-27-uc-view-domain-alignment (cerrado)
trigger: directiva del ejecutor "abre un WP con ese scope antes de continuar"
```

# WP — Design-View restructure (cajas por modulo)

## Phase 1 — DISCOVER

### Estado actual de `design-view/` (archivos planos)

33 archivos `.rst` directamente en el directorio:

| Categoria | Cuenta | Archivos |
|---|---|---|
| Indice + overview | 2 | `index.rst`, `package-overview.rst` |
| `class-<modulo>.rst` | 10 | access, admin, alerts, audit, auth, logs, permissions, pipeline, reports, users |
| `seq-<modulo>.rst` | 10 | mismos 10 |
| `state-*.rst` (transversales) | 5 | alert-event, assignment, export-job, pipeline-execution, session |
| `act-*.rst` (transversales) | 6 | alert-evaluation, etl-pipeline-execution, export-async, jwt-auth, rbac-effective-set-eval, validacion-separacion |

Tamaño promedio: 80–100 lineas por archivo. Contenido sustantivo
(no son stubs).

### Estado en `use-case-view/` (modelo a seguir)

13 modulos con directorio + index + UC files:

```
use-case-view/
  access/    {index.rst + 7 UC files}
  admin/     {index.rst + 5 UC files}
  alerts/    {index.rst + 5 UC files}
  audit/     {index.rst + 4 UC files}
  auth/      {index.rst + 5 UC files}
  caller/    {index.rst + 5 UC files}     ← Vigente
  logs/      {index.rst + 7 UC files}
  operator/  {index.rst + 10 UC files}    ← Reservado a nivel cluster
  permissions/ {index.rst + 10 UC files}
  pipeline/  {index.rst + 4 UC files}
  reports/   {index.rst + 16 UC files}
  supervision/ {index.rst + 3 UC files}   ← Reservado a nivel cluster
  users/     {index.rst + 7 UC files}
```

### Modulos en design-view actual: 10

**Cubre:** access, admin, alerts, audit, auth, logs, permissions,
pipeline, reports, users.

**Falta:** caller, operator, supervision.

### Discrepancia con el scope propuesto por el ejecutor

El ejecutor dice "Excluyendo `operator`, `supervision` y
`caller` que estan Reservados, igual que en use-case-view." —
**parcialmente correcto:**

| Cluster | Estado en `use-case-view/<cluster>/index.rst` |
|---|---|
| `operator` | **Reservado** ✓ — coincide |
| `supervision` | **Reservado** ✓ — coincide |
| `caller` | **Vigente** ⚠ — la afirmacion no aplica |

Caller es **Vigente** en use-case-view (5 UC files con spec
textual completa). Excluirlo de design-view crearia una
asimetria nueva: la unica vista Vigente sin contraparte de
diseño.

**Recomendacion:** confirmar antes de ejecutar si:

- **Opcion A:** strict-follow del ejecutor — excluir
  caller; design-view cubre 10 modulos (access, admin, alerts,
  audit, auth, logs, permissions, pipeline, reports, users).
  Aceptar la asimetria con la justificacion de que caller
  describe interaccion con sistema externo IVR (no requiere
  diseño de clases internas).
- **Opcion B:** incluir caller (que es Vigente) — design-view
  cubre 11 modulos. Trabajo adicional: crear
  `caller/index.rst`, `caller/class.rst`, `caller/sequence.rst`
  desde cero (~3 archivos nuevos sustantivos). La diferencia
  vs Opcion A es agregar 3 archivos.

Asumiendo Opcion A por simetria con la directiva. Marcar como
**SP-D1 (decision pendiente del ejecutor).**

### Estructura objetivo

```
design-view/
  index.rst               (existe, actualizar toctree)
  package-overview.rst    (existe, sin cambio)
  access/
    index.rst             ← caja del modulo (NUEVO)
    class.rst             ← contenido de class-access.rst (RENAME via git mv)
    sequence.rst          ← contenido de seq-access.rst
    state.rst             ← contenido de state-assignment.rst
  admin/
    index.rst
    class.rst
    sequence.rst
    activity.rst          ← contenido de act-validacion-separacion.rst
  alerts/
    index.rst
    class.rst
    sequence.rst
    state.rst             ← state-alert-event.rst
    activity.rst          ← act-alert-evaluation.rst
  audit/
    index.rst
    class.rst
    sequence.rst
    state.rst             ← state-export-job.rst
    activity.rst          ← act-export-async.rst
  auth/
    index.rst
    class.rst
    sequence.rst
    state.rst             ← state-session.rst
    activity.rst          ← act-jwt-auth.rst
  logs/
    index.rst
    class.rst
    sequence.rst
  permissions/
    index.rst
    class.rst
    sequence.rst
    activity.rst          ← act-rbac-effective-set-eval.rst
  pipeline/
    index.rst
    class.rst
    sequence.rst
    state.rst             ← state-pipeline-execution.rst
    activity.rst          ← act-etl-pipeline-execution.rst
  reports/
    index.rst
    class.rst
    sequence.rst
  users/
    index.rst
    class.rst
    sequence.rst
```

### Mapeo de archivos transversales a modulos

Cada `state-*` y `act-*` actual se asigna al modulo donde
pertenece su semantica:

| Archivo actual | Destino |
|---|---|
| `state-assignment.rst` | `access/state.rst` |
| `state-alert-event.rst` | `alerts/state.rst` |
| `state-export-job.rst` | `audit/state.rst` |
| `state-session.rst` | `auth/state.rst` |
| `state-pipeline-execution.rst` | `pipeline/state.rst` |
| `act-validacion-separacion.rst` | `admin/activity.rst` |
| `act-alert-evaluation.rst` | `alerts/activity.rst` |
| `act-export-async.rst` | `audit/activity.rst` |
| `act-jwt-auth.rst` | `auth/activity.rst` |
| `act-rbac-effective-set-eval.rst` | `permissions/activity.rst` |
| `act-etl-pipeline-execution.rst` | `pipeline/activity.rst` |

Nota: 5 modulos no tendran `state.rst` (admin, logs,
permissions, reports, users). Eso es OK — `state.rst` es
opcional y solo se crea si hay diagrama relevante.

Modulos sin `activity.rst`: access, logs, reports, users
(no hay actualmente).

### Cross-refs entrantes a verificar

`grep -rohE ':doc:.../design-view/[a-z-]+'` retorna **31
referencias unicas** a archivos `design-view/` desde otros
documentos del corpus.

Top-15 mas referenciados:

```
4 :doc:`design-view/state-pipeline-execution`
3 :doc:`design-view/state-export-job`
3 :doc:`design-view/state-alert-event`
3 :doc:`design-view/seq-reports`
3 :doc:`design-view/seq-pipeline`
3 :doc:`design-view/seq-auth`
3 :doc:`design-view/seq-alerts`
3 :doc:`design-view/seq-access`
3 :doc:`design-view/class-access`
2 :doc:`design-view/state-session`
2 :doc:`design-view/seq-permissions`
2 :doc:`design-view/class-reports`
2 :doc:`design-view/class-pipeline`
2 :doc:`design-view/class-permissions`
2 :doc:`design-view/class-auth`
```

**Riesgo:** si se renombran los archivos sin actualizar los
referrers, el strict build falla con "unknown document". El
plan incluye actualizacion de cross-refs en el mismo bloque
de cada rename.

### Nuevos archivos a crear

10 `index.rst` (uno por modulo) — el contenido sustantivo
de cada caja: titulo del modulo, una imagen panoramica del
modelo (subset del class-* existente con foco a las relaciones
clave), toctree a class/sequence/state/activity.

### Estimacion de scope

| Categoria | Cuenta | Naturaleza |
|---|---|---|
| Renames `git mv` | 26 (10 class + 10 seq + 5 state + 6 act, donde 1 act-validacion-separacion va a admin/activity) — **wait recount** | preserva contenido |
| Renames a aplicar | 21 (10 class + 10 seq + 5 state + 6 act = 31, pero 5 state ya cubren todos los estados, 6 act se distribuyen) → contar exacto | |
| `index.rst` por modulo nuevo | 10 | contenido sustantivo |
| Update `design-view/index.rst` toctree | 1 | reflejar nueva estructura |
| Update `package-overview.rst` (si tiene refs antiguas) | 0–1 | revisar |
| Cross-refs entrantes a actualizar | ~31 (en ~25 archivos referrers) | sed scoped |
| **Total** | **~50 cambios + 10 nuevos** | |

### Conteo verificado de renames

- 10 `class-<m>.rst` → `<m>/class.rst`
- 10 `seq-<m>.rst` → `<m>/sequence.rst`
- 5 `state-*.rst` → `<modulo>/state.rst`
- 6 `act-*.rst` → `<modulo>/activity.rst`
- **Subtotal renames:** 31

### Stopping points

- **SP-D1:** confirmar ejecutor sobre `caller/` —
  Opcion A (excluir) o B (incluir).
- **SP-D2:** revision del task plan antes de ejecutar.
- **SP-D3:** verificacion de cross-refs entrantes resueltas
  tras EXECUTE (build strict EXIT=0).

## Decisiones pendientes (D-XX)

- **D1:** caller incluir o excluir.
- **D2:** mapping de transversales a modulos (propuesta arriba —
  confirmar especialmente `state-assignment` → access vs
  permissions).
- **D3:** que va en cada `<modulo>/index.rst` — propuesta:
  resumen del modulo + diagrama panoramico de clases con
  relaciones clave + toctree a sub-archivos.

## Refs

- WP `uc-view-domain-alignment` (precedente): patron de cajas
  por modulo establecido en use-case-view.
- WP `kruchten-view-diagram-types` (historico): aplicacion de
  Kruchten 4+1 al corpus.

## Artefactos discover

- `discover/incoming-refs.txt` — 31 cross-refs entrantes
  unicas.
