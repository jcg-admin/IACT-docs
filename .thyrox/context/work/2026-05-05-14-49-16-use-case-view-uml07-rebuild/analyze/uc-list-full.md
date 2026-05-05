# Lista completa — 83 UCs ↔ archivos ↔ clases canónicas

Generado del cruce inventory.json + uc-to-domain-model-mapping.json.


## auth/ (5 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-auth-01 | uc-auth-01-iniciar-sesion.rst | ✓ | AccessGroup, AuditEvent, ExceptionalPermission, FunctionGroup, InternalMailbox |
| uc-auth-02 | uc-auth-02-cerrar-sesion.rst | ✓ | AccessGroup, AuditEvent, FunctionGroup, InternalMailbox |
| uc-auth-03 | uc-auth-03-recuperar-contrasena.rst | ✓ | AccessGroup, AuditEvent, FunctionGroup, InternalMailbox |
| uc-auth-04 | uc-auth-04-cambiar-contrasena.rst | ✓ | AccessGroup, AuditEvent, FunctionGroup, InternalMailbox |
| uc-auth-05 | uc-auth-05-gestionar-sesiones.rst | ✓ | AuditEvent |

## users/ (4 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-usr-01 | uc-usr-01-crear-usuario.rst | ✓ | AccessGroup, AuditEvent, InternalMailbox |
| uc-usr-02 | uc-usr-02-consultar-usuarios.rst | ✓ | AccessGroup, AuditEvent, FilterValidator |
| uc-usr-03 | uc-usr-03-modificar-usuario.rst | ✓ | AuditEvent, InternalMailbox |
| uc-usr-04 | uc-usr-04-eliminar-usuario.rst | ✓ | AuditEvent, InternalMailbox |

## access/ (7 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-acc-01 | uc-acc-01-asignar-funciones.rst | ✓ | AuditEvent, InternalMailbox, PermissionCache |
| uc-acc-02 | uc-acc-02-revocar-funciones.rst | ✓ | AuditEvent, InternalMailbox, PermissionCache |
| uc-acc-03 | uc-acc-03-consultar-permisos-efectivos.rst | ✓ | AccessGroup, AccessGroupFunction, AssignmentRepo, AuditEvent, ExceptionalPermission |
| uc-acc-04 | uc-acc-04-asignar-agrupador.rst | ✓ | AccessGroup, AccessGroupFunction, AuditEvent, InternalMailbox, PermissionCache |
| uc-acc-05 | uc-acc-05-gestionar-reglas-sod.rst | ✓ | AuditEvent |
| uc-acc-08 | uc-acc-08-permiso-temporal.rst | ✓ | AuditEvent, ExceptionalPermission, InternalMailbox, PermissionCache |
| uc-acc-09 | uc-acc-09-auditar-cambios-acceso.rst | ✓ | AuditEvent, FilterValidator |

## permissions/ (10 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-perm-01 | uc-perm-01-asignar-grupo-a-usuario.rst | — | AccessGroup, AccessGroupFunction, AuditEvent, PermissionCache |
| uc-perm-02 | uc-perm-02-revocar-grupo-a-usuario.rst | — | AccessGroup, AuditEvent, InternalMailbox, PermissionCache |
| uc-perm-03 | uc-perm-03-conceder-permiso-excepcional.rst | — | AuditEvent, ExceptionalPermission, PermissionCache |
| uc-perm-04 | uc-perm-04-revocar-permiso-excepcional.rst | ✓ | AuditEvent, ExceptionalPermission, ExceptionalPermissionRepo, InternalMailbox, PermissionCache |
| uc-perm-05 | uc-perm-05-crear-grupo-de-permisos.rst | ✓ | AccessGroup, AccessGroupFunction, AuditEvent |
| uc-perm-06 | uc-perm-06-asignar-funciones-a-grupo.rst | ✓ | AccessGroup, AccessGroupFunction, AuditEvent, FunctionGroup, PermissionCache |
| uc-perm-07 | uc-perm-07-verificar-permiso-de-usuario.rst | ✓ | AccessGroup, AccessGroupFunction, AssignmentRepo, AuditEvent, ExceptionalPermission, ExceptionalPermissionRepo, PermissionCache, PermissionService |
| uc-perm-08 | uc-perm-08-generar-menu-dinamico.rst | ✓ | AccessGroup, AccessGroupFunction, AuditEvent, ExceptionalPermission, PermissionService |
| uc-perm-09 | uc-perm-09-auditar-acceso-write-side.rst | ✓ | AccessGroup, AlertHook, AuditEvent, AuditRepo, AuditService, AuditValidator |
| uc-perm-10 | uc-perm-10-consultar-auditoria-de-permisos.rst | ✓ | AccessGroup, AuditEvent, AuditQueryService, AuditRepo, AuditService, CursorEncoder, ExportJob, ExportWorker, FilterValidator |

## reports/ (16 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-inc-rpt-01 | uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst | — | SegmentResolver |
| uc-rpt-01 | uc-rpt-01-ver-dashboard.rst | ✓ | AuditEvent, SegmentResolver |
| uc-rpt-02 | uc-rpt-02-ver-metricas-en-tiempo-real.rst | ✓ | AuditService, SegmentResolver |
| uc-rpt-03 | uc-rpt-03-ver-reportes-historicos.rst | ✓ | FilterValidator, HistoricalReport, SegmentResolver |
| uc-rpt-04 | uc-rpt-04-exportar-reporte.rst | ✓ | AuditService, ExportJob, ExportWorker, SegmentResolver |
| uc-rpt-07 | uc-rpt-07-programar-reporte.rst | ✓ | AuditService, ExportJob, ExportWorker, ScheduledReport, ScheduledReportRepo |
| uc-rpt-08 | uc-rpt-08-ver-reportes-programados.rst | ✓ | ScheduledReport, ScheduledReportListService, ScheduledReportRepo |
| uc-rpt-09 | uc-rpt-09-configurar-filtros.rst | ✓ | AuditService, FilterValidator, SavedFilter, SegmentResolver |
| uc-rpt-10 | uc-rpt-10-guardar-vista.rst | — | AuditService, ColumnCatalog, SavedView, SegmentResolver |
| uc-rpt-11 | uc-rpt-11-compartir-reporte.rst | — | AuditService, SavedView |
| uc-rpt-12 | uc-rpt-12-reporte-de-agentes.rst | — | AgentDailyStatRepo, AgentReportService, AuditService, SegmentResolver |
| uc-rpt-13 | uc-rpt-13-reporte-de-colas.rst | — | AbandonmentReportService, SegmentResolver |
| uc-rpt-14 | uc-rpt-14-reporte-de-campanas.rst | — | SegmentResolver |
| uc-rpt-15 | uc-rpt-15-reporte-de-transferencias.rst | — | SegmentResolver, TransferReportService |
| uc-rpt-16 | uc-rpt-16-reporte-de-menus-ivr.rst | — | IvrNavigationReportService, SegmentResolver |
| uc-rpt-17 | uc-rpt-17-reporte-de-clientes-unicos.rst | — | CallerReportService, SegmentResolver |

## alerts/ (5 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-alr-01 | uc-alr-01-configurar-umbrales-de-alertas.rst | — | AlertRule, AuditService, EvaluatorReloader, RuleValidator, SegmentResolver |
| uc-alr-02 | uc-alr-02-ver-alertas-activas.rst | — | AlertRepo, AlertRule, SegmentResolver |
| uc-alr-03 | uc-alr-03-reconocer-alerta.rst | — | AlertRepo, AuditEvent, AuditService, SegmentResolver |
| uc-alr-04 | uc-alr-04-ver-historial-de-alertas.rst | — | AlertRepo, SegmentResolver, TimingCalculator |
| uc-alr-05 | uc-alr-05-gestionar-suscripciones.rst | — | AuditService |

## pipeline/ (4 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-pip-01 | uc-pip-01-supervisar-etl.rst | — | PipelineExecution |
| uc-pip-02 | uc-pip-02-consultar-errores-etl.rst | — | PipelineExecution |
| uc-pip-03 | uc-pip-03-consultar-disponibilidad-de-datos.rst | — | PipelineExecution |
| uc-pip-04 | uc-pip-04-solicitar-reintento-de-pipeline.rst | — | AuditService, PipelineExecution |

## audit/ (4 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-aud-01 | uc-aud-01-consultar-auditoria-general.rst | — | AuditEvent, AuditRepo, AuditService, CursorEncoder |
| uc-aud-02 | uc-aud-02-buscar-auditoria.rst | — | AuditEvent, AuditService |
| uc-aud-03 | uc-aud-03-exportar-auditoria.rst | — | AuditEvent, AuditRepo, ExportJob, ExportWorker, InternalMailbox |
| uc-aud-04 | uc-aud-04-generar-reporte-de-compliance.rst | — | AccessGroup, AuditEvent, AuditRepo, AuditService |

## logs/ (7 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-log-01 | uc-log-01-consultar-logs-del-sistema.rst | — | AuditEvent |
| uc-log-02 | uc-log-02-consultar-logs-del-etl.rst | — | — |
| uc-log-03 | uc-log-03-buscar-logs.rst | — | — |
| uc-log-04 | uc-log-04-exportar-logs.rst | — | ExportJob, ExportWorker, InternalMailbox |
| uc-log-05 | uc-log-05-ver-logs-de-infraestructura.rst | — | — |
| uc-log-06 | uc-log-06-ver-estado-del-sistema.rst | — | PipelineExecution |
| uc-log-07 | uc-log-07-ver-metricas-tecnicas.rst | — | — |

## operator/ (10 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-opr-01 | uc-opr-01-cambiar-estado-del-agente.rst | — | AuditService |
| uc-opr-02 | uc-opr-02-atender-llamada-entrante.rst | — | AuditService |
| uc-opr-03 | uc-opr-03-realizar-llamada-saliente.rst | — | AuditService |
| uc-opr-04 | uc-opr-04-hold-unhold-llamada.rst | — | AuditService |
| uc-opr-05 | uc-opr-05-transferir-llamada.rst | — | AuditService |
| uc-opr-06 | uc-opr-06-ingresar-disposition.rst | — | AuditService |
| uc-opr-07 | uc-opr-07-solicitar-break-pausa.rst | — | — |
| uc-opr-08 | uc-opr-08-ver-propio-dashboard.rst | — | AgentDailyStatRepo |
| uc-opr-09 | uc-opr-09-ver-propio-historial-de-llamadas.rst | — | — |
| uc-opr-10 | uc-opr-10-recibir-notificacion-supervisor.rst | — | — |

## supervision/ (3 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-sup-01 | uc-sup-01-monitorear-llamada-whisper.rst | — | AuditService |
| uc-sup-02 | uc-sup-02-barge-in-en-llamada.rst | — | AuditService |
| uc-sup-03 | uc-sup-03-mensaje-broadcast-al-equipo.rst | — | AuditService |

## caller/ (5 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-cli-01 | uc-cli-01-iniciar-llamada-al-call-center.rst | — | AuditService |
| uc-cli-02 | uc-cli-02-navegar-ivr.rst | — | — |
| uc-cli-03 | uc-cli-03-esperar-en-cola.rst | — | — |
| uc-cli-04 | uc-cli-04-solicitar-callback.rst | — | AuditService |
| uc-cli-05 | uc-cli-05-calificar-atencion-post-call.rst | — | — |

## admin/ (3 UCs)

| ID | Archivo destino | Src diag | Clases canónicas usadas |
|----|-----------------|----------|--------------------------|
| uc-adm-01 | uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst | — | AuditEvent, AuditService |
| uc-adm-02 | uc-adm-02-gestionar-catalogo-de-funciones.rst | — | AuditEvent, AuditService |
| uc-adm-03 | uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst | — | AuditEvent, AuditService, FunctionGroup |

**Total UCs:** 83
**Con src diagram en casos-uso:** 30/83