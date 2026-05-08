```yml
project: IACT-docs
work_package: 2026-05-08-17-51-36-design-view-restructure
created_at: 2026-05-08 17:51:36
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (33 archivos a reorganizar + ~31 cross-refs entrantes a actualizar + 10 nuevos index.rst de modulo)
target: Restructurar `source/arquitectura-tecnica/design-view/` de archivos planos a directorios por modulo, siguiendo la convencion ya establecida en `use-case-view/`. Cada modulo gana su `index.rst` (caja Kruchten 4+1 — DesignView), con `class.rst`, `sequence.rst`, y opcionalmente `state.rst` / `activity.rst`.
predecessor_wp: 2026-05-08-04-10-27-uc-view-domain-alignment (cerrado)
trigger: directiva del ejecutor "abre un WP con ese scope antes de continuar"
```

# WP — Design-View restructure (cajas por modulo)

## Phase 1 — DISCOVER (consolidado)

### Decision SP-D1 resuelta — caller, operator, supervision

**Hallazgo del DISCOVER profundo:** el archivo
`design-view/index.rst` v3.1.0 ya documenta explicitamente:

> "Scope de implementacion: los modulos MOD_Operator,
> MOD_Supervision y MOD_Caller estan documentados en
> use-case-view/ como vista de requisitos pero **NO entran
> en este DesignView**. Su construccion queda diferida a WP
> futuros si/cuando se decida implementarlos."

**Resolucion:** la directiva del ejecutor de excluir caller
es **correcta** y consistente con el scope ya documentado.
Mi flag inicial sobre "caller Vigente" era una observacion
basada solo en el cluster index de use-case-view; no
contemplaba la decision de scope ya tomada en design-view.

- Scope DesignView: 10 modulos (access, admin, alerts,
  audit, auth, logs, permissions, pipeline, reports,
  users).
- Excluidos por scope: caller (externo IVR — no se diseña
  internamente), operator y supervision (deferidos).

**SP-D1 cerrado: Opcion A confirmada por el corpus mismo.**

### Estado actual de `design-view/` (33 archivos planos)

| Categoria | Cuenta | Archivos |
|---|---|---|
| Indice + overview | 2 | `index.rst` v3.1.0 (con toctree explicito a las 4 categorias actuales), `package-overview.rst` |
| `class-<modulo>.rst` | 10 | access, admin, alerts, audit, auth, logs, permissions, pipeline, reports, users |
| `seq-<modulo>.rst` | 10 | mismos 10 modulos |
| `state-*.rst` (transversales) | 5 | alert-event, assignment, export-job, pipeline-execution, session |
| `act-*.rst` (transversales) | 6 | alert-evaluation, etl-pipeline-execution, export-async, jwt-auth, rbac-effective-set-eval, validacion-separacion |

Tamaño promedio: 80–100 lineas. Contenido sustantivo
(no son stubs).

### Pattern de "caja" verificado en use-case-view

Sample `use-case-view/access/index.rst` v2.0.0:

```
1. meta block (artefacto, tipo, modulo, estado, version)
2. titulo "MOD_Access — Asignacion de Accesos: UC por Modulo"
3. intro paragraph (vista funcional, scope, hipotesis arquitectonica)
4. UML panoramico (diagrama del modulo con actores, UCs y relaciones <<extend>>)
5. seccion "Lectura del diagrama" (interpretacion narrativa)
6. seccion "Clases canonicas que materializan los UCs" (lista de :doc: a domain-model)
7. tabla de UCs del modulo con :doc: a spec textual y a diagrama individual
```

### Pattern equivalente para design-view module index

Adaptado al rol de DesignView:

```
1. meta block (artefacto, tipo: Design View — Module Box,
   modulo, estado, version)
2. titulo "Design View — MOD_X: Vista de Diseño"
3. intro paragraph (rol del modulo en la arquitectura,
   relacion con UCs)
4. UML panoramico CURATED (subset del class.rst con foco
   en relaciones inter-modulo y entidades centrales — no
   duplica class.rst sino que da vista de "que veo cuando
   abro la caja")
5. seccion "Lectura del diagrama" (narrativa de relaciones)
6. seccion "Clases canonicas" (link a domain-model)
7. toctree a class.rst, sequence.rst, state.rst (si aplica),
   activity.rst (si aplica)
8. seealso a use-case-view del modulo + design-view raiz
```

### Mapeo CONFIRMADO de transversales a modulos

Verificado contra el contenido de cada `state-*.rst` y
`act-*.rst` (no inferencia, lectura literal de la
seccion "Cubre los UCs..."):

| Archivo actual | "Cubre" segun el archivo | Destino confirmado |
|---|---|---|
| `state-assignment.rst` | Assignment (entidad RBAC) | `access/state.rst` |
| `state-alert-event.rst` | AlertEvent | `alerts/state.rst` |
| `state-export-job.rst` | ExportJob (UC_RPT_04 + UC_LOG_04) | `reports/state.rst` |
| `state-session.rst` | Session (auth) | `auth/state.rst` |
| `state-pipeline-execution.rst` | PipelineExecution (UC_PIP_01/02) | `pipeline/state.rst` |
| `act-validacion-separacion.rst` | "UC_ACC_01, UC_ACC_03, UC_PERM_03" | `access/activity.rst` |
| `act-rbac-effective-set-eval.rst` | "UC_PERM_07, UC_PERM_03 + gateway checks" | `permissions/activity.rst` |
| `act-jwt-auth.rst` | "UC_AUTH_01, UC_AUTH_05" | `auth/activity.rst` |
| `act-etl-pipeline-execution.rst` | "UC_PIP_01, UC_PIP_02" | `pipeline/activity.rst` |
| `act-alert-evaluation.rst` | "UC_ALR_01..05" | `alerts/activity.rst` |
| `act-export-async.rst` | "UC_RPT_04, UC_LOG_04" | `reports/activity.rst` |

**Cambio respecto al DISCOVER inicial:**

- `act-validacion-separacion` antes → admin/activity; ahora
  → `access/activity` (correcto: el archivo dice "antes de
  cualquier mutacion RBAC" y cubre UC_ACC_*; admin solo
  gestiona el catalogo de SeparationRules, no la
  verificacion runtime).
- `state-export-job` antes → audit/state; ahora →
  `reports/state` (el archivo cubre UC_RPT_04 + UC_LOG_04;
  audit no aparece en su seccion "Cubre"). Si el ejecutor
  prefiere audit/state por agrupacion conceptual, ajustar
  en PLAN.

### Distribucion final por modulo

| Modulo | index | class | sequence | state | activity | Total |
|---|---|---|---|---|---|---|
| access | NUEVO | mv | mv | mv (assignment) | mv (validacion-separacion) | 5 |
| admin | NUEVO | mv | mv | — | — | 3 |
| alerts | NUEVO | mv | mv | mv (alert-event) | mv (alert-evaluation) | 5 |
| audit | NUEVO | mv | mv | — | — | 3 |
| auth | NUEVO | mv | mv | mv (session) | mv (jwt-auth) | 5 |
| logs | NUEVO | mv | mv | — | — | 3 |
| permissions | NUEVO | mv | mv | — | mv (rbac-effective-set-eval) | 4 |
| pipeline | NUEVO | mv | mv | mv (pipeline-execution) | mv (etl-pipeline-execution) | 5 |
| reports | NUEVO | mv | mv | mv (export-job) | mv (export-async) | 5 |
| users | NUEVO | mv | mv | — | — | 3 |
| **Subtotal modulos** | **10 nuevos** | **10 mv** | **10 mv** | **5 mv** | **6 mv** | **41 archivos** |
| Top-level: `index.rst` | update | | | | | 1 |
| Top-level: `package-overview.rst` | sin cambio (verificar refs) | | | | | 1 |
| **Total post-EXECUTE** | | | | | | **43 archivos** |

### Cross-refs entrantes (R-01)

`grep` retorna **31 references** unicas a archivos
`design-view/<archivo plano>` desde otros documentos:

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
... (+ 16 mas con 1 ref cada uno)
```

**Riesgo R-01:** romper estas refs implica strict build con
"unknown document" warnings y EXIT≠0. Mitigacion: cada
rename `git mv` se acompaña de un sed scoped que actualiza
todas las refs entrantes a la nueva ruta. Patron:

```
old: :doc:`/arquitectura-tecnica/design-view/class-access`
new: :doc:`/arquitectura-tecnica/design-view/access/class`
```

Cantidad de archivos referrers (no refs): 33 archivos
distintos contienen al menos una ref. Algunos se pueden
agrupar por mismo bloque sed.

Ademas el archivo `design-view/index.rst` mismo contiene
toctree con los archivos viejos — debe re-generarse al
nuevo formato.

### Cross-refs internos en archivos design-view (R-02)

Cada uno de los 33 archivos design-view tiene seccion
`.. seealso::` que linkea a otros design-view. Por ejemplo
`state-assignment.rst:67-69`:

```
- :doc:`/arquitectura-tecnica/design-view/seq-access`
- :doc:`/arquitectura-tecnica/design-view/act-validacion-separacion`
- :doc:`/arquitectura-tecnica/design-view/act-rbac-effective-set-eval`
```

Cuando se hace `git mv state-assignment.rst access/state.rst`,
estos seealso internos tambien deben re-targetarse a las
nuevas rutas:

```
- :doc:`/arquitectura-tecnica/design-view/access/sequence`
- :doc:`/arquitectura-tecnica/design-view/access/activity`
- :doc:`/arquitectura-tecnica/design-view/permissions/activity`
```

**Conteo de seealso internos:** ~30-40 cross-refs internos
adicionales a actualizar (estimacion sin contar exacto —
verificable con grep en PLAN).

### Conteo global

| Categoria | Cuenta |
|---|---|
| Renames `git mv` | 31 (10 class + 10 seq + 5 state + 6 act) |
| `index.rst` nuevos por modulo | 10 |
| `design-view/index.rst` toctree update | 1 |
| `package-overview.rst` (verificar refs internas) | 1 |
| Cross-refs entrantes (R-01) actualizables via sed | 31 refs en 33 archivos referrers |
| Cross-refs internos design-view→design-view (R-02) | ~30-40 seealso |
| **Total cambios estimados** | **~75-85 cambios** |
| **Archivos nuevos** | **10** |

### Decisiones pendientes refinadas (post-deep-dive)

- ~~**D1 caller**~~ → CERRADO. Opcion A (excluir) confirmada
  por scope ya documentado en `design-view/index.rst`.
- **D2 mapping de transversales** → Confirmado por lectura
  literal del contenido. Excepcion: `state-export-job`
  propuesto a `reports/` (vs audit/) — el ejecutor puede
  ajustar si prefiere agrupacion conceptual distinta.
- **D3 contenido de cada `<modulo>/index.rst`** →
  Propuesta refinada: 7 secciones siguiendo el pattern
  use-case-view (meta, titulo, intro, UML panoramico
  curated, lectura, clases canonicas, toctree a sub-files,
  seealso). Cada index ~50-70 lineas.

### Stopping points

- **SP-D1:** ~~caller~~ → cerrado.
- **SP-D2:** revisar mapeo de transversales (especialmente
  `state-export-job` → reports vs audit). Confirmar antes de
  ejecutar.
- **SP-D3:** revisar pattern de contenido del index del
  modulo antes de generar los 10. Una vez validado el
  pattern en 1 modulo, replicar.
- **SP-D4:** verificacion build strict EXIT=0 tras EXECUTE.

## Refs

- WP `uc-view-domain-alignment` (precedente): patron de
  cajas por modulo establecido en use-case-view.
- WP `kruchten-view-diagram-types` (historico): aplicacion
  de Kruchten 4+1 al corpus.
- `design-view/index.rst` v3.1.0: scope de DesignView que
  resuelve SP-D1.

## Artefactos discover

- `discover/incoming-refs.txt` — 31 cross-refs entrantes
  unicas.

## Pendiente para Phase 8 PLAN

1. Producir task plan atomico T-NNN — cada task es un
   bloque que combina `git mv` + sed para refs entrantes
   y seealso internos del mismo archivo.
2. Generar el pattern del module index.rst en el primer
   modulo (e.g., access/index.rst) y validar antes de
   replicar a los otros 9.
3. Ejecutar todo en bloques por modulo (atomicidad por
   modulo) → 10 commits + 1 actualizacion de
   design-view/index.rst raiz + 1 cierre TR.
