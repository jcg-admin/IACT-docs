```yml
created_at: 2026-05-04 11:10:00
project: IACT-docs
work_package: 2026-05-04-08-32-37-estructura-requisitos-arq-audit
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Activo
```

# Registro de Decisiones — Trazabilidad de Clases y Atributos

## Modelo canónico de referencia

Fuente: `source/arquitectura-tecnica/bounded-contexts/bounded-context-*.rst`

### Clases canónicas con atributos y métodos clave

| BC | Clase | Atributos canónicos (tipos) | Métodos canónicos |
|----|-------|-----------------------------|-------------------|
| Auth | User | user_id:UUID, username:String, email:String, state:UserState, created_at:DateTime, last_login_at:DateTime | create(), deactivate(), modify(), view(), recover_password() |
| Auth | Session | session_id:UUID, user_id:UUID, started_at:DateTime, last_activity_at:DateTime, expires_at:DateTime, state:SessionState | open(), close(), close_all(), view_own_sessions() |
| Auth | InternalMailbox | mailbox_id:UUID, owner_user_id:UUID, last_read_at:DateTime | deliver_message(), view_messages(), mark_read() |
| RBAC | Function | name:String, module:Module | register(), view() |
| RBAC | FunctionGroup | group_id:UUID, name:String | create_function_group(), assign_functions() |
| RBAC | AccessGroup | agr_id:String, name:String | assign_to_user(), revoke_from_user() |
| RBAC | Assignment | assignment_id:UUID, user_id:UUID, group_ref:String, expires_at:DateTime, state:AssignmentState | create(), revoke() |
| RBAC | ExceptionalPermission | permission_id:UUID, function_id:UUID, granted_at:DateTime, expires_at:DateTime, state:PermissionState | grant(), revoke() |
| RBAC | SeparationRule | rule_id:UUID, conflicting_functions:List | create(), view(), update_separation_rule() |
| Calls | Call | call_id:UUID, campaign_id:UUID | (ver BC) |
| Calls | Campaign | campaign_id:UUID | (ver BC) |
| Reports | Report | report_id:UUID, scope:ReportScope, state:ReportState | view(), filter(), export() |
| Reports | Metric | metric_id:UUID, name:MetricName | (ver BC) |
| Reports | ExportJob | job_id:UUID, format:ExportFormat, state:JobState | enqueue(), process(), complete() |
| Reports | ScheduledReport | (ver BC) | (ver BC) |
| Reports | SavedView | (ver BC) | (ver BC) |
| Pipeline ETL | ETLEjecucion | id:Integer, tabla_origen:String, estado:EstadoEjecucion | es_exitosa(), es_fallida() |
| Alerts | Alert | alert_id:UUID, state:AlertState | acknowledge(), configure() |
| Alerts | Threshold | (ver BC) | (ver BC) |
| Alerts | Subscription | subscription_id:UUID, state:SubscriptionState | subscribe(), unsubscribe() |
| Audit | AuditEvent | event_id:UUID, event_type:EventType, details:JSON, occurred_at:DateTime | record(), view(), search() |
| Logs | ApplicationLog | (ver BC) | (ver BC) |
| Logs | ETLLog | (ver BC) | (ver BC) |
| Logs | InfrastructureLog | (ver BC) | (ver BC) |
| Logs | SystemHealth | (ver BC) | (ver BC) |
| Logs | TechnicalMetric | (ver BC) | (ver BC) |

### Enums canónicos

| Clase | Enum | Valores |
|-------|------|---------|
| User | UserState | ACTIVE, INACTIVE, BLOCKED |
| Session | SessionState | ACTIVE, CLOSED, EXPIRED |
| Assignment | AssignmentState | (ver BC) |
| ExceptionalPermission | PermissionState | (ver BC) |
| SeparationRule | RuleState | (ver BC) |
| Alert | AlertState | ACTIVE, ACKNOWLEDGED, DISABLED |
| Subscription | SubscriptionState | (ver BC) |
| ETLEjecucion | EstadoEjecucion | (ver BC) |
| Report | ReportScope | (ver BC) |
| Report | ReportState | (ver BC) |
| ExportJob | JobState | (ver BC) |
| ExportJob | ExportFormat | (ver BC) |

## Inconsistencias identificadas en archivos existentes (auditoría pre-ejecución)

| Archivo | Inconsistencia | Tipo | Severidad | Corrección |
|---------|---------------|------|-----------|------------|
| `modulos/user-identity/diagramas/clases-modulo-identidad.rst` | `id` (int) → debe ser `user_id` (UUID); `is_active` (bool) → `state` (UserState); `date_joined` → `created_at` | Atributos incorrectos | CRÍTICA | Actualizar diagrama con clases canónicas |
| `modulos/alerts/diagramas/ciclo-vida-alerta.rst` | Estados PENDIENTE/ACTIVA/RECONOCIDA/RESUELTA → deben ser ACTIVE/ACKNOWLEDGED/DISABLED | Enum incorrecto | ALTA | Reemplazar estados con AlertState canónico |
| `requisitos/casos-uso/auth/uc-auth-01/datos-involucrados.rst` | `closed_at`, `close_reason` como atributos de Session → no existen en canónico | Atributos no canónicos | MEDIA | Eliminar; usar `state: SessionState` |
| `requisitos/casos-uso/permissions/uc-perm-06/diagrama-de-cascade.rst` | Clase `AccessGroupFunction` (junction table técnica) → no está en modelo de dominio | Clase técnica en diagrama de dominio | MEDIA | Reemplazar con relación canónica FunctionGroup→Function |

## Decisiones tomadas para la ejecución

**DT-01:** Los 26 archivos de clase en `domain-model/` (T-009) se crean extrayendo
el diagrama exacto de cada clase del `bounded-context-*.rst` fuente. Los atributos
y métodos deben ser idénticos al canónico — sin modificaciones.

**DT-02:** En `design-view/` (T-020), los diagramas de secuencia por módulo usan
exactamente los nombres de clase del BC correspondiente para representar los
objetos participantes. No se usan alias genéricos como "SvcNode" cuando hay un
nombre de clase concreto.

**DT-03:** En `process-view/` (T-028..T-031), los diagramas de concurrencia ETL
usan `ETLEjecucion` con sus atributos y métodos canónicos (`es_exitosa()`,
`es_fallida()`, `estado:EstadoEjecucion`).

**DT-04:** Las correcciones de trazabilidad en archivos existentes (user-identity,
alerts, uc-auth-01, uc-perm-06) se ejecutan dentro de este WP como parte de la
fase de corrección de vistas (después de restructuring).
