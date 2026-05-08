```yml
created_at: 2026-05-08 04:45:00
project: IACT-docs
work_package: 2026-05-08-04-10-27-uc-view-domain-alignment
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Task plan — UC ↔ View ↔ Domain-Model alignment

Orden de ejecución (D6): D3a → D3b → D3c → D1 → D1 colateral.

## Bloque D3a — 14 renames en UCs (sed scoped)

Un task por archivo UC afectado. Renames combinados por archivo
(múltiples renames en el mismo class block del mismo archivo).

**Estrategia sed:** sustitución scoped al bloque
`class <ClassName> { ... }` para evitar matches espurios. Como
las renames son patrones específicos (e.g., `+ owner :` o
`+ owner ` al inicio de línea de class block), el sed se ancla
en el patrón de declaración de miembro (`^\s*+\s+old_name\b`).

Verificación: tras cada task, `grep -E "+ <new_name>"` el
archivo encuentra el miembro renombrado y `grep -E "+
<old_name>\b"` no lo encuentra dentro de class block.

---

- [ ] **T-001** | UC AccessGroup: rename `agr_code` → `agr_id`
  - Archivo: `source/requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst`
  - Sed (line-anchored): `s/^\(\s\+[+#-~]\s*\)agr_code\b/\1agr_id/`
  - Referencia DM: `AccessGroup.agr_id : String <<AGR-001..012>>`
  - Verificación: `grep -c '+ agr_id' archivo` ≥ 1 y `grep -c '+ agr_code' archivo` = 0

- [ ] **T-002** | UC AgentReportService: rename `list` → `get`
  - Archivo: `source/requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst`
  - Sed (line-anchored): `s/^\(\s\+[+#-~]\s*\)list\(\s*(\)/\1get\2/`
  - Referencia DM: `AgentReportService.get(invoker, period, filters)`
  - Verificación: `grep -c '+ get(' archivo` ≥ 1 y `grep -c '+ list(' archivo` = 0

- [ ] **T-003** | UC AlertRule: renames `id` → `rule_id` y `state` → `status`
  - Archivo: `source/requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst`
  - Sed:
    - `s/^\(\s\+[+#-~]\s*\)id\(\s*:\)/\1rule_id\2/`
    - `s/^\(\s\+[+#-~]\s*\)state\(\s*:\)/\1status\2/`
  - Referencia DM: `AlertRule.rule_id : UUID`, `AlertRule.status : RuleState`
  - Verificación: `grep -c '+ rule_id' archivo` ≥ 1, `grep -c '+ status' archivo` ≥ 1

- [ ] **T-004** | UC AuditRepo: rename `query` → `find`
  - Archivo: `source/requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/^\(\s\+[+#-~]\s*\)query\(\s*(\)/\1find\2/`
  - Referencia DM: `AuditRepo.find(filters, cursor, limit) : QueryResult`
  - Verificación: `grep -c '+ find(' archivo` ≥ 1

- [ ] **T-005** | UC EvaluatorReloader: rename `reload` → `reload_all`
  - Archivo: `source/requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/^\(\s\+[+#-~]\s*\)reload\(\s*(\s*)\)/\1reload_all\2/`
  - Referencia DM: `EvaluatorReloader.reload_all() : ReloadResult`
  - Verificación: `grep -c '+ reload_all(' archivo` ≥ 1
  - Nota: T-003 y T-005 tocan el mismo archivo — coordinar orden o ejecutar ambos en una sola pasada.

- [ ] **T-006** | UC ErroresETLService: rename `listar` → `query`
  - Archivo: `source/requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/^\(\s\+[+#-~]\s*\)listar\(\s*(\)/\1query\2/`
  - Referencia DM: `ErroresETLService.query(filters, ...)`
  - Verificación: `grep -c '+ query(' archivo` ≥ 1

- [ ] **T-007** | UC PipelineExecutionRepo (uc-pip-02): rename `por_estado` → `find_by_state`
  - Archivo: `source/requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/^\(\s\+[+#-~]\s*\)por_estado\b/\1find_by_state/`
  - Referencia DM: `PipelineExecutionRepo.find_by_state(state) : List<PipelineExecution>`
  - Nota: T-006 y T-007 tocan el mismo archivo.

- [ ] **T-008** | UC PipelineExecutionRepo (uc-pip-01): rename `ultima_ejecucion` → `last_successful_by_dataset`
  - Archivo: `source/requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/^\(\s\+[+#-~]\s*\)ultima_ejecucion\b/\1last_successful_by_dataset/`
  - Referencia DM: `PipelineExecutionRepo.last_successful_by_dataset(dataset)`
  - Decisión adicional: si UC también declara `ejecuciones_recientes` (este es ADD a DM, no rename),
    preservar esa línea; T-008 solo toca `ultima_ejecucion`.

- [ ] **T-009** | UC SavedView: renames `id` → `view_id`, `filters` → `filters_snapshot`, `owner` → `owner_user_id`
  - Archivo: `source/requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-clases.rst`
  - Sed:
    - `s/^\(\s\+[+#-~]\s*\)id\(\s*:\s*UUID\)/\1view_id\2/`
    - `s/^\(\s\+[+#-~]\s*\)filters\b/\1filters_snapshot/`
    - `s/^\(\s\+[+#-~]\s*\)owner\b/\1owner_user_id/`
  - Referencia DM: `SavedView.view_id`, `SavedView.filters_snapshot`, `SavedView.owner_user_id`
  - Verificación: `grep -cE '+ (view_id|filters_snapshot|owner_user_id)' archivo` = 3

- [ ] **T-010** | UC Subscription: renames `id` → `subscription_id`, `user` → `subscriber_user_id`, `rule` → `alert_id`
  - Archivo: `source/requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst`
  - Sed:
    - `s/^\(\s\+[+#-~]\s*\)id\(\s*:\s*UUID\)/\1subscription_id\2/`
    - `s/^\(\s\+[+#-~]\s*\)user\(\s*:\)/\1subscriber_user_id\2/`
    - `s/^\(\s\+[+#-~]\s*\)rule\(\s*:\)/\1alert_id\2/`
  - Referencia DM: `Subscription.subscription_id`, `Subscription.subscriber_user_id`, `Subscription.alert_id`

**Total D3a: 10 tasks (T-001..T-010), 8 archivos UC distintos, 14 renames.**

## Bloque D3b — 15 adds en domain-model

Un task por miembro agregado. Cada task edita el bloque
PlantUML `class <ClassName> { ... }` del archivo canónico,
añadiendo la línea de declaración antes de la sección `--`
(separador atributos/métodos) si es atributo, o después si es
método.

Verificación: tras cada task,
`grep -A30 "^class <Class>" archivo | grep -c "+ <member>"` ≥ 1.

---

- [ ] **T-011** | DM AccessGroup: add `id` (UUID PK)
  - Archivo: `source/arquitectura-tecnica/domain-model/access-group.rst`
  - Línea a agregar: `   + id : UUID                    <<technical PK>>`
  - Posición: antes de `+ agr_id`
  - Tipo: UUID, PK técnico separado de `agr_id` business code
  - Justificación: UC_ACC_04 referencia `id` como PK en agregación con FunctionGroupMembership

- [ ] **T-012** | DM AccessGroup: add `is_system` (Boolean)
  - Archivo: `source/arquitectura-tecnica/domain-model/access-group.rst`
  - Línea: `   + is_system : Boolean           <<true para AGR-001..012, false para custom>>`
  - Tipo: Boolean
  - Justificación: UC_ACC_04 distingue grupos de sistema (no modificables) de grupos custom

- [ ] **T-013** | DM AccessGroup: add `state` (AccessGroupState)
  - Archivo: `source/arquitectura-tecnica/domain-model/access-group.rst`
  - Línea: `   + state : AccessGroupState`
  - Adicionalmente declarar enum `AccessGroupState { ACTIVE, INACTIVE }` en el mismo @startuml
  - Justificación: UC_ACC_04 modela lifecycle ACTIVE/INACTIVE del AGR

- [ ] **T-014** | DM PipelineExecutionRepo: add `ejecuciones_recientes()` → renombrar a `find_recent`
  - Archivo: `source/arquitectura-tecnica/domain-model/pipeline-execution-repo.rst`
  - Línea: `   + find_recent(period : Period) : List<PipelineExecution>`
  - Nota: la UC declara nombre español `ejecuciones_recientes`; D4 dice ADD pero la convención
    de DM es inglés. Acción combinada: agregar `find_recent` a DM y renombrar UC `ejecuciones_recientes`
    → `find_recent` (compatible con D3a en una segunda pasada). Preferir `find_recent` en ambos lados.
  - Justificación: UC_PIP_01 solicita listar ejecuciones recientes (general)

- [ ] **T-015** | DM RBACRepo: add `get_user_segments(user_id)`
  - Archivo: `source/arquitectura-tecnica/domain-model/rbac-repo.rst`
  - Línea: `   + get_user_segments(user_id : UUID) : List<Segment>`
  - Justificación: UC_INC_RPT_01 requiere lista de segmentos del usuario para resolver scope

- [ ] **T-016** | DM RBACRepo: add `has_global_capability(user_id, capability)`
  - Archivo: `source/arquitectura-tecnica/domain-model/rbac-repo.rst`
  - Línea: `   + has_global_capability(user_id : UUID, capability : String) : Boolean`
  - Justificación: UC_INC_RPT_01 verifica si un user tiene capability global (distinto de admin global)

- [ ] **T-017** | DM SavedView: add `chart_config` (JSON)
  - Archivo: `source/arquitectura-tecnica/domain-model/saved-view.rst`
  - Línea: `   + chart_config : Map<String, Any>`
  - Justificación: UC_RPT_10 persiste configuración de chart (tipo, ejes, formato)

- [ ] **T-018** | DM SavedView: add `columns` (List<String>)
  - Línea: `   + columns : List<String>`
  - Justificación: UC_RPT_10 persiste set de columnas seleccionadas del catálogo del report_type

- [ ] **T-019** | DM SavedView: add `report_type` (ReportType)
  - Línea: `   + report_type : ReportType`
  - Justificación: UC_RPT_10 distingue el tipo del reporte (vs `report_id` que es el reporte concreto)

- [ ] **T-020** | DM SegmentResolver: add `invalidate_cache(user_id)`
  - Archivo: `source/arquitectura-tecnica/domain-model/segment-resolver.rst`
  - Línea: `   + invalidate_cache(user_id : UUID) : void`
  - Nota: DM tiene `cache : SegmentCache` (privado); este método público invalida segmentos del usuario
  - Justificación: UC_INC_RPT_01 invalida cache cuando el segmento cambia

- [ ] **T-021** | DM SegmentResolver: add `is_global(user_id)`
  - Línea: `   + is_global(user_id : UUID) : Boolean`
  - Justificación: UC_INC_RPT_01 distingue si el usuario tiene scope global vs segmentado

- [ ] **T-022** | DM Subscription: add `scope` (SubscriptionScope)
  - Archivo: `source/arquitectura-tecnica/domain-model/subscription.rst`
  - Línea: `   + scope : SubscriptionScope`
  - Justificación: UC_ALR_05 distingue subscripciones por scope (segmento, global, etc.)

- [ ] **T-023** | DM Subscription: add `channel` (NotificationChannel)
  - Línea: `   + channel : NotificationChannel`
  - Justificación: UC_ALR_05 selecciona canal de notificación (in-app, email, etc.)

- [ ] **T-024** | DM User: add `segment_id` (UUID)
  - Archivo: `source/arquitectura-tecnica/domain-model/user.rst`
  - Línea: `   + segment_id : UUID                  <<BR-012: segmento único por usuario>>`
  - Justificación: UC_USR_03 / UC_ACC_04 referencia segmento del usuario (BR-012)

**Total D3b: 14 tasks (T-011..T-024), 9 archivos DM distintos, 14 adds + 1 enum (AccessGroupState).**

(Nota: T-014 cubre tanto el ADD como el rename UC asociado; el conteo de 15 miembros
del MEASURE se cubre con 14 tasks porque T-013 introduce además el enum referenciado.)

## Bloque D3c — case mismatch y alias

- [ ] **T-025** | UC case mismatch: `PiiScanner` → `PIIScanner`
  - Archivos:
    - `source/requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-secuencia.rst`
    - `source/requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst`
    - `source/requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-secuencia.rst`
  - Sed: `s/\bPiiScanner\b/PIIScanner/g`
  - Justificación: el nombre canónico DM (en `general-audit-service.rst`) es `PIIScanner` (acrónimo en mayúsculas)
  - Verificación: `grep -rl 'PiiScanner' source/requisitos/` retorna 0 archivos

- [ ] **T-026** | UC alias: `MenuIVRReportService` → `IVRNavigationReportService`
  - Archivos:
    - `source/requisitos/casos-uso/reports/uc-rpt-16/implementacion-tecnica.rst`
    - `source/requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst`
  - Sed: `s/\bMenuIVRReportService\b/IVRNavigationReportService/g`
  - Justificación: D5 — `MenuIVRReportService` es alias semántico de la clase canónica DM
    `IVRNavigationReportService`. Se evita duplicar responsabilidad creando una clase nueva.
  - Verificación: `grep -rl 'MenuIVRReportService' source/` retorna 0 archivos

**Total D3c: 2 tasks (T-025..T-026).**

## Bloque D1 — 48 archivos nuevos uc-usr-05/06/07

Cada task crea la spec Larman completa de un UC (16 archivos) más
sus 6 diagramas UML. La elaboración debe respetar las
convenciones existentes en otros UCs del cluster `users/`
(uc-usr-01..04 como referencia de estructura).

**Estructura por UC (16 archivos):**

```
source/requisitos/casos-uso/users/uc-usr-XX/
├── index.rst                                  (existe, actualizar de Reservado a Aprobado)
├── informacion-general.rst                    (nuevo)
├── actores-precondiciones.rst                 (nuevo)
├── flujo-principal.rst                        (nuevo)
├── flujos-alternos.rst                        (nuevo)
├── excepciones.rst                            (nuevo)
├── criterios-aceptacion.rst                   (nuevo)
├── datos-involucrados.rst                     (nuevo)
├── patrones-diseno.rst                        (nuevo)
├── requisitos-no-funcionales.rst              (nuevo)
├── implementacion-tecnica.rst                 (nuevo)
├── testing.rst                                (nuevo)
└── diagramas-uml/
    ├── index.rst                              (nuevo)
    ├── diagrama-de-caso-de-uso.rst            (nuevo)
    ├── diagrama-de-secuencia.rst              (nuevo)
    ├── diagrama-de-actividad.rst              (nuevo)
    └── notas-sobre-los-diagramas.rst          (nuevo)
```

(15 archivos nuevos por UC + 1 actualización del index.rst = 16 acciones por UC.)

---

- [ ] **T-027** | UC_USR_05 bloquear-usuario: crear spec completa Larman
  - Directorio: `source/requisitos/casos-uso/users/uc-usr-05/`
  - Acciones:
    - Actualizar `index.rst` de `:estado: Reservado` a `:estado: Aprobado`, `:version: 1.0.0`,
      con `toctree` que liste los archivos creados.
    - Crear los 15 archivos nuevos siguiendo las plantillas de uc-usr-01..04.
  - Referencia conceptual: bloqueo administrativo de cuenta por uso indebido o seguridad;
    actor primario `block_user` (función RBAC) o admin equivalente; transición de
    `User.state: ACTIVE → BLOCKED` con AuditEvent `USER_BLOCKED`.
  - Domain-model usados: `User`, `AuditService`, `AuthorizationGuard`, `Session` (revocación de sesiones activas)
  - Origen documentado: referenciado en uc-auth-03/04/05 como UC dependiente
  - Verificación:
    - `find casos-uso/users/uc-usr-05 -name "*.rst" | wc -l` = 17 (1 index + 11 spec + 5 diagramas + diagrams-index = 17)
    - Build sphinx no genera warnings nuevos por refs rotas

- [ ] **T-028** | UC_USR_06 desbloquear-usuario: crear spec completa Larman
  - Directorio: `source/requisitos/casos-uso/users/uc-usr-06/`
  - Acciones equivalentes a T-027.
  - Referencia conceptual: desbloqueo administrativo de cuenta bloqueada;
    actor `unblock_user`; transición `User.state: BLOCKED → ACTIVE` con AuditEvent `USER_UNBLOCKED`.
  - Domain-model usados: `User`, `AuditService`, `AuthorizationGuard`
  - Verificación equivalente a T-027.

- [ ] **T-029** | UC_USR_07 editar-perfil-propio: crear spec completa Larman
  - Directorio: `source/requisitos/casos-uso/users/uc-usr-07/`
  - Acciones equivalentes a T-027.
  - Referencia conceptual: usuario edita campos editables de su propio perfil
    (full_name, email opcionalmente); actor `edit_own_profile`;
    sin cambio de RBAC (no toca primary_access_group_id ni segment_id).
  - Domain-model usados: `User`, `AuditService` (PROFILE_UPDATED), `AuthorizationGuard`
  - Verificación equivalente a T-027.

**Total D1: 3 tasks (T-027..T-029), 48 archivos nuevos (3 × 16).**

## Bloque D1 colateral — 3 view files alineados

- [ ] **T-030** | use-case-view uc-usr-05: alinear con spec nueva
  - Archivo: `source/arquitectura-tecnica/use-case-view/users/uc-usr-05-bloquear-usuario.rst`
  - Acciones:
    - Agregar `left to right direction` al @startuml (uml-07 conformance)
    - Verificar que `:doc:` refs apunten a la nueva spec textual
    - Verificar refs a domain-model coincidan con T-027

- [ ] **T-031** | use-case-view uc-usr-06: alinear con spec nueva
  - Archivo: `source/arquitectura-tecnica/use-case-view/users/uc-usr-06-desbloquear-usuario.rst`
  - Acciones equivalentes a T-030.

- [ ] **T-032** | use-case-view uc-usr-07: alinear con spec nueva
  - Archivo: `source/arquitectura-tecnica/use-case-view/users/uc-usr-07-editar-perfil-propio.rst`
  - Acciones equivalentes a T-030.

**Total D1 colateral: 3 tasks (T-030..T-032).**

## Bloque cierre

- [ ] **T-033** | Build sphinx strict + verificación completitud
  - Comando: `make html SPHINXOPTS='-W -j auto'`
  - Verificación:
    - Exit 0 sin warnings nuevos
    - Re-ejecutar el script de gap analysis del DISCOVER/MEASURE
    - Esperado: `cross-ref-gaps-v3.txt` muestra 0 gaps (todas las clases UC referenciadas existen
      en DM, todos los miembros UC tienen counterpart canónico)

- [ ] **T-034** | TRACK changelog y cierre del WP
  - Archivo: `track/wp-changelog.md`
  - Contenido: Keep a Changelog format con resumen por bloque (D3a/b/c, D1, colateral)
  - Cross-ref a commits con SHA
  - Update de roadmap status

**Total cierre: 2 tasks (T-033..T-034).**

---

# Resumen del task plan

| Bloque | Tasks | Archivos afectados | Riesgo |
|---|---|---|---|
| D3a — UC renames | 10 (T-001..T-010) | 8 archivos UC | Bajo (sed scoped) |
| D3b — DM adds | 14 (T-011..T-024) | 9 archivos DM | Bajo-medio (edición manual de PlantUML blocks) |
| D3c — case + alias | 2 (T-025..T-026) | 5 archivos UC | Bajo (sed bulk) |
| D1 — UCs nuevos | 3 (T-027..T-029) | 48 archivos nuevos | Alto volumen, riesgo medio (semántica) |
| D1 colateral — view | 3 (T-030..T-032) | 3 archivos view | Bajo |
| Cierre | 2 (T-033..T-034) | build + changelog | Bajo |
| **Total** | **34 tasks** | **~70 archivos** | — |

# Criterios de completitud verificable

Cada task atómico tiene:

1. **Archivo(s) afectado(s)** — paths absolutos especificados.
2. **Acción concreta** — sed pattern o contenido a insertar.
3. **Referencia de origen** — clase DM canónica o UC origen.
4. **Verificación post-task** — comando grep o regla específica
   que retorna estado `pass/fail` sin ambigüedad.

# DAG de dependencias

```
D3a (T-001..T-010) ──┐
                     ├─→ D3c (T-025..T-026) ──┐
D3b (T-011..T-024) ──┘                        │
                                              ├─→ T-033 (build) ──→ T-034 (cierre)
D1 (T-027..T-029) ──→ D1 colateral (T-030..T-032) ──┘
```

D3a, D3b y D1 son independientes entre sí (tocan archivos
disjuntos). D3c puede correr en paralelo. El cierre (T-033 build
strict + T-034 changelog) depende de todo lo anterior.

# Refs

- DISCOVER analysis: `wp-state.md`
- MEASURE summary: `measure/measure-summary.md`
- D4 classification: `analyze/d4-classification.md`
- DM bodies dump: `analyze/dm-canonical-bodies.txt`
