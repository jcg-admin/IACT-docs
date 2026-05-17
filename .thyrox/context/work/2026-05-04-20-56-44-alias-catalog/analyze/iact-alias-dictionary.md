```yml
created_at: 2026-05-04 21:30:00
project: THYROX
work_package: 2026-05-04-20-56-44-alias-catalog
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Diccionario de Aliases IACT

Equivalente al `diccionario_aliases.py` de referencia, adaptado al corpus IACT.

Criterios aplicados:
- Tipo 1 — módulo/BC reservado → nombre descriptivo completo con prefijo `SERVICIO_` o `BC_`
- Tipo 2 — alias numerado (UC ref) → nombre del UC que representa
- Tipo 3 — abreviatura arbitraria → palabra completa descriptiva en SCREAMING_SNAKE_CASE
- Tipo 4 — F_ función RBAC → nombre completo de la función
- Tipo 5 — prefijo técnico + abbrev → nombre descriptivo del artefacto/nodo

---

## Grupo 1 — SINGLE_LETTER (Tipo 1: BCs como letras)

Todos en `domain-model/overview.rst`. Un alias por BC.

```python
SINGLE_LETTER = {
    'A': 'BC_AUTH',
    'C': 'BC_CALLS',
    'D': 'BC_AUDIT',
    'E': 'BC_ETL',
    'G': 'BC_LOGS',
    'L': 'BC_ALERTS',
    'P': 'BC_REPORTS',
    'R': 'BC_RBAC',
}
```

---

## Grupo 2 — UC Referencias sin conflicto (Tipo 2)

Aliases que aparecen en un único contexto UC — corrección directa.

```python
# UC_CLI — Operaciones del sistema IVR (caller)
UC_CLI = {
    'C01': 'LLAMAR_SISTEMA_IVR',
    'C02': 'NAVEGAR_MENU_IVR',
    'C03': 'ESPERAR_COLA',
    'C04': 'RECIBIR_CALLBACK',
    'C05': 'RESPONDER_ENCUESTA_CSAT',
}

# UC_LOG — Consulta de logs del sistema
UC_LOG = {
    'L01': 'VER_LOGS_SISTEMA',
    'L02': 'VER_LOGS_ETL',
    'L03': 'BUSCAR_LOGS',
    'L04': 'EXPORTAR_LOGS',
    'L05': 'VER_LOGS_INFRAESTRUCTURA',
    'L06': 'VER_ESTADO_SISTEMA',
    'L07': 'VER_METRICAS_TECNICAS',
}

# UC_OPR — Operaciones del agente
UC_OPR = {
    'O01': 'CAMBIAR_ESTADO_AGENTE',
    'O02': 'ATENDER_LLAMADA',
    'O03': 'INICIAR_LLAMADA_OUTBOUND',
    'O04': 'HOLD_UNHOLD_LLAMADA',
    'O05': 'TRANSFERIR_LLAMADA',
    'O06': 'DISPOSICION_POST_LLAMADA',
    'O07': 'TOMAR_BREAK',
    'O08': 'VER_DASHBOARD_DESEMPENO',
    'O09': 'VER_HISTORIAL_LLAMADAS',
    'O10': 'VER_BUZON_MENSAJES',
}

# UC_RPT — Reportes IVR
UC_RPT = {
    'R01': 'VER_DASHBOARD_IVR',
    'R02': 'VER_METRICAS_TIEMPO_REAL',
    'R03': 'VER_REPORTES_HISTORICOS',
    'R04': 'EXPORTAR_REPORTE',
    'R07': 'PROGRAMAR_REPORTE',
    'R08': 'VER_REPORTES_PROGRAMADOS',
    'R10': 'GUARDAR_VISTA',
    'R11': 'COMPARTIR_REPORTE',
    'R12': 'REPORTE_AGENTES',
    'R13': 'REPORTE_COLAS',
    'R14': 'REPORTE_CAMPANAS',
    'R15': 'REPORTE_TRANSFERENCIAS',
    'R16': 'REPORTE_MENUS_IVR',
    'R17': 'REPORTE_CLIENTES_UNICOS',
}

# UC_SUP — Supervisor
UC_SUP = {
    'S01': 'MONITOREAR_LLAMADAS_EN_VIVO',
    'S02': 'INTERVENIR_LLAMADA',
    'S03': 'ENVIAR_MENSAJE_EQUIPO',
}

# UC_ACC — Acceso y permisos
UC_ACC = {
    'AC01': 'ASIGNAR_FUNCIONES_A_USUARIO',
    'AC02': 'REVOCAR_FUNCIONES_DE_USUARIO',
    'AC03': 'CONSULTAR_PERMISOS_EFECTIVOS',
    'AC04': 'ASIGNAR_AGRUPADOR_A_USUARIO',
    'AC05': 'GESTIONAR_REGLAS_SOD',
    'AC08': 'OTORGAR_PERMISO_TEMPORAL',
    'AC09': 'AUDITAR_CAMBIOS_ACCESO',
    'ACC01': 'ASIGNAR_FUNCIONES_A_USUARIO',
    'ACC02': 'REVOCAR_FUNCIONES_GENERICO',
    'ACC04': 'ASIGNAR_AGRUPADOR_DESDE_USER',
    'ACC08': 'GRANT_EXCEPCIONAL',
}

# UC_ALR — Alertas
UC_ALR = {
    'AL01': 'CONFIGURAR_UMBRALES_ALERTAS',
    'AL02': 'VER_ALERTAS_ACTIVAS',
    'AL03': 'RECONOCER_ALERTA',
    'AL04': 'VER_HISTORIAL_ALERTAS',
    'AL05': 'NOTIFICACION_AUTOMATICA_ETL',
    'ALR03': 'RECONOCER_ALERTA',
}

# UC_AUD — Auditoría
UC_AUD = {
    'AUD01': 'CONSULTAR_AUDITORIA',
    'AUD03': 'EXPORTAR_AUDITORIA',
    'AU1':   'CONSULTAR_AUDITORIA',
}

# UC_ADM — Administración RBAC
UC_ADM = {
    'ADM01': 'GESTIONAR_CICLO_VIDA_SOD',
    'ADM02': 'GESTIONAR_CATALOGO_FUNCIONES',
    'ADM03': 'GESTIONAR_CATALOGO_AGRUPADORES',
}

# UC_PIP — Pipeline ETL
UC_PIP = {
    'PIP01': 'SUPERVISAR_ETL',
    'PIP04': 'SOLICITAR_REINTENTO_ETL',
}

# UC_AUTH — Autenticación
UC_AUTH = {
    'AUTH01': 'INICIAR_SESION',
}

# UC_PERM — Permisos RBAC
UC_PERM = {
    'PERM01': 'ASIGNAR_GRUPO_DESDE_CATALOGO',
    'PERM02': 'REVOCAR_AGR_CATALOGO',
    'PERM03': 'GRANT_EXCEPCIONAL',
    'PERM07': 'VERIFICAR_PERMISO',
}

# UC_RPT (formato largo)
UC_RPT_LARGO = {
    'RPT01': 'VER_DASHBOARD_IVR',
    'RPT03': 'VER_REPORTES_HISTORICOS',
    'RPT04': 'EXPORTAR_REPORTE',
    'RPT07': 'PROGRAMAR_REPORTE',
    'RPT09': 'CONFIGURAR_FILTROS',
    'RPT10': 'GUARDAR_VISTA',
    'RPT11': 'COMPARTIR_REPORTE',
    'INC01': 'RESOLVER_SEGMENTO',
}

# UC_INC (includes)
UC_INC = {
    'INC01': 'RESOLVER_SEGMENTO',
}
```

---

## Grupo 3 — UC Referencias CON CONFLICTO (por archivo)

Estos alias apuntan a UCs distintos según el archivo fuente.
Requieren corrección individual por archivo, igual que `ORD`/`WH` en la referencia.

| Alias conflictivo | Contexto A | Corrección A | Contexto B | Corrección B |
|-------------------|-----------|--------------|-----------|--------------|
| `A01` | mod-auth.rst | `INICIAR_SESION` | mod-audit.rst | `VER_AUDITORIA` |
| `A02` | mod-auth.rst | `CERRAR_SESION` | mod-audit.rst | `BUSCAR_AUDITORIA` |
| `A03` | mod-auth.rst | `RECUPERAR_CONTRASENA` | mod-audit.rst | `EXPORTAR_AUDITORIA` |
| `A04` | mod-auth.rst | `CAMBIAR_CONTRASENA` | mod-audit.rst | `REPORTE_COMPLIANCE` |
| `A05` | mod-auth.rst | `GESTIONAR_SESIONES` | — | — |
| `P01` | uc-perm-*.rst | `ASIGNAR_GRUPO` | uc-pip-*.rst | `VER_ESTADO_ETL` |
| `P02` | uc-perm-*.rst | `REVOCAR_GRUPO` | uc-pip-*.rst | `VER_ERRORES_ETL` |
| `P03` | uc-perm-*.rst | `CONCEDER_PERMISO_EXCEPCIONAL` | uc-pip-*.rst | `VER_DISPONIBILIDAD_DATOS` |
| `P04` | uc-perm-*.rst | `REVOCAR_PERMISO_EXCEPCIONAL` | uc-pip-*.rst | `REINTENTAR_ETL` |
| `P05`-`P10` | uc-perm-*.rst | `CREAR_MODIFICAR_AGRUPADOR` etc. | — | — |
| `U01` | uc-usr-*.rst | `CREAR_USUARIO` | uc-rpt-*.rst | `VER_DASHBOARD_IVR` |
| `U02` | uc-usr-*.rst | `CONSULTAR_USUARIOS` | uc-rpt-*.rst | `VER_METRICAS_TIEMPO_REAL` |
| `U03` | uc-usr-*.rst | `MODIFICAR_USUARIO` | uc-rpt-*.rst | `VER_REPORTES_HISTORICOS` |
| `U04` | uc-usr-*.rst | `ELIMINAR_USUARIO` | uc-rpt-*.rst | `EXPORTAR_REPORTE` |
| `UC01`-`UC09` | múltiples módulos | distinto UC por módulo | — | — |

---

## Grupo 4 — Abreviaturas cortas (Tipo 1 y Tipo 3)

```python
ABREV_CORTA = {
    # Servicios de módulo (Tipo 1)
    'AUTH':  'SERVICIO_AUTH',
    'RBAC':  'SERVICIO_RBAC',
    'RPT':   'SERVICIO_REPORTES',
    'ETL':   'SERVICIO_ETL',
    'AUD':   'SERVICIO_AUDITORIA',
    'PERM':  'SERVICIO_PERMISOS',
    'ALR':   'SERVICIO_ALERTAS',
    'PIP':   'SERVICIO_ETL',           # duplicado con ETL — analizar
    'LOG':   'SERVICIO_LOGS',
    'IACT':  'SISTEMA_IACT',

    # Sistemas externos
    'IVR':   'SISTEMA_IVR',            # CONFLICTO: también es BD en algunos diagramas
    'LDAP':  'LDAP_CORPORATIVO',
    'REDIS': 'CACHE_REDIS',
    'WSGI':  'SERVIDOR_WSGI',

    # Bases de datos
    'BDA':   'BD_ANALYTICS',
    'BDO':   'BD_OPERATIVA',
    'IVRDB': 'BD_IVR',
    'ANAL':  'BASE_ANALITICA',
    'HIST':  'HISTORICO_IVR',
    'SESS':  'BASE_SESIONES',
    'AUDIT': 'TABLA_AUDIT_LOG',        # CONFLICTO: también es servicio en algunos diagramas
    'RUNS':  'TABLA_ETL_RUNS',
    'DS1':   'TABLA_ETL_RUNS',
    'DS2':   'BASE_IVR_ANALITICA',
    'DS3':   'TABLA_AUDIT_LOG',
    'DS4':   'TABLA_AUTH_SESSION',

    # Componentes de aplicación
    'APPS':  'MODULOS_DJANGO',
    'DASH':  'DASHBOARD_IVR',
    'RPTS':  'MODULO_REPORTES',
    'ETLS':  'MODULO_ETL',

    # Operaciones/acciones
    'DISP':  'DISPOSICION_LLAMADA',
    'SCHED': 'PROGRAMADOR_ETL',
    'MOTOR': 'MOTOR_ALERTAS',
    'TONE':  'EMISOR_TONO_COMPLIANCE',
    'AUTO':  'EJECUCION_ETL_AUTOMATICA',
    'SUCC':  'ETL_EXITOSO',
    'ABT':   'ETL_ABORTADO',
    'OETL':  'OPERADOR_ETL',

    # Validaciones/actores técnicos
    'AREP':  'REPOSITORIO_AUDITORIA',
    'AUDS':  'AUDITORIA_SELECTIVA',
    'AUDS':  'AUDITORIA_SELECTIVA',
    'CACHE': 'CACHE_PERMISOS',
    'VSOD':  'VALIDAR_SOD',
    'VAGR':  'VALIDAR_AGRUPADOR',
    'VFUN':  'VALIDAR_FUNCIONES',
    'VUSER': 'VALIDAR_USUARIO_DESTINO',
    'BULK':  'VERIFICACION_MASIVA',
    'CALC':  'CALCULO_POST_REVOKE',
    'CALL':  'CERRAR_SESIONES_USUARIO',
    'IDEM':  'FILTRO_IDEMPOTENTE',
    'COMP':  'VALIDAR_COMPLEJIDAD',
    'CONS':  'CONSOLIDAR_METADATA',
    'FINAL': 'CIERRE_SESION',
    'FULL':  'SESION_SCOPE_PLENO',
    'ALERT': 'EVALUADOR_ALERTAS',
    'STATE': 'ESTADO_AGENTE_CACHE',
    'SEG':   'APLICAR_FILTRO_SEGMENTO',
    'MENU':  'VIEW_NAVEGACION_DINAMICA',

    # Acrónimos de roles/actores
    'ADMIN': 'ADMINISTRADOR_SISTEMA',
    'USER':  'USUARIO_AUTENTICADO',
    'USERS': 'REPOSITORIO_USUARIOS',
    'USRD':  'USUARIO_VER_REPORTES',
    'UR':    'REPOSITORIO_USUARIO',
    'UREP':  'REPOSITORIO_USUARIO',

    # Abreviaturas de módulos internos
    'PA':    'MODULO_ACCESO_RBAC',
    'PD':    'MODULO_AUDITORIA',
    'PE':    'MODULO_ETL',             # CONFLICTO: también PermissionsEngine
    'PL':    'MODULO_LLAMADAS_IVR',
    'PN':    'MODULO_ALERTAS',
    'PR':    'MODULO_REPORTES',

    # API/infraestructura
    'REST':  'API_REST_DJANGO',
    'HTTP':  'CLIENTE_HTTP',
    'RBAC':  'SERVICIO_RBAC',
    'EP':    'ENDPOINT_GRUPOS_SISTEMA',
    'VIEW':  'CONSULTA_ALERTAS',

    # Abreviaturas en metodología (si aplica corrección)
    'OOP':   'ORIENTACION_OBJETOS_IACT',
    'CRUD':  'OPERACION_CRUD',
    'DEST':  'BASE_ANALITICA_DESTINO',
    'RPTNN': 'UC_RPT_GENERICO',
    'DB':    'BASE_DATOS',

    # Referencias a UCs cortas
    'UCCRE': 'CREAR_AGRUPADOR',
    'UCMOD': 'MODIFICAR_AGRUPADOR',
    'UCRET': 'RETIRAR_AGRUPADOR',
    'ACRET': 'RETIRAR_AGRUPADOR',
    'AC1':   'ASIGNAR_FUNCIONES_A_USUARIO',
    'AC5':   'GESTIONAR_REGLAS_SOD',
    'AL3':   'RECONOCER_ALERTA',
    'AU1':   'CONSULTAR_AUDITORIA',
    'PE7':   'VERIFICAR_PERMISO',
    'PE8':   'GENERAR_MENU_DINAMICO',
    'R1':    'VER_DASHBOARD_IVR',       # CONFLICTO: también "Solicitar Reporte"
    'R2':    'RESOLVER_SEGMENTO',
    'R4':    'EJECUTAR_PROCEDIMIENTO_RPT',
    'R5':    'RENDERIZAR_REPORTE',
    'P1':    'PASO_AUTENTICACION',      # CONFLICTO: múltiples contextos
    'P2':    'DASHBOARD_IVR',
    'P3':    'CIERRE_SESION',
    'P4':    'GESTION_PIPELINE_ETL',
    'P5':    'CONSULTA_LOGS',
    'P6':    'MODULO_REPORTES',
    'P7':    'BASE_ANALITICA_IVR',
    'P8':    'ALERTAS_NOTIFICACIONES',
    'P9':    'RESOLVER_SEGMENTO',
    'P10':   'AUDITORIA_ACCESO',
    'P11':   'VALIDAR_ANTI_SELF',
    'P08':   'GENERAR_MENU_DINAMICO',
    'P09':   'AUDITAR_ACCESO',
    'S1':    'RECIBIR_SOLICITUD_ETL',
    'S2A':   'SP_RPT_CENTROS_XSEGMENTO',
    'S2B':   'SP_RPT_LLAMADAS_ABANDONADAS',
    'S3':    'VERIFICAR_RESULTADO_ETL',
    'A1':    'INICIAR_SESION',
    'A2':    'CERRAR_SESION',
    'L1':    'CONSULTAR_LOGS',
    'U1':    'CRUD_USUARIOS',
    'R3A':   'VER_REPORTES_HISTORICOS_EXTENSION',
    'R3B':   'VER_REPORTES_HISTORICOS_EXTENSION',
    'R3C':   'VER_REPORTES_HISTORICOS_EXTENSION',
}
```

---

## Grupo 5 — F_ Funciones RBAC (Tipo 4)

Alias de función RBAC: `F_XXX` → nombre completo de la función en SCREAMING_SNAKE_CASE.

```python
F_FUNCIONES = {
    'F_ACA':  'FUNCION_RECONOCER_ALERTA',
    'F_AF':   'FUNCION_ASIGNAR_FUNCIONES',
    'F_AFG':  'FUNCION_ASIGNAR_GRUPOS_FUNCION',
    'F_AIC':  'FUNCION_ATENDER_LLAMADA',
    'F_BIC':  'FUNCION_INTERVENIR_LLAMADA',
    'F_BTM':  'FUNCION_ENVIAR_MENSAJE_EQUIPO',
    'F_CU':   'FUNCION_CREAR_USUARIOS',
    'F_DU':   'FUNCION_DESACTIVAR_USUARIOS',
    'F_EA':   'FUNCION_EXPORTAR_AUDITORIA',
    'F_ECD':  'FUNCION_DISPOSICION_LLAMADA',
    'F_ECSV': 'FUNCION_EXPORTAR_CSV',
    'F_EL':   'FUNCION_EXPORTAR_LOGS',
    'F_EPDF': 'FUNCION_EXPORTAR_PDF',
    'F_EXL':  'FUNCION_EXPORTAR_EXCEL',
    'F_FR':   'FUNCION_FILTRAR_REPORTES',
    'F_GCR':  'FUNCION_GENERAR_REPORTE_COMPLIANCE',
    'F_HC':   'FUNCION_HOLD_LLAMADA',
    'F_LU':   'FUNCION_LISTAR_USUARIOS',
    'F_MAG':  'FUNCION_CREAR_GRUPO_FUNCION',
    'F_MAGC': 'FUNCION_ASIGNAR_FUNCIONES_A_GRUPO',
    'F_MAT':  'FUNCION_CONFIGURAR_ALERTAS_EQUIPO',
    'F_MLC':  'FUNCION_MONITOREAR_LLAMADAS_VIVO',
    'F_MOAS': 'FUNCION_GESTIONAR_ESTADO_AGENTE',
    'F_MOC':  'FUNCION_LLAMADA_OUTBOUND',
    'F_RBK':  'FUNCION_SOLICITAR_BREAK',
    'F_RE':   'FUNCION_REINTENTAR_ETL',
    'F_RF':   'FUNCION_REVOCAR_FUNCIONES',
    'F_RFG':  'FUNCION_REVOCAR_GRUPO_FUNCION',
    'F_ROM':  'FUNCION_LEER_BUZON_PROPIO',
    'F_SA':   'FUNCION_BUSCAR_AUDITORIA',
    'F_SCH':  'FUNCION_PROGRAMAR_REPORTE',
    'F_SESS': 'FUNCION_VER_SESIONES_ACTIVAS',
    'F_SHR':  'FUNCION_COMPARTIR_REPORTE',
    'F_SL':   'FUNCION_BUSCAR_LOGS',
    'F_SV':   'FUNCION_GUARDAR_VISTA',
    'F_TC':   'FUNCION_TRANSFERIR_LLAMADA',
    'F_UU':   'FUNCION_ACTUALIZAR_USUARIOS',
    'F_VA':   'FUNCION_VER_ASIGNACIONES',
    'F_VAA':  'FUNCION_VER_AUDITORIA',
    'F_VAH':  'FUNCION_VER_HISTORIAL_ALERTAS',
    'F_VCH':  'FUNCION_VER_GRAFICOS',
    'F_VD':   'FUNCION_VER_DASHBOARD',
    'F_VDD':  'FUNCION_VER_DISPONIBILIDAD_DATOS',
    'F_VEE':  'FUNCION_VER_ESTADO_ETL',
    'F_VEER': 'FUNCION_VER_ERRORES_ETL',
    'F_VEL':  'FUNCION_VER_LOGS_ETL',
    'F_VGA':  'FUNCION_VER_AUDITORIA',       # duplicado de F_VAA — analizar
    'F_VIL':  'FUNCION_VER_LOGS_INFRAESTRUCTURA',
    'F_VK':   'FUNCION_VER_KPIS',
    'F_VOCH': 'FUNCION_VER_HISTORIAL_LLAMADAS_PROPIAS',
    'F_VON':  'FUNCION_VER_NAVEGACION_PROPIA',
    'F_VOPD': 'FUNCION_VER_DASHBOARD_DESEMPENO',
    'F_VR':   'FUNCION_VER_REPORTES',
    'F_VSL':  'FUNCION_VER_LOGS_APLICACION',
    'F_VSR':  'FUNCION_VER_REGLAS_SOD',
    'F_VSS':  'FUNCION_VER_ESTADO_SISTEMA',
    'F_VTM':  'FUNCION_VER_METRICAS_TECNICAS',
}
```

---

## Grupo 6 — Prefijos técnicos (Tipo 5)

```python
PREFIX_ABBREV = {
    # Artefactos (stored procedures, tablas)
    'ART_R1':    'ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS',
    'ART_R2':    'ARTEFACTO_SP_RPT_TRANSFERENCIAS',
    'ART_R3':    'ARTEFACTO_SP_RPT_MENUS_REDIRIGIDOS',
    'ART_R4':    'ARTEFACTO_SP_RPT_CLIENTES',
    'ART_R5':    'ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO',
    'ART_R6':    'ARTEFACTO_SP_RPT_MENU_CENTRO',
    'ART_R7':    'ARTEFACTO_SP_RPT_MENU_ERROR',
    'ART_E1':    'ARTEFACTO_SP_ETL_MAESTRO',
    'ART_E2':    'ARTEFACTO_ETL_RUNS',
    'ART_L1':    'ARTEFACTO_AUDIT_LOG',
    'ART_A1':    'ARTEFACTO_ACCESS_GROUP',
    'ART_A2':    'ARTEFACTO_ACCESS_FUNCTION',
    'ART_AUDIT': 'ARTEFACTO_AUDIT_LOG',
    'ART_BASE':  'ARTEFACTO_BASE_ANALITICA',
    'ART_HIST':  'ARTEFACTO_HISTORICO_IVR',
    'ART_PAG':   'ARTEFACTO_VISTA_PIPELINE_ADMIN',
    'ART_RVG':   'ARTEFACTO_VISTA_REPORTES',
    'ART_UAG':   'ARTEFACTO_VISTA_ASIGNACION',
    'ART_USERS': 'ARTEFACTO_AUTH_USER',
    'ART_WSGI':  'ARTEFACTO_IACT_WSGI',
    'ART_REQ':   'ARTEFACTO_REPORT_REQUEST',
    'ART_S1':    'ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO',
    'ART_S2':    'ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS',
    'ART_ETLRUNS': 'ARTEFACTO_ETL_RUNS',
    'ART_JWT_PAG': 'ARTEFACTO_JWT_PIPELINE',
    'ART_JWT_RVG': 'ARTEFACTO_JWT_REPORTES',
    'ART_CACHE_RVG': 'ARTEFACTO_CACHE_REPORTES',
    'ETL_SP':    'ARTEFACTO_SP_ETL_MAESTRO',
    'ETL_LOG':   'ARTEFACTO_ETL_LOG',
    'ETL_EXEC':  'ARTEFACTO_ETL_EJECUCION',
    'ETL_SP':    'ARTEFACTO_SP_ETL',
    'RPT_EXEC':  'ARTEFACTO_RPT_EJECUCION',

    # Nodos de infraestructura
    'NODE_APP':   'NODO_SERVIDOR_APLICACION',
    'NODE_DB':    'NODO_BASE_DATOS',
    'NODE_MARIA': 'NODO_MARIADB',
    'NODE_PG':    'NODO_POSTGRESQL',
    'NODE_SRV':   'NODO_SERVIDOR_IACT',
    'NODE_PAG':   'NODO_CLIENTE_PIPELINE',
    'NODE_RVG':   'NODO_CLIENTE_REPORTES',

    # Bases de datos
    'DB_AUTH':   'BASE_DATOS_AUTH',
    'DB_AUDIT':  'BASE_DATOS_AUDIT',
    'DB_ETLR':   'BASE_DATOS_ETL_RUNS',
    'DB_HIST':   'BASE_DATOS_HISTORICO',
    'DB_IVR':    'BASE_DATOS_IVR',
    'DB_MARIA':  'BASE_DATOS_MARIADB',
    'DB_PG':     'BASE_DATOS_POSTGRESQL',
    'DB_USERS':  'BASE_DATOS_USUARIOS',
    'DB_DETALLE':'BASE_DATOS_DETALLE',
    'DB_CLIENTES': 'BASE_DATOS_CLIENTES',

    # Clientes / Browsers
    'BROWSER_PAG': 'NAVEGADOR_WEB',
    'BROWSER_RVG': 'NAVEGADOR_WEB',        # mismo alias, mismo label — unificar
    'BR_PAG': 'NAVEGADOR_CHROME_FIREFOX',
    'BR_RVG': 'NAVEGADOR_CHROME_FIREFOX',
    'BR_UAG': 'NAVEGADOR_CHROME_FIREFOX',

    # CLI clientes
    'CLI_PAG': 'CLIENTE_PIPELINE',
    'CLI_RVG': 'CLIENTE_REPORTES',
    'CLI_UAG': 'CLIENTE_ASIGNACION',

    # Componentes
    'COMP_BACK': 'SISTEMA_BACKEND_IACT',
    'COMP_RVG':  'SISTEMA_VER_REPORTES',

    # Business Rules y otros
    'BR_PAG': 'NAVEGADOR_PIPELINE',
    'BR_RVG': 'NAVEGADOR_REPORTES',
    'BR_UAG': 'NAVEGADOR_ASIGNACION',

    # Schemas
    'SCH_BASE':   'SCHEMA_WEBSITE',
    'SCH_ETL':    'SCHEMA_ETL_CONTROL',
    'SCH_FUENTE': 'SCHEMA_IVR_FUENTE',
    'SCH_PG':     'SCHEMA_IACT_OPERATIONAL',

    # Servicios internos
    'SVC_AUTH':  'SERVICIO_AUTH_PROCESO',
    'SVC_ETL':   'SERVICIO_ETL_DISPARADOR',
    'SVC_OUTER': 'SERVICIO_REPORTES_EXTERNO',
    'SVC_SEG':   'SERVICIO_SEGMENT_RESOLVER',

    # Módulos Django
    'MOD_ADM':  'MODULO_ADMIN',
    'MOD_ETL':  'MODULO_ETL',
    'MOD_LOG':  'MODULO_LOGS',
    'MOD_RPT':  'MODULO_REPORTES',

    # ETL aliases
    'ETLV':  'VISTA_ETL',
    'ETLR':  'REPOSITORIO_ETL',
    'ETLORM':'ORM_ETL',
    'ETLF':  'FACADE_ETL',
    'ETLE':  'ENTIDAD_ETL',
    'ETL_SP':'SP_ETL_MAESTRO',

    # Misceláneos
    'OS_LINUX':    'SISTEMA_OPERATIVO_LINUX',
    'WEB_SERVER':  'SERVIDOR_WEB',
    'DRF_API':     'API_DJANGO_REST',
    'IACT_SVC':    'SERVICIO_IACT',
    'NODE_SRV':    'NODO_SERVIDOR',
    'RBAC_MIDDLEWARE': 'MIDDLEWARE_RBAC',   # ya CLEAN, confirmado
    'S_RPT':  'SUBSISTEMA_REPORTES',
    'S_RBAC': 'SUBSISTEMA_RBAC',
    'S_LOG':  'SUBSISTEMA_LOGS',
    'S_ETL':  'SUBSISTEMA_ETL',
    'S_DASH': 'SUBSISTEMA_DASHBOARD',
    'UC_RPT': 'CLUSTER_REPORTES',
    'UC_RBAC':'CLUSTER_RBAC',
}
```

---

## Grupo 7 — UC_PREFIX (Tipo 1/2)

```python
UC_PREFIX = {
    'UC_AUTH':    'CLUSTER_AUTH',
    'UC_RBAC':    'CLUSTER_RBAC',
    'UC_RPT':     'CLUSTER_REPORTES',
    'UC_ACC':     'CLUSTER_ACCESO',
    'UC_LOG':     'CLUSTER_LOGS',
    'UC_DASH':    'VER_DASHBOARD_IVR',
    'UC_DISP':    'VER_DISPONIBILIDAD_DATOS',
    'UC_INC':     'RESOLVER_SEGMENTO',
    'UC_LOGOUT':  'CERRAR_SESION',
    'UC_PIP':     'CLUSTER_ETL',
    'UC_R13':     'VER_LLAMADAS_ABANDONADAS',
    'UC_R15':     'VER_TRANSFERENCIAS',
    'UC_R16':     'VER_MENUS_IVR',
    'UC_R17':     'VER_CLIENTES_UNICOS',
    'UC_RPT_04':  'EXPORTAR_REPORTE',
}
```

---

## Conflictos identificados — requieren resolución por archivo

Igual que `ORD`/`WH` en el diccionario de referencia, estos aliases tienen
semántica distinta según el archivo donde aparecen:

1. `IVR` → `SISTEMA_IVR` en diagramas de contexto / `BD_IVR` en diagramas de datos
2. `AUDIT` / `AUD` → `SERVICIO_AUDITORIA` en secuencias / `TABLA_AUDIT_LOG` en deployment
3. `PE` → `MODULO_ETL` en módulos / `MOTOR_PERMISOS` en servicios
4. `BROWSER_PAG` / `BROWSER_RVG` → mismo label, mismo significado — se puede unificar a `NAVEGADOR_WEB`
5. `A01..A05` → AUTH en mod-auth / AUD en mod-audit
6. `U01..U14` → USR en uc-usr / RPT en uc-rpt
7. `UC01..UC09` → distintos módulos usan el mismo alias para su propio UC

## Estadísticas del diccionario

| Grupo | Aliases | Estado |
|-------|---------|--------|
| SINGLE_LETTER | 8 | ✓ Completo |
| UC sin conflicto | ~80 | ✓ Completo |
| UC con conflicto | ~20 | Requiere por-archivo |
| ABREV_CORTA | 76 | ✓ Completo |
| F_FUNCIONES | 57 | ✓ Completo |
| PREFIX_ABBREV | 60 | ✓ Completo |
| UC_PREFIX | 15 | ✓ Completo |
| **Total** | **316+** | 7 conflictos requieren per-archivo |
