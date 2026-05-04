```yml
created_at: 2026-05-04 21:05:00
project: THYROX
work_package: 2026-05-04-21-04-07-alias-fix-single-letra
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP alias-fix-single-letra — Scope Analysis

## Alcance

Corrección de aliases tipo SINGLE_LETTER y LETRA_NUMERO.
Fuente: diccionario `iact-alias-dictionary.md` del WP alias-catalog.

## Aliases con corrección directa (sin conflicto)

Total aliases con corrección directa: 75
Archivos afectados: 17

| Alias | Corrección | Archivos |
|-------|-----------|---------|
| `A` | `BC_AUTH` | overview.rst |
| `A1` | `INICIAR_SESION` | agrupamiento-con-paquetes.rst, ejemplo-iact-uc-auth-01-con-variante-2fa.rst |
| `A2` | `CERRAR_SESION` | agrupamiento-con-paquetes.rst |
| `C` | `BC_CALLS` | overview.rst |
| `C01` | `LLAMAR_SISTEMA_IVR` | mod-caller.rst |
| `C02` | `NAVEGAR_MENU_IVR` | mod-caller.rst |
| `C03` | `ESPERAR_COLA` | mod-caller.rst |
| `C04` | `RECIBIR_CALLBACK` | mod-caller.rst |
| `C05` | `RESPONDER_ENCUESTA_CSAT` | mod-caller.rst |
| `D` | `BC_AUDIT` | overview.rst |
| `E` | `BC_ETL` | overview.rst |
| `G` | `BC_LOGS` | overview.rst |
| `L` | `BC_ALERTS` | overview.rst |
| `L01` | `VER_LOGS_SISTEMA` | mod-logs.rst |
| `L02` | `VER_LOGS_ETL` | mod-logs.rst |
| `L03` | `BUSCAR_LOGS` | mod-logs.rst |
| `L04` | `EXPORTAR_LOGS` | mod-logs.rst |
| `L05` | `VER_LOGS_INFRAESTRUCTURA` | mod-logs.rst |
| `L06` | `VER_ESTADO_SISTEMA` | mod-logs.rst |
| `L07` | `VER_METRICAS_TECNICAS` | mod-logs.rst |
| `L1` | `CONSULTAR_LOGS` | agrupamiento-con-paquetes.rst |
| `O01` | `CAMBIAR_ESTADO_AGENTE` | mod-operator.rst |
| `O02` | `ATENDER_LLAMADA` | mod-operator.rst |
| `O03` | `INICIAR_LLAMADA_OUTBOUND` | mod-operator.rst |
| `O04` | `HOLD_UNHOLD_LLAMADA` | mod-operator.rst |
| `O05` | `TRANSFERIR_LLAMADA` | mod-operator.rst |
| `O06` | `DISPOSICION_POST_LLAMADA` | mod-operator.rst |
| `O07` | `TOMAR_BREAK` | mod-operator.rst |
| `O08` | `VER_DASHBOARD_DESEMPENO` | mod-operator.rst |
| `O09` | `VER_HISTORIAL_LLAMADAS` | mod-operator.rst |
| `O10` | `VER_BUZON_MENSAJES` | mod-operator.rst |
| `P` | `BC_REPORTS` | overview.rst |
| `P08` | `GENERAR_MENU_DINAMICO` | mod-auth.rst, mod-permissions.rst |
| `P09` | `AUDITAR_ACCESO` | mod-permissions.rst |
| `P1` | `PASO_AUTENTICACION` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst (+1) |
| `P10` | `AUDITORIA_ACCESO` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst (+1) |
| `P11` | `VALIDAR_ANTI_SELF` | diagrama-de-caso-de-uso.rst, diagrama-de-caso-de-uso.rst |
| `P2` | `DASHBOARD_IVR` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P3` | `CIERRE_SESION` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P4` | `GESTION_PIPELINE_ETL` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst (+2) |
| `P5` | `CONSULTA_LOGS` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P6` | `MODULO_REPORTES` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P7` | `BASE_ANALITICA_IVR` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P8` | `ALERTAS_NOTIFICACIONES` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `P9` | `RESOLVER_SEGMENTO` | arquitectura-general.rst, dfd-nivel-1-subprocesos.rst |
| `R` | `BC_RBAC` | overview.rst |
| `R01` | `VER_DASHBOARD_IVR` | mod-reports.rst |
| `R02` | `VER_METRICAS_TIEMPO_REAL` | mod-reports.rst |
| `R03` | `VER_REPORTES_HISTORICOS` | mod-reports.rst |
| `R04` | `EXPORTAR_REPORTE` | mod-reports.rst |
| `R07` | `PROGRAMAR_REPORTE` | mod-reports.rst |
| `R08` | `VER_REPORTES_PROGRAMADOS` | mod-reports.rst |
| `R1` | `VER_DASHBOARD_IVR` | submaquina-reporte.rst, agrupamiento-con-paquetes.rst |
| `R10` | `GUARDAR_VISTA` | mod-reports.rst |
| `R11` | `COMPARTIR_REPORTE` | mod-reports.rst |
| `R12` | `REPORTE_AGENTES` | mod-reports.rst |
| `R13` | `REPORTE_COLAS` | mod-reports.rst |
| `R14` | `REPORTE_CAMPANAS` | mod-reports.rst |
| `R15` | `REPORTE_TRANSFERENCIAS` | mod-reports.rst |
| `R16` | `REPORTE_MENUS_IVR` | mod-reports.rst |
| `R17` | `REPORTE_CLIENTES_UNICOS` | mod-reports.rst |
| `R2` | `RESOLVER_SEGMENTO` | submaquina-reporte.rst |
| `R3A` | `EXTENSION_REPORTES_HISTORICOS` | submaquina-reporte.rst |
| `R3B` | `EXTENSION_REPORTES_HISTORICOS_B` | submaquina-reporte.rst |
| `R3C` | `EXTENSION_REPORTES_HISTORICOS_C` | submaquina-reporte.rst |
| `R4` | `EJECUTAR_PROCEDIMIENTO_RPT` | submaquina-reporte.rst, agrupamiento-con-paquetes.rst |
| `R5` | `RENDERIZAR_REPORTE` | submaquina-reporte.rst |
| `S01` | `MONITOREAR_LLAMADAS_EN_VIVO` | mod-supervision.rst |
| `S02` | `INTERVENIR_LLAMADA` | mod-supervision.rst |
| `S03` | `ENVIAR_MENSAJE_EQUIPO` | mod-supervision.rst |
| `S1` | `RECIBIR_SOLICITUD_ETL` | submaquina-etl.rst |
| `S2A` | `SP_RPT_CENTROS_XSEGMENTO` | submaquina-etl.rst |
| `S2B` | `SP_RPT_LLAMADAS_ABANDONADAS` | submaquina-etl.rst |
| `S3` | `VERIFICAR_RESULTADO_ETL` | submaquina-etl.rst |
| `U1` | `CRUD_USUARIOS` | agrupamiento-con-paquetes.rst |

## Aliases CONFLICTIVOS (requieren per-archivo)

Total aliases conflictivos: 24
- `A01`: 2 archivos — use-case-view/mod-audit.rst, use-case-view/mod-auth.rst
- `A02`: 2 archivos — use-case-view/mod-audit.rst, use-case-view/mod-auth.rst
- `A03`: 2 archivos — use-case-view/mod-audit.rst, use-case-view/mod-auth.rst
- `A04`: 2 archivos — use-case-view/mod-audit.rst, use-case-view/mod-auth.rst
- `A05`: 1 archivos — use-case-view/mod-auth.rst
- `P01`: 2 archivos — use-case-view/mod-permissions.rst, use-case-view/mod-pipeline.rst
- `P02`: 2 archivos — use-case-view/mod-permissions.rst, use-case-view/mod-pipeline.rst
- `P03`: 2 archivos — use-case-view/mod-permissions.rst, use-case-view/mod-pipeline.rst
- `P04`: 2 archivos — use-case-view/mod-permissions.rst, use-case-view/mod-pipeline.rst
- `P05`: 1 archivos — use-case-view/mod-permissions.rst
- `P06`: 1 archivos — use-case-view/mod-permissions.rst
- `P07`: 1 archivos — use-case-view/mod-permissions.rst
- `U01`: 2 archivos — use-case-view/mod-users.rst, diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U02`: 2 archivos — use-case-view/mod-users.rst, diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U03`: 2 archivos — use-case-view/mod-users.rst, diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U04`: 2 archivos — use-case-view/mod-users.rst, diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U07`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U08`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U09`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U10`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U11`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U12`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U13`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
- `U14`: 1 archivos — diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst
