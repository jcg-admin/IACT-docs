```yml
created_at: 2026-05-08 04:25:00
project: IACT-docs
work_package: 2026-05-08-04-10-27-uc-view-domain-alignment
phase: Phase 2 — MEASURE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Phase 2 MEASURE — alignment quantitatives

Ejecuta las decisiones D1, D2 y D3 del DISCOVER. Mide volumenes
antes de proponer Phase 3 ANALYZE / Phase 6 PLAN.

## D3 — Cross-ref UCs ↔ domain-model (resultado de la medicion)

### M-01: Clases referenciadas vs definidas

| Metrica | Valor |
|---|---|
| Clases definidas en `domain-model/` (todas las apariciones) | 189 |
| Clases definidas en archivos canonicos (1 archivo = 1 clase principal) | 109 |
| Clases referenciadas desde class-diagrams de UCs | 40 |
| Clases UC NO definidas en DM | **1** |
| Clases con case mismatch UC vs DM | **1** |
| Clases en DM con miembros faltantes vs UC | **12** |
| Total miembros faltantes (atributos + metodos) | **29** |

### M-02: Clase faltante en DM

| Clase usada en UC | Estado | UCs afectados |
|---|---|---|
| `MenuIVRReportService` | NO existe en DM | uc-rpt-16 (probable) |

**Decision pendiente:** crear `menu-ivr-report-service.rst` o
verificar si el UC debe usar `IVRNavigationReportService`
(existente, similar nombre) vs crear nuevo servicio.

### M-03: Case mismatch

| UC name | DM name | Archivos a alinear |
|---|---|---|
| `PiiScanner` | `PIIScanner` | UC files que usan camelCase |

Convencion del proyecto: `PIIScanner` (acronimo en
mayusculas). Recomendacion: corregir las refs UC.

### M-04: Miembros faltantes por clase (29 totales)

| Clase | Archivo canonico | Miembros faltantes (n) | UC origen |
|---|---|---|---|
| `AccessGroup` | access-group.rst | 4 (id, agr_code, is_system, state) | uc-acc-04 |
| `AgentReportService` | agent-report-service.rst | 1 (list) | uc-rpt-12 |
| `AlertRule` | alert-rule.rst | 2 (id, state) | uc-alr-01 |
| `AuditRepo` | audit-repo.rst | 1 (query) | uc-aud-01 |
| `ErroresETLService` | errores-etl-service.rst | 1 (listar) | uc-pip-02 |
| `EvaluatorReloader` | evaluator-reloader.rst | 1 (reload) | uc-alr-01 |
| `PipelineExecutionRepo` | pipeline-execution-repo.rst | 3 (ejecuciones_recientes, por_estado, ultima_ejecucion) | uc-pip-01, uc-pip-02 |
| `RBACRepo` | rbac-repo.rst | 2 (get_user_segments, has_global_capability) | uc-inc-rpt-01 |
| `SavedView` | saved-view.rst | 6 (chart_config, columns, filters, id, owner, report_type) | uc-rpt-10 |
| `SegmentResolver` | segment-resolver.rst | 2 (invalidate_cache, is_global) | uc-inc-rpt-01 |
| `Subscription` | subscription.rst | 5 (channel, id, rule, scope, user) | uc-alr-05 |
| `User` | user.rst | 1 (segment_id) | uc-acc-04 |

**Patron observado:** los miembros faltantes son
mayoritariamente **atributos basicos** (id, state, channel,
columns, etc.) que el UC asume existir para mostrar la
estructura del agregado, mientras la DM canonica fue escrita
mas concisa. No hay metodos sofisticados nuevos — las firmas
faltantes son mayormente de naming basico.

**Estimacion ediciones D3:** 12 archivos a editar agregando
los 29 miembros declarados en UCs. Trabajo focalizado.

## D2 — Verificacion uml-07 profunda

### M-05: Conformidad estructural y pragmatica

| Criterio uml-07 | Conformidad |
|---|---|
| `actor` (stick figure) | 88/88 ✅ |
| `usecase` (elipse) | 88/88 ✅ |
| `rectangle "Sistema" { ... }` | 88/88 ✅ |
| `left to right direction` | **85/88** — faltan uc-usr-05/06/07 |
| `<<include>>` cuando aplica | 85/88 ✅ |
| `<<extend>>` cuando aplica | 27/88 ✅ |

Los 3 archivos sin `left to right direction` son **los mismos
3 UCs Reservado** (uc-usr-05/06/07). La asimetria del
DISCOVER (F-01 + F-03) se confirma: estos 3 view files fueron
creados como minimos placeholders sin convenciones uml-07
completas.

### M-06: Convencion de actores con nombre de funcion RBAC

Distribucion de actor names (top 20 / total 164):

```
63  AuthorizationGuard       ← componente sistema (initiator interno)
46  view_audit_log           ← funcion RBAC (correcta)
43  AuditService             ← componente sistema
20  SegmentResolver          ← componente sistema
19  PermissionCache          ← componente sistema
...
10  view_reports             ← funcion RBAC (correcta)
10  Caller                   ← actor humano
 9  Session                  ← entidad (actor secundario)
 8  UserRepo                 ← componente sistema
...
```

**Observacion:** la convencion uml-07 / STD-010 §4 D-DIAG-001
para actores RBAC dice "el actor SI usa el nombre exacto de la
funcion RBAC del catalogo" (e.g., `view_reports`,
`view_audit_log`). Esta convencion se aplica solamente cuando
el actor representa al "operador autorizado por funcion X".

Los `AuthorizationGuard`, `AuditService`, `SegmentResolver`,
`PermissionCache` son **componentes del sistema** declarados
como `actor` por convencion plantuml (initiator). Esto es
practica documentada del proyecto y no contradice uml-07.

**Conclusion D2:** sin violacion sistematica. Los 3 unicos
casos donde falta `left to right direction` (uc-usr-05/06/07)
quedan cubiertos por el trabajo de D1.

**Estimacion ediciones D2:** 0 (los gaps coinciden con D1).

## D1 — UCs Reservado uc-usr-05/06/07

### M-07: Estado actual

Cada UC Reservado tiene **solo 1 archivo** (`index.rst`)
con frontmatter `:estado: Reservado` y `:version: 0.1.0`.
Necesitan estructura completa Larman:

| Archivo | uc-usr-05 | uc-usr-06 | uc-usr-07 |
|---|---|---|---|
| `index.rst` | ✅ stub Reservado | ✅ stub Reservado | ✅ stub Reservado |
| `informacion-general.rst` | ❌ | ❌ | ❌ |
| `actores-precondiciones.rst` | ❌ | ❌ | ❌ |
| `flujo-principal.rst` | ❌ | ❌ | ❌ |
| `flujos-alternos.rst` | ❌ | ❌ | ❌ |
| `excepciones.rst` | ❌ | ❌ | ❌ |
| `criterios-aceptacion.rst` | ❌ | ❌ | ❌ |
| `datos-involucrados.rst` | ❌ | ❌ | ❌ |
| `patrones-diseno.rst` | ❌ | ❌ | ❌ |
| `requisitos-no-funcionales.rst` | ❌ | ❌ | ❌ |
| `implementacion-tecnica.rst` | ❌ | ❌ | ❌ |
| `testing.rst` | ❌ | ❌ | ❌ |
| `diagramas-uml/index.rst` | ❌ | ❌ | ❌ |
| `diagramas-uml/diagrama-de-caso-de-uso.rst` | ❌ | ❌ | ❌ |
| `diagramas-uml/diagrama-de-secuencia.rst` | ❌ | ❌ | ❌ |
| `diagramas-uml/diagrama-de-actividad.rst` | ❌ | ❌ | ❌ |
| `diagramas-uml/notas-sobre-los-diagramas.rst` | ❌ | ❌ | ❌ |
| **Total faltantes por UC** | **16** | **16** | **16** |

**Estimacion ediciones D1:** 48 archivos nuevos (3 × 16).

Tambien actualizar 3 view files para que usen
`left to right direction` y queden alineados al estandar
uml-07 cuando se elaboren las specs textuales.

## Estimacion total de Phase 6 PLAN / Phase 10 EXECUTE

| Decision | Trabajo | Archivos afectados | Cuenta |
|---|---|---|---|
| D1 ruta A | Crear specs Larman para 3 UCs | nuevos en `casos-uso/users/uc-usr-{05,06,07}/` | 48 |
| D1 alineacion | Actualizar view files al estandar | 3 view files | 3 |
| D2 (cubierto por D1) | — | — | 0 |
| D3 — class faltante | Crear `menu-ivr-report-service.rst` o reasignar | 0-1 | 0-1 |
| D3 — case mismatch | Corregir `PiiScanner` → `PIIScanner` en UCs | refs UC | ~5 |
| D3 — miembros faltantes | Editar 12 archivos DM agregando 29 miembros | 12 | 12 |
| **Total estimado** | — | — | **~68-69 ediciones** |

## Riesgos identificados

- **R-01:** Las definiciones de DM y UC pueden tener semantica
  divergente intencional (e.g., DM usa `agr_id`, UC usa `id`
  como UUID interno). Antes de "agregar miembros faltantes" hay
  que verificar caso por caso si el miembro UC es **adicion**
  (faltante real) o **renombrado** (semantica equivalente).
- **R-02:** `MenuIVRReportService` puede ser typo o renombramiento
  pendiente de `IVRNavigationReportService`. Decidir antes de
  crear archivo nuevo.
- **R-03:** Los 48 archivos nuevos para uc-usr-05/06/07 deben
  tener referencias semanticas correctas a otros UCs (uc-auth-03,
  04, 05 segun el frontmatter Reservado los menciona). Coherencia
  con UCs existentes requerida.

## Decisiones pendientes para Phase 6 PLAN

- **D4:** caso-por-caso de los 29 miembros — ¿son adiciones reales
  o son inconsistencias de naming entre UC y DM?
- **D5:** trato de `MenuIVRReportService` — alias de
  `IVRNavigationReportService` o servicio nuevo?
- **D6:** orden de ejecucion sugerido — D3 primero (12 ediciones
  focales) → D1 (48 archivos nuevos) → cierre.

## Artefactos measure

- `measure/domain-model-catalog.txt` — catalogo de 189
  definiciones de clase con sus miembros.
- `measure/uc-class-method-usage.txt` — uso por clase desde
  UC UML files (clases + dotted access).
- `measure/cross-ref-gaps-v2.txt` — gaps detallados con UCs
  origen.
- `measure/view-no-direction.txt` — 3 archivos.
- `measure/casos-uso-no-direction.txt` — 0 archivos.
- `measure/actors-distribution.txt` — 164 actores unicos.
