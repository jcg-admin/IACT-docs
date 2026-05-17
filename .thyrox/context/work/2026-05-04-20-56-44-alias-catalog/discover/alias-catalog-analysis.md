```yml
created_at: 2026-05-04 21:00:00
project: THYROX
work_package: 2026-05-04-20-56-44-alias-catalog
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Catálogo de Aliases PlantUML — IACT docs

## Alcance

Directorios analizados:
- `source/arquitectura-tecnica/` — 87 archivos RST con aliases
- `source/requisitos/` — 409 archivos RST con aliases

**Total aliases únicos:** 424
**Aliases con violación:** 369 (581 ocurrencias)
**Aliases limpios:** 55

## Criterios de violación (adaptados de normativa clean code)

| Tipo | Criterio | Ejemplo violación | Ejemplo correcto |
|------|----------|-------------------|-----------------|
| SINGLE_LETTER | Alias de 1 letra | `A`, `S`, `U` | `SERVICIO_AUTH` |
| LETRA_NUMERO | Letra + dígito | `A1`, `C01`, `P10` | `INICIAR_SESION` |
| ABBREV_2_NUMERO | 2 letras + número | `UC01`, `AL03`, `AC08` | `CREAR_USUARIO` |
| ABBREV_NUMERO | Abreviatura + número | `PERM01`, `ACC08`, `RPT03` | `GESTIONAR_PERMISOS` |
| ABREV_CORTA | 2-5 chars sin underscore | `AUD`, `ETL`, `RPT`, `IVR` | `SERVICIO_AUDITORIA` |
| UC_PREFIX | Prefijo `UC_` o `UC` | `UC_AUTH`, `UC_RPT` | `CLUSTER_AUTH` |
| F_ABBREV | `F_` + abreviatura | `F_VA`, `F_EL`, `F_TC` | `FUNCION_VER_ALERTAS` |
| PREFIX_ABBREV | Prefijo técnico + abbrev | `NODE_PG`, `DB_AUTH`, `ART_R1` | `NODO_POSTGRES` |

---

## Resumen por tipo de violación

- **Letra sola** (`SINGLE_LETTER`): 8 aliases, 8 ocurrencias
- **Letra + dígito** (`LETRA_NUMERO`): 86 aliases, 117 ocurrencias
- **2 letras + número** (`ABBREV_2_NUMERO`): 42 aliases, 85 ocurrencias
- **Abreviatura + número** (`ABBREV_NUMERO`): 25 aliases, 40 ocurrencias
- **Abreviatura corta (2-5 chars)** (`ABREV_CORTA`): 76 aliases, 198 ocurrencias
- **Prefijo UC_** (`UC_PREFIX`): 15 aliases, 15 ocurrencias
- **F_ + abreviatura** (`F_ABBREV`): 57 aliases, 57 ocurrencias
- **Prefijo técnico + abreviatura** (`PREFIX_ABBREV`): 60 aliases, 61 ocurrencias

---

## Letra sola (8 aliases, 8 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `A` | 1 | Auth | `arquitectura-tecnica/domain-model/overview.rst` |
| `C` | 1 | Calls | `arquitectura-tecnica/domain-model/overview.rst` |
| `D` | 1 | Audit | `arquitectura-tecnica/domain-model/overview.rst` |
| `E` | 1 | Pipeline ETL | `arquitectura-tecnica/domain-model/overview.rst` |
| `G` | 1 | Logs | `arquitectura-tecnica/domain-model/overview.rst` |
| `L` | 1 | Alerts | `arquitectura-tecnica/domain-model/overview.rst` |
| `P` | 1 | Reports & Metrics | `arquitectura-tecnica/domain-model/overview.rst` |
| `R` | 1 | RBAC (subsume PERM) | `arquitectura-tecnica/domain-model/overview.rst` |

## Letra + dígito (86 aliases, 117 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `A01` | 2 | UC_AUD_01\nVer Auditoria\nGeneral; UC_AUTH_01\nIniciar Sesion | `arquitectura-tecnica/use-case-view/mod-audit.rst` (+1) |
| `A02` | 2 | UC_AUD_02\nBuscar en\nAuditoria; UC_AUTH_02\nCerrar Sesion | `arquitectura-tecnica/use-case-view/mod-audit.rst` (+1) |
| `A03` | 2 | UC_AUD_03\nExportar\nAuditoria; UC_AUTH_03\nRecuperar Contrasena | `arquitectura-tecnica/use-case-view/mod-audit.rst` (+1) |
| `A04` | 2 | UC_AUD_04\nGenerar Reporte\nCompliance; UC_AUTH_04\nCambiar Contrasena | `arquitectura-tecnica/use-case-view/mod-audit.rst` (+1) |
| `A05` | 1 | UC_AUTH_05\nGestionar Sesiones | `arquitectura-tecnica/use-case-view/mod-auth.rst` |
| `A1` | 2 | Iniciar sesión; UC_AUTH_01\nIniciar sesión\n(BASE) | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` (+1) |
| `A2` | 1 | Cerrar sesión | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `C01` | 1 | UC_CLI_01\nLlamar al\nSistema IVR | `arquitectura-tecnica/use-case-view/mod-caller.rst` |
| `C02` | 1 | UC_CLI_02\nNavegar Menu\nIVR | `arquitectura-tecnica/use-case-view/mod-caller.rst` |
| `C03` | 1 | UC_CLI_03\nEsperar en Cola\nde Atencion | `arquitectura-tecnica/use-case-view/mod-caller.rst` |
| `C04` | 1 | UC_CLI_04\nRecibir\nCallback | `arquitectura-tecnica/use-case-view/mod-caller.rst` |
| `C05` | 1 | UC_CLI_05\nResponder Encuesta\nCSAT post | `arquitectura-tecnica/use-case-view/mod-caller.rst` |
| `L01` | 1 | UC_LOG_01\nVer Logs\ndel Sistema | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L02` | 1 | UC_LOG_02\nVer Logs ETL\n(etl_runs) | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L03` | 1 | UC_LOG_03\nBuscar Logs | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L04` | 1 | UC_LOG_04\nExportar Logs | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L05` | 1 | UC_LOG_05\nVer Logs de\nInfraestructura | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L06` | 1 | UC_LOG_06\nVer Estado\ndel Sistema | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L07` | 1 | UC_LOG_07\nVer Metricas\nTecnicas | `arquitectura-tecnica/use-case-view/mod-logs.rst` |
| `L1` | 1 | Consultar logs | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `O01` | 1 | UC_OPR_01\nCambiar Estado\ndel Agente | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O02` | 1 | UC_OPR_02\nAtender Llamada\nEntrante | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O03` | 1 | UC_OPR_03\nIniciar Llamada\nOutbound | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O04` | 1 | UC_OPR_04\nHold/Unhold\nLlamada | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O05` | 1 | UC_OPR_05\nTransferir\nLlamada | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O06` | 1 | UC_OPR_06\nDisposicion\npost-Llamada | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O07` | 1 | UC_OPR_07\nTomar Break | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O08` | 1 | UC_OPR_08\nVer Dashboard\nde Desempeno | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O09` | 1 | UC_OPR_09\nVer Historial\nde Llamadas | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `O10` | 1 | UC_OPR_10\nVer Buzon\nde Mensajes | `arquitectura-tecnica/use-case-view/mod-operator.rst` |
| `P01` | 2 | UC_PERM_01\nAsignar Grupo\na Usuario; UC_PIP_01\nVer Estado ETL\n(etl_runs) | `arquitectura-tecnica/use-case-view/mod-permissions.rst` (+1) |
| `P02` | 2 | UC_PERM_02\nRevocar Grupo\na Usuario; UC_PIP_02\nVer Errores ETL\n(etl_runs.es | `arquitectura-tecnica/use-case-view/mod-permissions.rst` (+1) |
| `P03` | 2 | UC_PERM_03\nConceder Permiso\nExcepciona; UC_PIP_03\nVer Disponibilidad\nde Datos | `arquitectura-tecnica/use-case-view/mod-permissions.rst` (+1) |
| `P04` | 2 | UC_PERM_04\nRevocar Permiso\nExcepcional; UC_PIP_04\nReintentar ETL\n(sp_etl_histo | `arquitectura-tecnica/use-case-view/mod-permissions.rst` (+1) |
| `P05` | 1 | UC_PERM_05\nCrear / Modificar /\nRetirar | `arquitectura-tecnica/use-case-view/mod-permissions.rst` |
| `P06` | 1 | UC_PERM_06\nAsignar Funciones\na Grupo | `arquitectura-tecnica/use-case-view/mod-permissions.rst` |
| `P07` | 1 | UC_PERM_07\nVerificar Permiso\nde Usuari | `arquitectura-tecnica/use-case-view/mod-permissions.rst` |
| `P08` | 2 | UC_PERM_08\nGenerar Menu Dinamico\n[view; UC_PERM_08\nGenerar Menu\nDinamico\n[vie | `arquitectura-tecnica/use-case-view/mod-auth.rst` (+1) |
| `P09` | 1 | UC_PERM_09\nAuditar Acceso\n(write side) | `arquitectura-tecnica/use-case-view/mod-permissions.rst` |
| `P1` | 3 | 1\nAutenticacion JWT; 1\nAutenticacion\nJWT (+1) | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+2) |
| `P10` | 3 | 10\nAuditoria; 10\nAuditoria\nde Acceso (+1) | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+2) |
| `P11` | 2 | Validar P-11\nanti-self-elimination; Validar P-11\nanti-self-revoke | `uc-acc-02/diagramas-uml/diagrama-de-caso-de-uso.rst` (+1) |
| `P2` | 2 | 2\nDashboard IVR | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P3` | 2 | 3\nCierre de Sesion; 3\nCierre de\nSesion | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P4` | 4 | 4\nGestion\nPipeline ETL; Solicitar reintento (+1) | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+3) |
| `P5` | 2 | 5\nConsulta\nde Logs | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P6` | 2 | 6\nMOD Reports; 6\nMOD Reports\n(Reportes IVR) | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P7` | 2 | 7\nBase Analitica\nIVR; 7\nServicio de\nReportes\nsp_rpt_* | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P8` | 2 | 8\nAlertas; 8\nAlertas y\nNotificaciones | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `P9` | 2 | 9\nResolver Segmento\nUC_INC_RPT_01; 9\nResolver\nSegmento\nUC_INC_RPT_01 | `arquitectura-tecnica/arquitectura-sistema/arquitectura-general.rst` (+1) |
| `R01` | 1 | UC_RPT_01\nVer Dashboard IVR | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R02` | 1 | UC_RPT_02\nVer Metricas\nTiempo Real | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R03` | 1 | UC_RPT_03\nVer Reportes\nHistoricos | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R04` | 1 | UC_RPT_04\nExportar Reporte | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R07` | 1 | UC_RPT_07\nProgramar Reporte | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R08` | 1 | UC_RPT_08\nVer Reportes\nProgramados | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R1` | 2 | Solicitar Reporte; Ver dashboard | `arquitectura-tecnica/system-view/submaquina-reporte.rst` (+1) |
| `R10` | 1 | UC_RPT_10\nGuardar Vista | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R11` | 1 | UC_RPT_11\nCompartir Reporte | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R12` | 1 | UC_RPT_12\nReporte de Agentes\n(sp_rpt_c | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R13` | 1 | UC_RPT_13\nReporte de Colas\n(sp_rpt_lla | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R14` | 1 | UC_RPT_14\nReporte de Campanas | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R15` | 1 | UC_RPT_15\nReporte de\nTransferencias\n( | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R16` | 1 | UC_RPT_16\nReporte de Menus IVR\n(sp_rpt | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R17` | 1 | UC_RPT_17\nReporte de Clientes\nUnicos\n | `arquitectura-tecnica/use-case-view/mod-reports.rst` |
| `R2` | 1 | Resolver Segmento\nUC_INC_RPT_01 | `arquitectura-tecnica/system-view/submaquina-reporte.rst` |
| `R4` | 2 | Exportar reporte; Llamar sp_rpt_* | `arquitectura-tecnica/system-view/submaquina-reporte.rst` (+1) |
| `R5` | 1 | Renderizar Reporte | `arquitectura-tecnica/system-view/submaquina-reporte.rst` |
| `S01` | 1 | UC_SUP_01\nMonitorear Llamadas\nen Vivo | `arquitectura-tecnica/use-case-view/mod-supervision.rst` |
| `S02` | 1 | UC_SUP_02\nIntervenir en\nLlamada\n(barg | `arquitectura-tecnica/use-case-view/mod-supervision.rst` |
| `S03` | 1 | UC_SUP_03\nEnviar Mensaje\nal Equipo | `arquitectura-tecnica/use-case-view/mod-supervision.rst` |
| `S1` | 1 | Recibir Solicitud ETL | `arquitectura-tecnica/system-view/submaquina-etl.rst` |
| `S3` | 1 | Verificar Resultado | `arquitectura-tecnica/system-view/submaquina-etl.rst` |
| `U01` | 2 | UC_RPT_01\nVer Dashboard; UC_USR_01\nCrear Usuario | `arquitectura-tecnica/use-case-view/mod-users.rst` (+1) |
| `U02` | 2 | UC_RPT_02\nVer Métricas Tiempo Real; UC_USR_02\nConsultar Usuarios | `arquitectura-tecnica/use-case-view/mod-users.rst` (+1) |
| `U03` | 2 | UC_RPT_03\nVer Reportes Históricos; UC_USR_03\nModificar Usuario | `arquitectura-tecnica/use-case-view/mod-users.rst` (+1) |
| `U04` | 2 | UC_RPT_04\nExportar Reporte; UC_USR_04\nEliminar Usuario\n(baja logic | `arquitectura-tecnica/use-case-view/mod-users.rst` (+1) |
| `U07` | 1 | UC_RPT_07\nProgramar Reporte | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U08` | 1 | UC_RPT_08\nVer Programados | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U09` | 1 | UC_RPT_09\nConfigurar Filtros | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U1` | 1 | CRUD usuarios | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `U10` | 1 | UC_RPT_10\nGuardar Vista | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U11` | 1 | UC_RPT_11\nCompartir Reporte | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U12` | 1 | UC_RPT_12\nReporte Agentes | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U13` | 1 | UC_RPT_13\nReporte Colas | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |
| `U14` | 1 | UC_RPT_14\nReporte Campañas | `_metodologia-aplicacion/diagramas-uml/diagrama-de-casos-de-uso-uc-rpt-reportes-14-ucs.rst` |

## 2 letras + número (42 aliases, 85 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `AC01` | 1 | UC_ACC_01\nAsignar Funciones\na Usuario | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC02` | 1 | UC_ACC_02\nRevocar Funciones\nde Usuario | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC03` | 1 | UC_ACC_03\nConsultar Permisos\nEfectivos | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC04` | 1 | UC_ACC_04\nAsignar Agrupador\na Usuario | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC05` | 1 | UC_ACC_05\nGestionar Reglas SoD | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC08` | 1 | UC_ACC_08\nOtorgar Permiso\nTemporal Exc | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC09` | 1 | UC_ACC_09\nAuditar Cambios\nde Acceso | `arquitectura-tecnica/use-case-view/mod-access.rst` |
| `AC1` | 1 | Asignar funciones | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `AC5` | 1 | Gestionar SoD | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `AL01` | 1 | UC_ALR_01\nConfigurar Umbrales\nde Alert | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `AL02` | 1 | UC_ALR_02\nVer Alertas Activas | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `AL03` | 1 | UC_ALR_03\nReconocer Alerta | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `AL04` | 1 | UC_ALR_04\nVer Historial\nde Alertas | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `AL05` | 1 | UC_ALR_05\nNotificacion\nAutomatica ETL | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `AL3` | 1 | Reconocer alerta | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `AU1` | 1 | Consultar auditoría | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `DS1` | 1 | etl_runs | `arquitectura-tecnica/arquitectura-sistema/dfd-nivel-1-subprocesos.rst` |
| `DS2` | 1 | base_ivr_* | `arquitectura-tecnica/arquitectura-sistema/dfd-nivel-1-subprocesos.rst` |
| `DS3` | 1 | audit_log | `arquitectura-tecnica/arquitectura-sistema/dfd-nivel-1-subprocesos.rst` |
| `DS4` | 1 | auth_session | `arquitectura-tecnica/arquitectura-sistema/dfd-nivel-1-subprocesos.rst` |
| `PE7` | 1 | Verificar permiso | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `PE8` | 1 | Generar menú\ndinámico | `_metodologia-aplicacion/casos-uso-diagramas/agrupamiento-con-paquetes.rst` |
| `UC01` | 9 | UC_ACC_01\nAsignar Funciones; UC_ALR_01\nConfigurar Umbrales (+7) | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` (+8) |
| `UC02` | 8 | UC_ACC_02\nRevocar Funciones; UC_ALR_02\nAlertas Activas (+6) | `uc-acc-02/diagramas-uml/diagrama-de-caso-de-uso.rst` (+7) |
| `UC03` | 9 | UC_ACC_03\nConsultar Permisos; UC_ALR_03\nAck inline (+7) | `uc-acc-03/diagramas-uml/diagrama-de-caso-de-uso.rst` (+8) |
| `UC04` | 10 | UC_ACC_04\nAsignar AGR; UC_ALR_04\nHistorial (+8) | `uc-acc-04/diagramas-uml/diagrama-de-caso-de-uso.rst` (+9) |
| `UC05` | 4 | UC_ACC_05\nGestionar SoD; UC_ALR_05\nSubscriptions (+2) | `uc-acc-05/diagramas-uml/diagrama-de-caso-de-uso.rst` (+3) |
| `UC06` | 2 | UC_LOG_06\nEstado Sistema; UC_PERM_06\nComposicion AGR | `uc-log-06/diagramas-uml/caso-de-uso.rst` (+1) |
| `UC07` | 4 | UC_LOG_07\nMetricas; UC_PERM_07\nVerificar Permiso (+2) | `uc-log-07/diagramas-uml/caso-de-uso.rst` (+3) |
| `UC08` | 3 | UC_ACC_08\nPermiso Temporal; UC_PERM_08\nGenerar Menu (+1) | `uc-acc-08/diagramas-uml/diagrama-de-caso-de-uso.rst` (+2) |
| `UC09` | 3 | UC_ACC_09\nAuditar Cambios; UC_PERM_09\nAuditar Acceso (+1) | `uc-acc-09/diagramas-uml/diagrama-de-caso-de-uso.rst` (+2) |
| `UC1` | 1 | Comprar gaseosa | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-visual-maquina-de-gaseosas-referencia-generica.rst` |
| `UC10` | 1 | UC_RPT_10\nGuardar Vista | `uc-rpt-10/diagramas-uml/caso-de-uso.rst` |
| `UC11` | 1 | UC_RPT_11\nCompartir | `uc-rpt-11/diagramas-uml/caso-de-uso.rst` |
| `UC12` | 1 | UC_RPT_12\nReporte Agentes | `uc-rpt-12/diagramas-uml/caso-de-uso.rst` |
| `UC13` | 1 | UC_RPT_13\nReporte Abandono | `uc-rpt-13/diagramas-uml/caso-de-uso.rst` |
| `UC14` | 1 | UC_RPT_14\nReporte Campanas | `uc-rpt-14/diagramas-uml/caso-de-uso.rst` |
| `UC15` | 1 | UC_RPT_15\nReporte Transferencias | `uc-rpt-15/diagramas-uml/caso-de-uso.rst` |
| `UC16` | 1 | UC_RPT_16\nReporte Menus IVR | `uc-rpt-16/diagramas-uml/caso-de-uso.rst` |
| `UC17` | 1 | UC_RPT_17\nClientes Unicos IVR | `uc-rpt-17/diagramas-uml/caso-de-uso.rst` |
| `UC2` | 1 | Reabastecer | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-visual-maquina-de-gaseosas-referencia-generica.rst` |
| `UC3` | 1 | Recolectar el dinero | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-visual-maquina-de-gaseosas-referencia-generica.rst` |

## Abreviatura + número (25 aliases, 40 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `ACC01` | 1 | UC_ACC_01\nAsignar funciones | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` |
| `ACC02` | 1 | UC_ACC_02\nRevocar\n(generico) | `uc-perm-02/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `ACC04` | 1 | UC_ACC_04\nAsignar AGR\n(desde User) | `uc-perm-01/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `ACC08` | 1 | UC_ACC_08\nGrant excepcional | `uc-perm-03/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `ADM01` | 1 | UC_ADM_01\nGestionar Ciclo\nde Vida de R | `arquitectura-tecnica/use-case-view/mod-admin.rst` |
| `ADM02` | 1 | UC_ADM_02\nGestionar Catalogo\nde Funcio | `arquitectura-tecnica/use-case-view/mod-admin.rst` |
| `ADM03` | 1 | UC_ADM_03\nGestionar Catalogo\nde Agrupa | `arquitectura-tecnica/use-case-view/mod-admin.rst` |
| `ALR03` | 1 | UC_ALR_03\nReconocer alerta | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` |
| `AUD01` | 2 | UC_AUD_01\nConsultar auditoría | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `AUD03` | 2 | UC_AUD_03\nConsultar audit; UC_AUD_03\nExportar auditoría | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `AUTH01` | 2 | UC_AUTH_01\nIniciar sesión; UC_AUTH_01\nLogin | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `INC01` | 1 | UC_INC_RPT_01\nResolver Segmento | `uc-inc-rpt-01/diagramas-uml/caso-de-uso-relacion-de-inclusion.rst` |
| `PERM01` | 1 | UC_PERM_01\nAsignar Grupo\n(desde catalo | `uc-perm-01/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `PERM02` | 1 | UC_PERM_02\nRevocar AGR\n(catalogo) | `uc-perm-02/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `PERM03` | 1 | UC_PERM_03\nGrant excepcional | `uc-perm-03/diagramas-uml/diagrama-de-coexistencia-acc-perm.rst` |
| `PERM07` | 2 | UC_PERM_07\nVerificar permiso | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `PIP01` | 2 | UC_PIP_01\nCarga ETL; UC_PIP_01\nSupervisar ETL | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `PIP04` | 2 | UC_PIP_04\nSolicitar reintento; UC_PIP_04\nSolicitar reintento ETL | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `RPT01` | 2 | UC_RPT_01\nVer dashboard | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+1) |
| `RPT03` | 4 | UC_RPT_03\nVer reportes históricos; UC_RPT_03\nVer reportes\nhistóricos (+2) | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-03-ver-reportes-historicos-extendido.rst` (+3) |
| `RPT04` | 3 | UC_RPT_04\nExportar reporte | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst` (+2) |
| `RPT07` | 1 | UC_RPT_07\nReporte programado | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact.rst` |
| `RPT09` | 2 | UC_RPT_09\nConfigurar filtros; UC_RPT_09\nConfigurar\nfiltros\n(EXTIEND | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-03-ver-reportes-historicos-extendido.rst` (+1) |
| `RPT10` | 2 | UC_RPT_10\nGuardar vista; UC_RPT_10\nGuardar vista\n(EXTIENDE) | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-03-ver-reportes-historicos-extendido.rst` (+1) |
| `RPT11` | 2 | UC_RPT_11\nCompartir reporte; UC_RPT_11\nCompartir reporte\n(EXTIENDE) | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-03-ver-reportes-historicos-extendido.rst` (+1) |

## Abreviatura corta (2-5 chars) (76 aliases, 198 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `ABT` | 2 | AbortadaPorError; AbortadoFlowFinal | `_metodologia-aplicacion/diagramas-estados/flow-final-abort-anormal.rst` (+1) |
| `ADMIN` | 6 | create_users; reset_password (+3) | `user-identity/diagramas/secuencia-creacion-usuario.rst` (+5) |
| `ALERT` | 1 | AlertEvaluator\n(BR-016 tasa abandono) | `caller/diagramas/pipeline-datos-ivr-caller.rst` |
| `ALR` | 1 | Alerts Service\nUmbrales, Notif | `_metodologia-aplicacion/diagramas-uml/diagrama-de-componentes-arquitectura-del-sistema-iact.rst` |
| `ANAL` | 2 | base_ivr_detalle\nbase_ivr_clientes\n(Ba | `caller/diagramas/pipeline-datos-ivr-caller.rst` (+1) |
| `APPS` | 1 | auth_app, perm_app,\nrpt_app, alr_app,\n | `_metodologia-aplicacion/diagramas-distribucion/vista-de-despliegue-global-iact.rst` |
| `AREP` | 2 | AssignmentRepository; audit_log\n(PostgreSQL — append-only) | `audit/diagramas/flujo-emision-evento-auditoria.rst` (+1) |
| `AUD` | 3 | Audit Service\nInmutable; Registrar en\nAuditLog\n(CNST_025) | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-04-exportar-reporte.rst` (+2) |
| `AUDIT` | 3 | audit_log\n(MySQL,\nimmutable CNST_025); audit_log\n(PostgreSQL) (+1) | `etl-monitoring/diagramas/componentes-mod-pipeline.rst` (+2) |
| `AUDS` | 3 | Audit P-16\nselectivo; Audit selectivo\n(P-16) (+1) | `uc-acc-03/diagramas-uml/diagrama-de-caso-de-uso.rst` (+2) |
| `AUTH` | 3 | ARQ_MOD_001\nAutenticación; Autenticacion JWT (+1) | `auth/diagramas/diagrama-contexto-dependencias.rst` (+2) |
| `AUTO` | 1 | Ejecutar ETL\nAutomatico\n(sp_etl_maestr | `arquitectura-tecnica/use-case-view/mod-pipeline.rst` |
| `BDA` | 12 | bd_analytics; bd_analytics\n(MySQL) (+2) | `_metodologia-aplicacion/diagramas-componentes/ejemplo-iact-component-view-de-iact-wsgi.rst` (+11) |
| `BDO` | 14 | :bd_operativa; BD operativa\n(call center) (+8) | `_metodologia-aplicacion/diagramas-colaboraciones/mensaje-en-bucle.rst` (+13) |
| `BULK` | 1 | Bulk check | `uc-perm-07/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `CACHE` | 5 | Cache lookup; Invalidar cache (+2) | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` (+4) |
| `CALC` | 1 | Calcular post-revoke\n+ warnings | `uc-acc-02/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `CALL` | 1 | Cerrar todas\nlas del User | `uc-auth-05/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `COMP` | 1 | Validar complejidad | `uc-auth-04/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `CONS` | 1 | Consolidar\n+ metadata origen | `uc-acc-03/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `CRUD` | 1 | Crear/Update | `uc-rpt-07/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `DASH` | 2 | Dashboard IACT; PerformanceDashboard\n(view_own_performa | `operator/diagramas/componentes-mod-operator.rst` (+1) |
| `DB` | 1 | — | `_metodologia-aplicacion/diagramas-uml/diagrama-de-distribucion-despliegue-del-proyecto-iact.rst` |
| `DEST` | 2 | base_ivr_clientes\n(telefono_hashed); base_ivr_detalle\nbase_ivr_clientes\n(Ba | `etl-monitoring/diagramas/flujo-etl-nocturno.rst` (+1) |
| `DISP` | 2 | DispositionEndpoint\n(/api/v1/dispositio; DispositionService\n(enter_call_disposit | `operator/diagramas/componentes-mod-operator.rst` (+1) |
| `EP` | 1 | SystemGroupEndpoint | `uc-adm-03/diagramas-uml/impacto.rst` |
| `ETL` | 9 | :etl_runner; Carga ETL\nnocturna (+4) | `arquitectura-tecnica/context-view/context-diagram.rst` (+8) |
| `FINAL` | 1 | Cierre de Sesion | `arquitectura-tecnica/system-view/maquina-estados-sistema-iact.rst` |
| `FULL` | 1 | Sesion scope pleno | `uc-auth-04/diagramas-uml/diagrama-de-estados-user-first-login-scope.rst` |
| `HIST` | 4 | AlertEvent\n(historico alertas); Verificar historial\n(no reuso) (+2) | `alerts/diagramas/componentes-mod-alerts.rst` (+3) |
| `HTTP` | 1 | HTTP Client\nAxios + JWT | `_metodologia-aplicacion/diagramas-uml/diagrama-de-componentes-arquitectura-del-sistema-iact.rst` |
| `IACT` | 8 |   1\n  Sistema IACT\n  (Analisis IVR Cal;   Sistema IACT   (+4) | `arquitectura-tecnica/arquitectura-sistema/dfd-nivel-0-contexto.rst` (+5) |
| `IDEM` | 1 | Filtrar idempotente | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `IVR` | 13 | BD Operativa IVR\n(MariaDB — solo lectur; IVR Conmutador\n(read-only) (+7) | `arquitectura-tecnica/context-view/context-diagram.rst` (+12) |
| `IVRDB` | 1 | base_ivr_detalle\nbase_ivr_clientes | `vis-reports/diagramas/secuencia-sp-rpt-flujo-completo.rst` |
| `LDAP` | 19 | :ldap-corporativo; LDAP corporativo (+5) | `_metodologia-aplicacion/diagramas-colaboraciones/reverse-stimulus-request-respuesta.rst` (+18) |
| `LOG` | 1 | — | `_metodologia-aplicacion/diagramas-componentes/vista-detallada-con-interfaces-lollipop.rst` |
| `MENU` | 1 | view_own_navigation | `uc-perm-07/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `MOTOR` | 1 | Motor de Alertas\n(automatico) | `arquitectura-tecnica/use-case-view/mod-alerts.rst` |
| `OETL` | 3 | Operador ETL; Operador ETL\n[Person] | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact.rst` (+2) |
| `OOP` | 1 | Orientación a Objetos en IACT | `_metodologia-aplicacion/orientacion-objetos/resumen-visual-de-los-6-principios.rst` |
| `PA` | 1 | Acceso & RBAC | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` |
| `PD` | 1 | Auditoría | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` |
| `PE` | 2 | PermissionsEngine; Pipeline ETL | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` (+1) |
| `PERM` | 2 | UC_PERM_07\nVerificar permiso\n+ throttl | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-04-exportar-reporte.rst` (+1) |
| `PIP` | 1 | ETL Supervisor\nestado, reintento | `_metodologia-aplicacion/diagramas-uml/diagrama-de-componentes-arquitectura-del-sistema-iact.rst` |
| `PL` | 1 | Llamadas / IVR | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` |
| `PN` | 1 | Alertas / Notificaciones | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` |
| `PR` | 1 | Reportes / Métricas | `_metodologia-aplicacion/analisis-dominio/conversion-a-clases-vista-global-del-dominio.rst` |
| `RBAC` | 2 | ARQ_MOD_003\nControl de Acceso\n(RBAC); RBAC Service\nFunciones, Grupos | `auth/diagramas/diagrama-contexto-dependencias.rst` (+1) |
| `REDIS` | 2 | Redis; Redis\n(sesiones, throttling) | `_metodologia-aplicacion/diagramas-componentes/vista-fisica-global-de-iact.rst` (+1) |
| `REST` | 1 | REST API\nViewSets | `_metodologia-aplicacion/diagramas-uml/diagrama-de-componentes-arquitectura-del-sistema-iact.rst` |
| `RPT` | 2 | Reports Service\nMétricas, Export | `_metodologia-aplicacion/diagramas-componentes/vista-detallada-con-interfaces-lollipop.rst` (+1) |
| `RPTNN` | 1 | UC_RPT_NN\n(cualquier reporte) | `uc-inc-rpt-01/diagramas-uml/caso-de-uso-relacion-de-inclusion.rst` |
| `RPTS` | 1 | apps.reports\n(API views) | `vis-reports/diagramas/componentes-mod-reports.rst` |
| `RUNS` | 2 | Historico runs; etl_runs\n(registro de ejecuciones) | `etl-monitoring/diagramas/componentes-mod-pipeline.rst` (+1) |
| `SCHED` | 1 | ETLScheduler\n(tarea programada) | `etl-monitoring/diagramas/componentes-mod-pipeline.rst` |
| `SEG` | 1 | Aplicar filtro\nsegmento\n(BR_012,\nCNST | `_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-uc-rpt-04-exportar-reporte.rst` |
| `SESS` | 1 | auth_session\n(PostgreSQL) | `operator/diagramas/componentes-mod-operator.rst` |
| `STATE` | 2 | agent_state\n(cache) | `operator/diagramas/componentes-mod-operator.rst` (+1) |
| `SUCC` | 1 | ETL Exitoso | `arquitectura-tecnica/system-view/submaquina-etl.rst` |
| `TONE` | 1 | ComplianceToneEmitter\n(tono obligatorio | `supervision/diagramas/componentes-mod-supervision.rst` |
| `UCCRE` | 2 | Crear regla; UC_PERM_05\nCreate AGR | `uc-acc-05/diagramas-uml/diagrama-de-caso-de-uso.rst` (+1) |
| `UCMOD` | 2 | Modificar regla; UC_PERM_05\nModify AGR | `uc-acc-05/diagramas-uml/diagrama-de-caso-de-uso.rst` (+1) |
| `UCRET` | 2 | Retirar regla; UC_PERM_05\nRetire AGR | `uc-acc-05/diagramas-uml/diagrama-de-caso-de-uso.rst` (+1) |
| `UR` | 1 | UserRepo | `uc-adm-03/diagramas-uml/impacto.rst` |
| `UREP` | 1 | UserRepository | `uc-usr-02/diagramas-uml/diagrama-de-secuencia-detalle.rst` |
| `USER` | 7 | Nuevo User; User (+4) | `uc-auth-02/diagramas-uml/diagrama-de-caso-de-uso.rst` (+6) |
| `USERS` | 2 | Repositorio\nde Usuarios; Users con AGR | `auth/diagramas/flujo-autenticacion.rst` (+1) |
| `USRD` | 1 | view_reports | `uc-rpt-12/diagramas-uml/caso-de-uso.rst` |
| `VAGR` | 1 | Validar AGR\nexiste + ACTIVE | `uc-acc-04/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `VFUN` | 1 | Validar funciones\n(existen + activas) | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `VIEW` | 1 | view_alerts\n(consulta) | `alerts/diagramas/componentes-mod-alerts.rst` |
| `VSOD` | 3 | Validar SoD\n(CNST-005); Validar SoD\ncascade (+1) | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` (+2) |
| `VUSER` | 1 | Validar User destino | `uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst` |
| `WSGI` | 7 | iact.wsgi; iact.wsgi\n[Django + mod_wsgi sobre Apac (+2) | `_metodologia-aplicacion/diagramas-componentes/vista-fisica-global-de-iact.rst` (+6) |

## Prefijo UC_ (15 aliases, 15 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `UC_ACC` | 1 | Acceder a\nModulos | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_AUTH` | 1 | Autenticar JWT | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_DASH` | 1 | Ver Dashboard IVR | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_DISP` | 1 | Ver Disponibilidad\nde Datos | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_INC` | 1 | Resolver Segmento\nUC_INC_RPT_01 | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_LOG` | 1 | Consultar Logs\n(view_audit_log) | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_LOGOUT` | 1 | Cerrar Sesion | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_PIP` | 1 | Gestionar\nPipeline ETL | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_R13` | 1 | Ver Llamadas\nAbandonadas\n(sp_rpt_llama | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_R15` | 1 | Ver\nTransferencias\n(sp_rpt_centros_tra | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_R16` | 1 | Ver Menus IVR\n(sp_rpt_menu_redirigidos) | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_R17` | 1 | Ver Clientes\nUnicos\n(sp_rpt_clientes) | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_RBAC` | 1 | Gestionar\nFunciones RBAC | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_RPT` | 1 | Ver Reportes IVR | `arquitectura-tecnica/system-view/casos-uso-sistema-iact.rst` |
| `UC_RPT_04` | 1 | — | `audit/uc-aud-03/implementacion-tecnica.rst` |

## F_ + abreviatura (57 aliases, 57 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `F_ACA` | 1 | acknowledge_alert | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_AF` | 1 | assign_functions | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_AFG` | 1 | assign_function_groups | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_AIC` | 1 | answer_inbound_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_BIC` | 1 | barge_in_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_BTM` | 1 | broadcast_team_messages | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_CU` | 1 | create_users | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_DU` | 1 | deactivate_users | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_EA` | 1 | export_audit_log | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_ECD` | 1 | enter_call_disposition | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_ECSV` | 1 | export_csv | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_EL` | 1 | export_logs | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_EPDF` | 1 | export_pdf | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_EXL` | 1 | export_excel | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_FR` | 1 | filter_reports | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_GCR` | 1 | generate_compliance_report | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_HC` | 1 | hold_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_LU` | 1 | list_users | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MAG` | 1 | create_function_group | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MAGC` | 1 | assign_functions_to_group | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MAT` | 1 | configure_team_alerts | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MLC` | 1 | monitor_live_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MOAS` | 1 | manage_own_agent_state | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_MOC` | 1 | make_outbound_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_RBK` | 1 | request_break | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_RE` | 1 | request_pipeline_retry | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_RF` | 1 | revoke_functions | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_RFG` | 1 | revoke_function_group | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_ROM` | 1 | read_own_mailbox | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SA` | 1 | search_audit_log | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SCH` | 1 | schedule_report | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SESS` | 1 | view_all_active_sessions | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SHR` | 1 | share_report | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SL` | 1 | search_logs | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_SV` | 1 | save_view | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_TC` | 1 | transfer_calls | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_UU` | 1 | update_users | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VA` | 1 | view_assignments | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VAA` | 1 | view_audit_log | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VAH` | 1 | view_alert_history | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VCH` | 1 | view_charts | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VD` | 1 | view_dashboard | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VDD` | 1 | view_data_availability | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VEE` | 1 | view_pipeline_status | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VEER` | 1 | view_pipeline_errors | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VEL` | 1 | view_etl_logs | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VGA` | 1 | view_audit_log | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VIL` | 1 | view_infrastructure_logs | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VK` | 1 | view_kpis | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VOCH` | 1 | view_own_call_history | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VON` | 1 | view_own_navigation | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VOPD` | 1 | view_own_performance_dashboard | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VR` | 1 | view_reports | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VSL` | 1 | view_application_logs | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VSR` | 1 | view_separation_rules | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VSS` | 1 | view_system_health | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |
| `F_VTM` | 1 | view_technical_metrics | `arquitectura-tecnica/rbac/rbac-funciones-por-modulo.rst` |

## Prefijo técnico + abreviatura (60 aliases, 61 ocurrencias)

| Alias | Occ | Label(s) | Archivos |
|-------|-----|----------|----------|
| `ART_A1` | 1 | <<artifact>>\nAccessGroup | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_A2` | 1 | <<artifact>>\nAccessFunction | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_AUDIT` | 1 | audit_log | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_BASE` | 1 | base_ivr_detalle\nbase_ivr_clientes\n(Ba | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_E1` | 1 | <<artifact>>\nsp_etl_maestro | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_E2` | 1 | <<artifact>>\netl_runs | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_HIST` | 1 | tbl_historico_*\n(Repositorio IVR) | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_L1` | 1 | <<artifact>>\naudit_log | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_PAG` | 1 | <<artifact>>\nUser_View\n(JWT + view_pip | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_R1` | 1 | <<artifact>>\nsp_rpt_llamadas_abandonada | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R2` | 1 | <<artifact>>\nsp_rpt_centros_transferenc | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R3` | 1 | <<artifact>>\nsp_rpt_menu_redirigidos | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R4` | 1 | <<artifact>>\nsp_rpt_clientes | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R5` | 1 | <<artifact>>\nsp_rpt_centros_xsegmento | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R6` | 1 | <<artifact>>\nsp_rpt_menu_centro | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_R7` | 1 | <<artifact>>\nsp_rpt_cMENU_ERROR | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_REQ` | 1 | <<artifact>>\nReport Request Buffer\n(JW | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_RVG` | 1 | <<artifact>>\nUser_View\n(JWT + view_rep | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_S1` | 1 | <<artifact>>\nsp_rpt_centros_xsegmento | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_S2` | 1 | <<artifact>>\nsp_rpt_llamadas_abandonada | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_UAG` | 1 | <<artifact>>\nUser_View\n(JWT + assign_f | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `ART_USERS` | 1 | auth_user\n(AccessGroup / AccessFunction | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `ART_WSGI` | 1 | <<artifact>>\niact-app.wsgi | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `BROWSER_PAG` | 1 | <<app>>\nNavegador Web | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `BROWSER_RVG` | 1 | <<app>>\nNavegador Web | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `BR_PAG` | 1 | <<app>>\nNavegador (Chrome / Firefox) | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `BR_RVG` | 1 | <<app>>\nNavegador (Chrome / Firefox) | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `BR_UAG` | 1 | <<app>>\nNavegador (Chrome / Firefox) | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `CLI_PAG` | 1 | request_pipeline_retry\nos WINDOWS / Lin | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `CLI_RVG` | 1 | view_reports\nos WINDOWS / MacOS | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `CLI_UAG` | 1 | assign_functions\nos WINDOWS | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `COMP_BACK` | 1 | <<System>>\nBackend IACT | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `COMP_RVG` | 1 | <<System>>\nview_reports\n(view_reports  | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `DB_AUDIT` | 1 | audit_log | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `DB_AUTH` | 1 | <<artifact>>\nauth_user\naudit_log | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `DB_ETLR` | 1 | etl_runs | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `DB_HIST` | 2 | <<artifact>>\ntbl_historico_*; tbl_historico_* | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` (+1) |
| `DB_IVR` | 1 | <<artifact>>\nbase_ivr_detalle\nbase_ivr | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `DB_MARIA` | 1 | <<subsystem>>\nMariaDB 10.1.48 | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `DB_PG` | 1 | <<subsystem>>\nPostgreSQL | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `DB_USERS` | 1 | auth_user\nAccessGroup / AccessFunction | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `MOD_ADM` | 1 | MOD_Admin\n(assign_functions / create_us | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `MOD_ETL` | 1 | MOD_Pipeline ETL\n(view_pipeline_status  | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `MOD_LOG` | 1 | MOD_Logs\n(view_audit_log) | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `MOD_RPT` | 1 | MOD_Reports\n(view_reports / view_dashbo | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `NODE_APP` | 1 | <<server>>\nServidor de Aplicacion | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `NODE_DB` | 1 | Database | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `NODE_MARIA` | 1 | <<database system>>\nMariaDB 10.1.48 | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `NODE_PAG` | 1 | <<client>>\nrequest_pipeline_retry\n(PC  | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `NODE_PG` | 1 | <<database system>>\nPostgreSQL | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `NODE_RVG` | 1 | <<client>>\nview_reports\n(PC / Navegado | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `NODE_SRV` | 1 | <<server>>\nServidor IACT | `arquitectura-tecnica/system-view/despliegue-multicliente.rst` |
| `SCH_BASE` | 1 | Website data\nbase_ivr | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `SCH_ETL` | 1 | ETL control\netl_control | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `SCH_FUENTE` | 1 | IVR source\nivr_fuente | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `SCH_PG` | 1 | operational\niact_operational | `arquitectura-tecnica/system-view/despliegue-sistema-iact.rst` |
| `SVC_AUTH` | 1 | <<process>>\nAuthService\n(JWT + RBAC) | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `SVC_ETL` | 1 | <<process>>\nDisparadorETL\n(management  | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `SVC_OUTER` | 1 | Suggestion\nServicio de Reportes | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |
| `SVC_SEG` | 1 | <<process>>\nSegmentResolver\n(DID_MAP) | `arquitectura-tecnica/system-view/componentes-sistema-iact.rst` |

## Aliases limpios (CLEAN) — sin violación

| Alias | Occ | Label(s) |
|-------|-----|----------|
| `A1B` | 1 | UC_AUTH_01b\nIniciar sesión\ncon 2FA |
| `AGR_ADMIN` | 1 | agr_admin |
| `APACHE` | 1 | Apache + mod_wsgi |
| `ART_CACHE_RVG` | 1 | <<artifact>>\nCache Reportes (30s) |
| `ART_ETLRUNS` | 1 | etl_runs\n(Registro ETL) |
| `ART_JWT_PAG` | 1 | <<artifact>>\nJWT Token (LocalStorage) |
| `ART_JWT_RVG` | 1 | <<artifact>>\nJWT Token (LocalStorage) |
| `ART_SETTINGS` | 1 | <<artifact>>\nsettings.py\n(DATABASES: ivr + defau |
| `ASIGNAR_GRUPO_RBAC` | 1 | Asignar grupo RBAC\n(FunctionGroup/AccessGroup) |
| `AUDIT_EVENT` | 1 | AuditEvent\n(append-only) |
| `AUDLOG` | 1 | Registrar en AuditLog\n(CNST_025) |
| `BUSINESS_LOGIC` | 1 | Business\nLogic |
| `CALLER` | 3 | Caller\n(externo); write_audit_event |
| `CERRAR_SESIONES` | 1 | Cerrar sesiones\n(view_all_active_sessions) |
| `CREAR_USUARIO` | 1 | Crear usuario |
| `DB_CLIENTES` | 1 | base_ivr_clientes |
| `DB_DETALLE` | 1 | base_ivr_detalle |
| `DESACTIVAR_USUARIO` | 1 | Desactivar usuario\n(BR-009 v2.0.0) |
| `DRF_API` | 1 | DRF\nAPI |
| `ETLORM` | 1 | ETLEjecucionORM\nETLLogORM |
| `ETL_EXEC` | 1 | Ejecucion ETL |
| `ETL_LOG` | 1 | etl_runs |
| `ETL_SP` | 1 | sp_etl_maestro\n(Almacen de Datos SP) |
| `F_VAA2` | 1 | view_alerts |
| `HMACKMS` | 1 | HMACKMS |
| `IACT_SVC` | 1 | <<service>>\nBackend IACT |
| `INVOKER` | 9 | assign_function_groups; assign_functions |
| `MANAGER` | 1 | view_separation_rules |
| `OS_LINUX` | 1 | <<OS>>\nLinux |
| `OTORGAR_PERMISO_TEMPORAL` | 1 | Otorgar permiso temporal\n(CNST-031: max 6 meses) |
| `P4B` | 1 | UC_PIP_04b\nReintentar con\nparámetros ajustados |
| `R3A` | 1 | Segmento nacional_A\n(DID 19028031) |
| `R3B` | 1 | Segmento nacional_B\n(DID 19020001) |
| `R3C` | 1 | Segmento Puebla\n(DID 19020084) |
| `RBAC_MIDDLEWARE` | 1 | RBAC\nMiddleware |
| `REDUCED` | 1 | Sesion scope reducido |
| `REVOCAR_GRUPO_RBAC` | 1 | Revocar grupo RBAC |
| `REVOCAR_PERMISO_TEMPORAL` | 1 | Revocar permiso temporal |
| `RPT_EXEC` | 1 | Consulta de Reporte IVR |
| `S2A` | 1 | sp_etl_base_detalle |
| `S2B` | 1 | sp_etl_base_clientes |
| `SESSIONS` | 1 | Repositorio\nde Sesiones |
| `S_DASH` | 1 | Ver Dashboard IVR\n[view_dashboard] |
| `S_ETL` | 1 | Gestion Pipeline ETL\n[view_pipeline_status] |
| `S_LOG` | 1 | Consulta de Logs\n[view_audit_log] |
| `S_RBAC` | 1 | Gestion RBAC\n[assign_functions] |
| `S_RPT` | 1 | MOD Reports\n[view_reports] |
| `TARGET` | 6 | User consultado; User destino |
| `UIBUNDLE` | 1 | iact-admin.bundle.js |
| `USUARIO` | 1 | Usuario\n(cualquier rol) |
| `VER_AUDIT_LOG` | 1 | Ver audit log\n(CNST-025) |
| `VER_REGLAS_SOD` | 1 | Ver reglas SoD\n(CNST-030) |
| `VER_SESIONES_ACTIVAS` | 1 | Ver sesiones activas |
| `VIEWER` | 1 | view_separation_rules |
| `WEB_SERVER` | 1 | <<WebServer>>\nGunicorn + Nginx |
