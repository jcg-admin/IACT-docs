#!/usr/bin/env python3
"""
Fix ABREV_CORTA aliases in PlantUML blocks.

Strategy (safe):
  1. For each @startuml...@enduml block, find aliases EXPLICITLY DECLARED
     with "as ALIAS" syntax.
  2. For declared aliases only, replace ALL word-boundary occurrences in that
     block — EXCEPT inside double-quoted strings and single-quote comment lines.
  3. Aliases NOT declared with "as" in the block are left untouched (avoids
     changing acronyms used as display labels like 'package "RBAC" {}').
"""

import re
import sys
import glob
import os

ABREV_CORTA = {
    'AUTH': 'SERVICIO_AUTH', 'RBAC': 'SERVICIO_RBAC', 'RPT': 'SERVICIO_REPORTES',
    'ETL': 'SERVICIO_ETL', 'AUD': 'SERVICIO_AUDITORIA', 'PERM': 'SERVICIO_PERMISOS',
    'ALR': 'SERVICIO_ALERTAS', 'PIP': 'SERVICIO_ETL', 'LOG': 'SERVICIO_LOGS',
    'IACT': 'SISTEMA_IACT', 'IVR': 'SISTEMA_IVR', 'LDAP': 'LDAP_CORPORATIVO',
    'REDIS': 'CACHE_REDIS', 'WSGI': 'SERVIDOR_WSGI', 'BDA': 'BD_ANALYTICS',
    'BDO': 'BD_OPERATIVA', 'IVRDB': 'BD_IVR', 'ANAL': 'BASE_ANALITICA',
    'HIST': 'HISTORICO_IVR', 'SESS': 'BASE_SESIONES', 'AUDIT': 'TABLA_AUDIT_LOG',
    'RUNS': 'TABLA_ETL_RUNS', 'DS1': 'TABLA_ETL_RUNS', 'DS2': 'BASE_IVR_ANALITICA',
    'DS3': 'TABLA_AUDIT_LOG', 'DS4': 'TABLA_AUTH_SESSION', 'APPS': 'MODULOS_DJANGO',
    'DASH': 'DASHBOARD_IVR', 'RPTS': 'MODULO_REPORTES', 'ETLS': 'MODULO_ETL',
    'DISP': 'DISPOSICION_LLAMADA', 'SCHED': 'PROGRAMADOR_ETL', 'MOTOR': 'MOTOR_ALERTAS',
    'TONE': 'EMISOR_TONO_COMPLIANCE', 'AUTO': 'EJECUCION_ETL_AUTOMATICA',
    'SUCC': 'ETL_EXITOSO', 'ABT': 'ETL_ABORTADO', 'OETL': 'OPERADOR_ETL',
    'AREP': 'REPOSITORIO_AUDITORIA', 'AUDS': 'AUDITORIA_SELECTIVA',
    'CACHE': 'CACHE_PERMISOS', 'VSOD': 'VALIDAR_SOD', 'VAGR': 'VALIDAR_AGRUPADOR',
    'VFUN': 'VALIDAR_FUNCIONES', 'VUSER': 'VALIDAR_USUARIO_DESTINO',
    'BULK': 'VERIFICACION_MASIVA', 'CALC': 'CALCULO_POST_REVOKE',
    'CALL': 'CERRAR_SESIONES_USUARIO', 'IDEM': 'FILTRO_IDEMPOTENTE',
    'COMP': 'VALIDAR_COMPLEJIDAD', 'CONS': 'CONSOLIDAR_METADATA',
    'FINAL': 'CIERRE_SESION', 'FULL': 'SESION_SCOPE_PLENO',
    'ALERT': 'EVALUADOR_ALERTAS', 'STATE': 'ESTADO_AGENTE_CACHE',
    'SEG': 'APLICAR_FILTRO_SEGMENTO', 'MENU': 'VIEW_NAVEGACION_DINAMICA',
    'ADMIN': 'ADMINISTRADOR_SISTEMA', 'USER': 'USUARIO_AUTENTICADO',
    'USERS': 'REPOSITORIO_USUARIOS', 'USRD': 'USUARIO_VER_REPORTES',
    'UR': 'REPOSITORIO_USUARIO', 'UREP': 'REPOSITORIO_USUARIO',
    'PA': 'MODULO_ACCESO_RBAC', 'PD': 'MODULO_AUDITORIA', 'PE': 'MODULO_ETL',
    'PL': 'MODULO_LLAMADAS_IVR', 'PN': 'MODULO_ALERTAS', 'PR': 'MODULO_REPORTES',
    'REST': 'API_REST_DJANGO', 'HTTP': 'CLIENTE_HTTP',
    'EP': 'ENDPOINT_GRUPOS_SISTEMA', 'VIEW': 'CONSULTA_ALERTAS',
    'OOP': 'ORIENTACION_OBJETOS_IACT', 'CRUD': 'OPERACION_CRUD',
    'DEST': 'BASE_ANALITICA_DESTINO', 'RPTNN': 'UC_RPT_GENERICO', 'DB': 'BASE_DATOS',
    'UCCRE': 'CREAR_AGRUPADOR', 'UCMOD': 'MODIFICAR_AGRUPADOR',
    'UCRET': 'RETIRAR_AGRUPADOR', 'ACRET': 'RETIRAR_AGRUPADOR',
    'AC1': 'ASIGNAR_FUNCIONES_A_USUARIO', 'AC5': 'GESTIONAR_REGLAS_SOD',
    'AL3': 'RECONOCER_ALERTA', 'AU1': 'CONSULTAR_AUDITORIA',
    'PE7': 'VERIFICAR_PERMISO', 'PE8': 'GENERAR_MENU_DINAMICO',
    'R1': 'VER_DASHBOARD_IVR', 'R2': 'RESOLVER_SEGMENTO',
    'R4': 'EJECUTAR_PROCEDIMIENTO_RPT', 'R5': 'RENDERIZAR_REPORTE',
    'P1': 'PASO_AUTENTICACION', 'P2': 'DASHBOARD_IVR', 'P3': 'CIERRE_SESION',
    'P4': 'GESTION_PIPELINE_ETL', 'P5': 'CONSULTA_LOGS', 'P6': 'MODULO_REPORTES',
    'P7': 'BASE_ANALITICA_IVR', 'P8': 'ALERTAS_NOTIFICACIONES',
    'P9': 'RESOLVER_SEGMENTO', 'P10': 'AUDITORIA_ACCESO',
    'P11': 'VALIDAR_ANTI_SELF', 'P08': 'GENERAR_MENU_DINAMICO',
    'P09': 'AUDITAR_ACCESO', 'S1': 'RECIBIR_SOLICITUD_ETL',
    'S2A': 'SP_RPT_CENTROS_XSEGMENTO', 'S2B': 'SP_RPT_LLAMADAS_ABANDONADAS',
    'S3': 'VERIFICAR_RESULTADO_ETL', 'A1': 'INICIAR_SESION', 'A2': 'CERRAR_SESION',
    'L1': 'CONSULTAR_LOGS', 'U1': 'CRUD_USUARIOS',
    'R3A': 'VER_REPORTES_HISTORICOS_EXTENSION', 'R3B': 'VER_REPORTES_HISTORICOS_EXTENSION',
    'R3C': 'VER_REPORTES_HISTORICOS_EXTENSION',
}

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')


def replace_in_text_outside_strings(text, alias, new_alias):
    """
    Replace word-boundary occurrences of alias in text, skipping
    double-quoted string contents and single-quote comment lines.
    """
    pat = re.compile(rf'(?<![A-Za-z0-9_]){re.escape(alias)}(?![A-Za-z0-9_])')
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.lstrip()
        # Skip PlantUML single-quote comment lines entirely
        if stripped.startswith("'"):
            result.append(line)
            continue
        # Split on string literals; replace only outside strings
        parts = STRING_RE.split(line)
        strings = STRING_RE.findall(line)
        # Interleave: parts[0], strings[0], parts[1], strings[1], ...
        new_line_parts = []
        for i, part in enumerate(parts):
            new_line_parts.append(pat.sub(new_alias, part))
            if i < len(strings):
                new_line_parts.append(strings[i])  # keep string unchanged
        result.append(''.join(new_line_parts))
    return '\n'.join(result)


def process_block(block_text):
    """
    Find explicitly declared aliases in this block (via 'as ALIAS' syntax),
    then replace all identifier usages of those aliases.
    """
    declared = {}
    for alias, new_alias in ABREV_CORTA.items():
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
    """Process a single RST file."""
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
        if isinstance(info, str):  # error
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
