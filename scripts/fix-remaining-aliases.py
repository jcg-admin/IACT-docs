#!/usr/bin/env python3
"""
Fix F_FUNCIONES, PREFIX_ABBREV and UC_PREFIX aliases in PlantUML blocks.
Same safe strategy as fix-abrev-corta.py:
  Only replace aliases explicitly declared with 'as ALIAS' in the block.
"""

import re
import sys
import glob
import os

F_FUNCIONES = {
    'F_ACA': 'FUNCION_RECONOCER_ALERTA', 'F_AF': 'FUNCION_ASIGNAR_FUNCIONES',
    'F_AFG': 'FUNCION_ASIGNAR_GRUPOS_FUNCION', 'F_AIC': 'FUNCION_ATENDER_LLAMADA',
    'F_BIC': 'FUNCION_INTERVENIR_LLAMADA', 'F_BTM': 'FUNCION_ENVIAR_MENSAJE_EQUIPO',
    'F_CU': 'FUNCION_CREAR_USUARIOS', 'F_DU': 'FUNCION_DESACTIVAR_USUARIOS',
    'F_EA': 'FUNCION_EXPORTAR_AUDITORIA', 'F_ECD': 'FUNCION_DISPOSICION_LLAMADA',
    'F_ECSV': 'FUNCION_EXPORTAR_CSV', 'F_EL': 'FUNCION_EXPORTAR_LOGS',
    'F_EPDF': 'FUNCION_EXPORTAR_PDF', 'F_EXL': 'FUNCION_EXPORTAR_EXCEL',
    'F_FR': 'FUNCION_FILTRAR_REPORTES', 'F_GCR': 'FUNCION_GENERAR_REPORTE_COMPLIANCE',
    'F_HC': 'FUNCION_HOLD_LLAMADA', 'F_LU': 'FUNCION_LISTAR_USUARIOS',
    'F_MAG': 'FUNCION_CREAR_GRUPO_FUNCION', 'F_MAGC': 'FUNCION_ASIGNAR_FUNCIONES_A_GRUPO',
    'F_MAT': 'FUNCION_CONFIGURAR_ALERTAS_EQUIPO', 'F_MLC': 'FUNCION_MONITOREAR_LLAMADAS_VIVO',
    'F_MOAS': 'FUNCION_GESTIONAR_ESTADO_AGENTE', 'F_MOC': 'FUNCION_LLAMADA_OUTBOUND',
    'F_RBK': 'FUNCION_SOLICITAR_BREAK', 'F_RE': 'FUNCION_REINTENTAR_ETL',
    'F_RF': 'FUNCION_REVOCAR_FUNCIONES', 'F_RFG': 'FUNCION_REVOCAR_GRUPO_FUNCION',
    'F_ROM': 'FUNCION_LEER_BUZON_PROPIO', 'F_SA': 'FUNCION_BUSCAR_AUDITORIA',
    'F_SCH': 'FUNCION_PROGRAMAR_REPORTE', 'F_SESS': 'FUNCION_VER_SESIONES_ACTIVAS',
    'F_SHR': 'FUNCION_COMPARTIR_REPORTE', 'F_SL': 'FUNCION_BUSCAR_LOGS',
    'F_SV': 'FUNCION_GUARDAR_VISTA', 'F_TC': 'FUNCION_TRANSFERIR_LLAMADA',
    'F_UU': 'FUNCION_ACTUALIZAR_USUARIOS', 'F_VA': 'FUNCION_VER_ASIGNACIONES',
    'F_VAA': 'FUNCION_VER_AUDITORIA', 'F_VAH': 'FUNCION_VER_HISTORIAL_ALERTAS',
    'F_VCH': 'FUNCION_VER_GRAFICOS', 'F_VD': 'FUNCION_VER_DASHBOARD',
    'F_VDD': 'FUNCION_VER_DISPONIBILIDAD_DATOS', 'F_VEE': 'FUNCION_VER_ESTADO_ETL',
    'F_VEER': 'FUNCION_VER_ERRORES_ETL', 'F_VEL': 'FUNCION_VER_LOGS_ETL',
    'F_VGA': 'FUNCION_VER_AUDITORIA', 'F_VIL': 'FUNCION_VER_LOGS_INFRAESTRUCTURA',
    'F_VK': 'FUNCION_VER_KPIS', 'F_VOCH': 'FUNCION_VER_HISTORIAL_LLAMADAS_PROPIAS',
    'F_VON': 'FUNCION_VER_NAVEGACION_PROPIA', 'F_VOPD': 'FUNCION_VER_DASHBOARD_DESEMPENO',
    'F_VR': 'FUNCION_VER_REPORTES', 'F_VSL': 'FUNCION_VER_LOGS_APLICACION',
    'F_VSR': 'FUNCION_VER_REGLAS_SOD', 'F_VSS': 'FUNCION_VER_ESTADO_SISTEMA',
    'F_VTM': 'FUNCION_VER_METRICAS_TECNICAS',
}

PREFIX_ABBREV = {
    'ART_R1': 'ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS',
    'ART_R2': 'ARTEFACTO_SP_RPT_TRANSFERENCIAS',
    'ART_R3': 'ARTEFACTO_SP_RPT_MENUS_REDIRIGIDOS',
    'ART_R4': 'ARTEFACTO_SP_RPT_CLIENTES',
    'ART_R5': 'ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO',
    'ART_R6': 'ARTEFACTO_SP_RPT_MENU_CENTRO',
    'ART_R7': 'ARTEFACTO_SP_RPT_MENU_ERROR',
    'ART_E1': 'ARTEFACTO_SP_ETL_MAESTRO',
    'ART_E2': 'ARTEFACTO_ETL_RUNS',
    'ART_L1': 'ARTEFACTO_AUDIT_LOG',
    'ART_A1': 'ARTEFACTO_ACCESS_GROUP',
    'ART_A2': 'ARTEFACTO_ACCESS_FUNCTION',
    'ART_AUDIT': 'ARTEFACTO_AUDIT_LOG',
    'ART_BASE': 'ARTEFACTO_BASE_ANALITICA',
    'ART_HIST': 'ARTEFACTO_HISTORICO_IVR',
    'ART_PAG': 'ARTEFACTO_VISTA_PIPELINE_ADMIN',
    'ART_RVG': 'ARTEFACTO_VISTA_REPORTES',
    'ART_UAG': 'ARTEFACTO_VISTA_ASIGNACION',
    'ART_USERS': 'ARTEFACTO_AUTH_USER',
    'ART_WSGI': 'ARTEFACTO_IACT_WSGI',
    'ART_REQ': 'ARTEFACTO_REPORT_REQUEST',
    'ART_S1': 'ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO',
    'ART_S2': 'ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS',
    'ART_ETLRUNS': 'ARTEFACTO_ETL_RUNS',
    'ART_JWT_PAG': 'ARTEFACTO_JWT_PIPELINE',
    'ART_JWT_RVG': 'ARTEFACTO_JWT_REPORTES',
    'ART_CACHE_RVG': 'ARTEFACTO_CACHE_REPORTES',
    'ETL_SP': 'ARTEFACTO_SP_ETL',
    'ETL_LOG': 'ARTEFACTO_ETL_LOG',
    'ETL_EXEC': 'ARTEFACTO_ETL_EJECUCION',
    'RPT_EXEC': 'ARTEFACTO_RPT_EJECUCION',
    'NODE_APP': 'NODO_SERVIDOR_APLICACION',
    'NODE_DB': 'NODO_BASE_DATOS',
    'NODE_MARIA': 'NODO_MARIADB',
    'NODE_PG': 'NODO_POSTGRESQL',
    'NODE_SRV': 'NODO_SERVIDOR_IACT',
    'NODE_PAG': 'NODO_CLIENTE_PIPELINE',
    'NODE_RVG': 'NODO_CLIENTE_REPORTES',
    'DB_AUTH': 'BASE_DATOS_AUTH',
    'DB_AUDIT': 'BASE_DATOS_AUDIT',
    'DB_ETLR': 'BASE_DATOS_ETL_RUNS',
    'DB_HIST': 'BASE_DATOS_HISTORICO',
    'DB_IVR': 'BASE_DATOS_IVR',
    'DB_MARIA': 'BASE_DATOS_MARIADB',
    'DB_PG': 'BASE_DATOS_POSTGRESQL',
    'DB_USERS': 'BASE_DATOS_USUARIOS',
    'DB_DETALLE': 'BASE_DATOS_DETALLE',
    'DB_CLIENTES': 'BASE_DATOS_CLIENTES',
    'BROWSER_PAG': 'NAVEGADOR_WEB',
    'BROWSER_RVG': 'NAVEGADOR_WEB',
    'BR_PAG': 'NAVEGADOR_PIPELINE',
    'BR_RVG': 'NAVEGADOR_REPORTES',
    'BR_UAG': 'NAVEGADOR_ASIGNACION',
    'CLI_PAG': 'CLIENTE_PIPELINE',
    'CLI_RVG': 'CLIENTE_REPORTES',
    'CLI_UAG': 'CLIENTE_ASIGNACION',
    'COMP_BACK': 'SISTEMA_BACKEND_IACT',
    'COMP_RVG': 'SISTEMA_VER_REPORTES',
    'SCH_BASE': 'SCHEMA_WEBSITE',
    'SCH_ETL': 'SCHEMA_ETL_CONTROL',
    'SCH_FUENTE': 'SCHEMA_IVR_FUENTE',
    'SCH_PG': 'SCHEMA_IACT_OPERATIONAL',
    'SVC_AUTH': 'SERVICIO_AUTH_PROCESO',
    'SVC_ETL': 'SERVICIO_ETL_DISPARADOR',
    'SVC_OUTER': 'SERVICIO_REPORTES_EXTERNO',
    'SVC_SEG': 'SERVICIO_SEGMENT_RESOLVER',
    'MOD_ADM': 'MODULO_ADMIN',
    'MOD_ETL': 'MODULO_ETL',
    'MOD_LOG': 'MODULO_LOGS',
    'MOD_RPT': 'MODULO_REPORTES',
    'ETLV': 'VISTA_ETL',
}

UC_PREFIX = {
    'UC_AUTH': 'CLUSTER_AUTH', 'UC_RBAC': 'CLUSTER_RBAC',
    'UC_RPT': 'CLUSTER_REPORTES', 'UC_ACC': 'CLUSTER_ACCESO',
    'UC_LOG': 'CLUSTER_LOGS', 'UC_DASH': 'VER_DASHBOARD_IVR',
    'UC_DISP': 'VER_DISPONIBILIDAD_DATOS', 'UC_INC': 'RESOLVER_SEGMENTO',
    'UC_LOGOUT': 'CERRAR_SESION', 'UC_PIP': 'CLUSTER_ETL',
    'UC_R13': 'VER_LLAMADAS_ABANDONADAS', 'UC_R15': 'VER_TRANSFERENCIAS',
    'UC_R16': 'VER_MENUS_IVR', 'UC_R17': 'VER_CLIENTES_UNICOS',
    'UC_RPT_04': 'EXPORTAR_REPORTE',
}

# Merge all groups
ALL_ALIASES = {}
ALL_ALIASES.update(F_FUNCIONES)
ALL_ALIASES.update(PREFIX_ABBREV)
ALL_ALIASES.update(UC_PREFIX)

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')


def replace_in_text_outside_strings(text, alias, new_alias):
    pat = re.compile(rf'(?<![A-Za-z0-9_]){re.escape(alias)}(?![A-Za-z0-9_])')
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.lstrip().startswith("'"):
            result.append(line)
            continue
        parts = STRING_RE.split(line)
        strings = STRING_RE.findall(line)
        new_parts = []
        for i, part in enumerate(parts):
            new_parts.append(pat.sub(new_alias, part))
            if i < len(strings):
                new_parts.append(strings[i])
        result.append(''.join(new_parts))
    return '\n'.join(result)


def process_block(block_text):
    declared = {}
    for alias, new_alias in ALL_ALIASES.items():
        if re.search(rf'\bas\s+{re.escape(alias)}\b', block_text):
            declared[alias] = new_alias
    if not declared:
        return block_text, []
    result = block_text
    applied = []
    for alias, new_alias in declared.items():
        new_result = replace_in_text_outside_strings(result, alias, new_alias)
        if new_result != result:
            applied.append(f'{alias}→{new_alias}')
        result = new_result
    return result, applied


BLOCK_RE = re.compile(r'(@startuml.*?@enduml)', re.DOTALL)


def fix_file(fpath, dry_run=False):
    try:
        content = open(fpath).read()
    except Exception as e:
        return False, f"read error: {e}"
    changed = False
    all_applied = []

    def replace_block(m):
        nonlocal changed
        new_block, applied = process_block(m.group(1))
        if new_block != m.group(1):
            changed = True
            all_applied.extend(applied)
        return new_block

    new_content = BLOCK_RE.sub(replace_block, content)
    if changed and not dry_run:
        try:
            open(fpath, 'w').write(new_content)
        except Exception as e:
            return False, f"write error: {e}"
    return changed, all_applied


def main():
    dry_run = '--dry-run' in sys.argv
    rst_files = sorted(glob.glob('source/**/*.rst', recursive=True))
    fixed = []
    errors = []
    for fpath in rst_files:
        changed, info = fix_file(fpath, dry_run=dry_run)
        if isinstance(info, str):
            errors.append((fpath, info))
            print(f"[ERR] {os.path.relpath(fpath)}: {info}")
        elif changed:
            rel = os.path.relpath(fpath)
            aliases_str = ', '.join(info) if isinstance(info, list) else ''
            print(f"{'[DRY]' if dry_run else '[FIX]'} {rel}  [{aliases_str}]")
            fixed.append(fpath)
    print(f"\n{'DRY RUN — ' if dry_run else ''}Fixed: {len(fixed)} files, Errors: {len(errors)}")
    return len(errors)


if __name__ == '__main__':
    sys.exit(main())
