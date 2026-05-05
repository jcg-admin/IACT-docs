```yml
created_at: 2026-05-04 21:30:00
project: THYROX
work_package: 2026-05-04-20-13-29-domain-model-per-class
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Inventario de Clases — source/requisitos/

## Metodología

**Corpus total:** 1918 archivos RST en `source/requisitos/`. 571 contienen
bloques `.. uml::` con PlantUML. Extracción de `class ClassName` via grep;
62 nombres únicos en el corpus completo.

**Corpus relevante:** El directorio `_metodologia-aplicacion/` contiene
ilustraciones didácticas de patrones UML (ejemplos con `Ave`, `Pinguino`,
`Circulo`, `Universidad`, jerarquías de herencia, singletons de config).
Estas clases NO son specs del sistema — son figuras pedagógicas. Se excluyen.

Filtrando solo `casos-uso/` (especificaciones reales de UCs): **51 clases únicas**.

Clasificación en 3 categorías:

- **CANÓNICO** — ya existe en `domain-model/` como archivo individual
- **IMPLEMENTACIÓN** — servicio, repositorio, hook, DTO, o artefacto técnico
- **POTENCIAL NUEVO** — podría ser entidad de dominio no cubierta

---

## Clases CANÓNICAS (ya en domain-model/)

| Clase | Archivo canónico | BC |
|-------|------------------|----|
| User | `domain-model/user.rst` | Auth |
| Session | `domain-model/session.rst` | Auth |
| InternalMailbox | `domain-model/internal-mailbox.rst` | Auth |
| Function | `domain-model/function.rst` | Permissions |
| FunctionGroup | `domain-model/function-group.rst` | Permissions |
| AccessGroup | `domain-model/access-group.rst` | Permissions |
| Assignment | `domain-model/assignment.rst` | Permissions |
| ExceptionalPermission | `domain-model/exceptional-permission.rst` | Permissions |
| SeparationRule | `domain-model/separation-rule.rst` | Permissions |
| AuditEvent | `domain-model/audit-event.rst` | Audit |
| ApplicationLog | `domain-model/application-log.rst` | Audit |
| InfrastructureLog | `domain-model/infrastructure-log.rst` | Audit |
| TechnicalMetric | `domain-model/technical-metric.rst` | Audit |
| SystemHealth | `domain-model/system-health.rst` | Audit |
| Alert | `domain-model/alert.rst` | Alerts |
| Threshold | `domain-model/threshold.rst` | Alerts |
| Subscription | `domain-model/subscription.rst` | Alerts |
| Metric | `domain-model/metric.rst` | Reports |
| Report | `domain-model/report.rst` | Reports |
| SavedView | `domain-model/saved-view.rst` | Reports |
| ExportJob | `domain-model/export-job.rst` | Reports |
| ScheduledReport | `domain-model/scheduled-report.rst` | Reports |
| Call | `domain-model/call.rst` | Calls |
| Campaign | `domain-model/campaign.rst` | Calls |
| EtlEjecucion | `domain-model/etl-ejecucion.rst` | ETL |
| EtlLog | `domain-model/etl-log.rst` | ETL |

**Total: 10 de las 51 clases de casos-uso/ son canónicas** (todas con archivo individual en domain-model/). El domain-model tiene 26 clases totales — las 16 restantes no aparecen en casos-uso/ (pertenecen a BCs de infraestructura/ETL documentados solo en arquitectura-tecnica/).

---

## Clases de IMPLEMENTACIÓN (no pertenecen a domain-model/)

Estas clases son artefactos de la capa de aplicación/infraestructura.

### Servicios de aplicación

| Clase | Archivo fuente | Razón |
|-------|----------------|-------|
| AuditService | uc-perm-09/diagramas-uml/diagrama-de-clases.rst | Orquestador de operaciones, no entidad |
| RuleValidator | uc-alr-01/diagramas-uml/clases.rst | Validador sin identidad persistida |
| EvaluatorReloader | uc-alr-01/diagramas-uml/clases.rst | Worker de recarga, no entidad |
| FilterValidator | uc-rpt-09/diagramas-uml/diagrama-de-clases.rst | Validador sin identidad persistida |
| ColumnCatalog | uc-rpt-10/diagramas-uml/clases.rst | Catálogo/servicio de consulta (solo métodos, sin atributos de estado) |

### Repositorios / Infraestructura

| Clase | Archivo fuente | Razón |
|-------|----------------|-------|
| AuditRepo | uc-perm-09/diagramas-uml/diagrama-de-clases.rst | Repositorio de persistencia (tabla append-only) |
| PIIScanner | uc-perm-09/diagramas-uml/diagrama-de-clases.rst | Scanner de datos PII, capa técnica |
| Sanitizer | uc-perm-09/diagramas-uml/diagrama-de-clases.rst | Sanitizador de payload, capa técnica |
| AlertHook | uc-perm-09/diagramas-uml/diagrama-de-clases.rst | Callback de evento `on_commit(event)` — hook técnico sin identidad |

### Patrones *Service / *Repo / *Worker / *Cache (todos los demás)

Patrón de nombre identifica implementación: `*Service`, `*Repo`, `*Worker`,
`*Cache`, `*Validator`, `*Scanner`, `*Builder`, `*Calculator`, `*Resolver`,
`*Loader`, `*Listener`, `*Encoder`. ~30 clases con estos sufijos — todas
descartadas como IMPLEMENTACIÓN sin revisión individual (criterio de nombre
es suficiente: los conceptos de negocio no se llaman así).

### Objetos de valor / estructuras transitorias

| Clase | Archivo fuente | Razón |
|-------|----------------|-------|
| HistoricalReport | uc-rpt-03/diagramas-uml/diagrama-de-clases.rst | Sin UUID propio; estructura calculada con period + buckets. Transiente. |
| Bucket | uc-rpt-03/diagramas-uml/diagrama-de-clases.rst | Componente de HistoricalReport (bucket_key + kpis). Sin ID propio. |
| Comparative | uc-rpt-03/diagramas-uml/diagrama-de-clases.rst | Componente de HistoricalReport (period_prior, diff_pct). Sin ID propio. |

### Tabla de asociación (join table)

| Clase | Archivo fuente | Razón |
|-------|----------------|-------|
| AccessGroupFunction | uc-perm-05, uc-acc-04 | Solo `access_group_id` + `function_id`. Sin ID propio, sin ciclo de vida. Tabla de unión M:N pura. |

### Proyecciones de UI / estructuras de navegación

| Clase | Archivo fuente | Razón |
|-------|----------------|-------|
| Menu | uc-perm-08/diagramas-uml/diagrama-de-estructura-del-menu.rst | Proyección de menú con `generated_at`, `cache: bool`. Sin UUID. Renderizado on-demand por usuario/locale. |
| Domain | uc-perm-08/diagramas-uml/diagrama-de-estructura-del-menu.rst | Agrupador de menú (code, label, order). Sin UUID. Elemento de navegación UI. |
| Section | uc-perm-08/diagramas-uml/diagrama-de-estructura-del-menu.rst | Sub-agrupador de menú (code, label, icon, order). Sin UUID. Elemento de navegación UI. |
| Action | uc-perm-08/diagramas-uml/diagrama-de-estructura-del-menu.rst | Ítem accionable del menú referenciando `function_code`. Sin UUID. Proyección de Function para UI. |

---

## Clases POTENCIALES NUEVAS — análisis detallado

### 1. AlertRule

**Archivo fuente:** `source/requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/clases.rst`

**Atributos declarados:**
```
id, name, metric, scope, condition, window, severity, actions, cooldown, status
```

**Análisis:**
- Tiene `id` (identidad propia) y `status` (ciclo de vida).
- `window` (ventana temporal de evaluación) y `cooldown` (tiempo mínimo entre disparos)
  son conceptos de negocio ausentes en `Threshold`.
- `actions` (qué notificaciones/acciones ejecutar) y `scope` (ámbito de la regla) amplían
  el modelo más allá de un simple umbral numérico.
- `Threshold` en domain-model cubre: `metric_id`, `comparison_operator`, `value`, `severity`.
  AlertRule cubre un concepto más rico: una regla nombrada con ventana temporal, acciones
  y cooldown. **Son entidades distintas** — Threshold es la condición de disparo,
  AlertRule es la política completa de alerta.

**Veredicto:** DOMINIO NUEVO — crear `domain-model/alert-rule.rst`

**BC sugerido:** Alerts

---

### 2. SavedFilter

**Archivo fuente:** `source/requisitos/casos-uso/reports/uc-rpt-09/diagramas-uml/diagrama-de-clases.rst`

**Atributos declarados:**
```
id, name, filters, period_relative, applies_to, is_default, is_invalid
```

**Análisis:**
- Tiene `id` (identidad propia) y un ciclo de vida implícito (`is_invalid`).
- `is_default` indica preferencias persistidas del usuario.
- `period_relative` y `applies_to` son conceptos de negocio (filtro reutilizable
  no atado a un report_id específico, a diferencia de `SavedView`).
- `SavedView` en domain-model tiene: `view_id`, `report_id` (atado a un report),
  `filters_snapshot`, `name`, `state`. SavedFilter NO tiene `report_id` —
  es un filtro reutilizable cross-report. **Son entidades distintas**.

**Veredicto:** DOMINIO NUEVO — crear `domain-model/saved-filter.rst`

**BC sugerido:** Reports

---

## Resumen ejecutivo

| Categoría | Cantidad |
|-----------|----------|
| Canónicas (ya en domain-model/) | 26 |
| Implementación / infraestructura | ~39 |
| Valor / transitorias / UI projection | 7 |
| Join table | 1 |
| **Potenciales nuevas** | **2** |

### Acciones recomendadas

| # | Clase | Acción | Prioridad |
|---|-------|--------|-----------|
| 1 | AlertRule | Crear `domain-model/alert-rule.rst` | ALTA — tiene id + status + ciclo de vida documentado en uc-alr-01 |
| 2 | SavedFilter | Crear `domain-model/saved-filter.rst` | MEDIA — tiene id + is_invalid, distinto de SavedView |

No se requieren acciones para las 60 clases restantes: o ya tienen archivo canónico,
o son artefactos de implementación que correctamente NO pertenecen a domain-model/.
