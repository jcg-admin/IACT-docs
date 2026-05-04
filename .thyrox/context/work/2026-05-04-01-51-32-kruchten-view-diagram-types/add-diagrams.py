#!/usr/bin/env python3
"""
Add missing diagrams and fix participant/node names to semantic roles.

Arquitectura IACT canonica:
  Vagrant VM / Ubuntu
  Apache + mod_wsgi  (NO nginx, NO gunicorn)
  Django Application
  MariaDB (NO MySQL alias en nuevos diagramas)
  Redis Cache

Regla: diagramas de secuencia y comunicacion usan ROLES semanticos.
       diagramas de despliegue usan nombres de producto reales.
"""
import os
import re

BASE = "/home/user/IACT-docs/source/arquitectura-tecnica"

# Semantic role labels per module for sequence/communication diagrams
MODULE_ROLES = {
    "auth":    ("Interfaz de Acceso",       "Servicio de Autenticacion"),
    "usr":     ("Interfaz de Usuarios",     "Servicio de Usuarios"),
    "acc":     ("Interfaz de Control",      "Servicio de Acceso"),
    "perm":    ("Interfaz de Permisos",     "Servicio de Permisos"),
    "rpt":     ("Interfaz de Reportes",     "Servicio de Reportes"),
    "alr":     ("Interfaz de Alertas",      "Servicio de Alertas"),
    "pip":     ("Interfaz de Pipeline",     "Servicio de Pipeline"),
    "aud":     ("Interfaz de Auditoria",    "Servicio de Auditoria"),
    "log":     ("Interfaz de Logs",         "Servicio de Logs"),
    "opr":     ("Interfaz de Operador",     "Servicio de Operador"),
    "sup":     ("Interfaz de Supervision",  "Servicio de Supervision"),
    "cli":     ("Interfaz de Llamadas",     "Servicio de Llamadas"),
    "inc-rpt": ("Interfaz de Reportes",     "Servicio de Reportes"),
}

# State machine patterns per module
STATE_MACHINES = {
    "auth": {
        "entity": "Session",
        "states": [
            ("[*]",        "Iniciada",    "usuario solicita login"),
            ("Iniciada",   "Validando",   "enviar credenciales"),
            ("Validando",  "Activa",      "autenticacion exitosa"),
            ("Activa",     "Cerrada",     "logout / timeout"),
            ("Validando",  "[*]",         "credenciales invalidas"),
        ],
    },
    "usr": {
        "entity": "User",
        "states": [
            ("[*]",        "Creado",      "crear usuario"),
            ("Creado",     "Activo",      "activar cuenta"),
            ("Activo",     "Suspendido",  "suspender"),
            ("Suspendido", "Activo",      "reactivar"),
            ("Activo",     "Desactivado", "dar de baja"),
            ("Desactivado","[*]",         "eliminar definitivo"),
        ],
    },
    "acc": {
        "entity": "FuncionAsignada",
        "states": [
            ("[*]",      "Pendiente", "solicitar asignacion"),
            ("Pendiente","Asignada",  "aprobar asignacion"),
            ("Asignada", "Activa",    "activar"),
            ("Activa",   "Revocada",  "revocar funcion"),
            ("Pendiente","[*]",       "rechazar solicitud"),
            ("Revocada", "[*]",       "eliminar registro"),
        ],
    },
    "perm": {
        "entity": "Permiso",
        "states": [
            ("[*]",        "Solicitado", "crear solicitud"),
            ("Solicitado", "EnRevision", "iniciar revision"),
            ("EnRevision", "Aprobado",   "aprobar"),
            ("EnRevision", "Denegado",   "denegar"),
            ("Aprobado",   "Activo",     "activar permiso"),
            ("Activo",     "Revocado",   "revocar"),
            ("Denegado",   "[*]",        "cerrar solicitud"),
            ("Revocado",   "[*]",        "archivar"),
        ],
    },
    "rpt": {
        "entity": "Reporte",
        "states": [
            ("[*]",        "Solicitado", "solicitar reporte"),
            ("Solicitado", "Generando",  "iniciar generacion"),
            ("Generando",  "Listo",      "generacion exitosa"),
            ("Listo",      "Entregado",  "descargar / visualizar"),
            ("Entregado",  "Archivado",  "archivar"),
            ("Generando",  "Error",      "fallo en generacion"),
            ("Error",      "[*]",        "descartar"),
            ("Archivado",  "[*]",        "purgar"),
        ],
    },
    "inc-rpt": {
        "entity": "Reporte",
        "states": [
            ("[*]",        "Solicitado", "solicitar reporte"),
            ("Solicitado", "Generando",  "iniciar generacion"),
            ("Generando",  "Listo",      "generacion exitosa"),
            ("Listo",      "Entregado",  "descargar / visualizar"),
            ("Entregado",  "Archivado",  "archivar"),
            ("Generando",  "Error",      "fallo en generacion"),
            ("Error",      "[*]",        "descartar"),
            ("Archivado",  "[*]",        "purgar"),
        ],
    },
    "alr": {
        "entity": "Alerta",
        "states": [
            ("[*]",       "Disparada",  "condicion detectada"),
            ("Disparada", "Activa",     "notificar usuario"),
            ("Activa",    "Reconocida", "usuario reconoce"),
            ("Reconocida","Resuelta",   "resolver causa"),
            ("Resuelta",  "[*]",        "cerrar alerta"),
            ("Activa",    "Escalada",   "timeout sin reconocer"),
            ("Escalada",  "Reconocida", "reconocer escalada"),
        ],
    },
    "pip": {
        "entity": "ETLRun",
        "states": [
            ("[*]",       "Programado", "agendar ejecucion"),
            ("Programado","Ejecutando", "sp_etl_maestro inicia"),
            ("Ejecutando","Completado", "todas las etapas OK"),
            ("Ejecutando","Fallido",    "error en etapa"),
            ("Completado","[*]",        "registrar en etl_runs"),
            ("Fallido",   "Reintento",  "politica de reintento"),
            ("Reintento", "Ejecutando", "reintentar"),
            ("Reintento", "[*]",        "agotar reintentos"),
        ],
    },
    "aud": {
        "entity": "RegistroAuditoria",
        "states": [
            ("[*]",        "Capturado",   "evento de negocio ocurre"),
            ("Capturado",  "Indexado",    "almacenar en BD"),
            ("Indexado",   "Consultable", "indice disponible"),
            ("Consultable","Archivado",   "politica de retencion"),
            ("Archivado",  "[*]",         "purgar segun CNST"),
        ],
    },
    "log": {
        "entity": "EntradaLog",
        "states": [
            ("[*]",        "Generado",    "evento tecnico ocurre"),
            ("Generado",   "Almacenado",  "escribir en log"),
            ("Almacenado", "Consultable", "indice disponible"),
            ("Consultable","Archivado",   "rotacion de logs"),
            ("Archivado",  "[*]",         "purgar segun retencion"),
        ],
    },
    "opr": {
        "entity": "AccionOperador",
        "states": [
            ("[*]",       "Iniciada",   "operador ejecuta accion"),
            ("Iniciada",  "Procesando", "sistema valida RBAC"),
            ("Procesando","Completada", "accion exitosa"),
            ("Procesando","Fallida",    "error / sin permiso"),
            ("Completada","[*]",        "registrar en auditoria"),
            ("Fallida",   "[*]",        "registrar error"),
        ],
    },
    "sup": {
        "entity": "SesionSupervision",
        "states": [
            ("[*]",          "Abierta",      "supervisor ingresa"),
            ("Abierta",      "Monitoreando", "ver metricas activas"),
            ("Monitoreando", "Interviniendo","accion correctiva"),
            ("Interviniendo","Monitoreando", "accion completada"),
            ("Monitoreando", "Cerrada",      "supervisor sale"),
            ("Cerrada",      "[*]",          "registrar sesion"),
        ],
    },
    "cli": {
        "entity": "SesionLlamada",
        "states": [
            ("[*]",      "Iniciada",   "llamada entrante"),
            ("Iniciada", "EnIVR",      "conectar IVR"),
            ("EnIVR",    "Atendida",   "agente disponible"),
            ("EnIVR",    "Abandonada", "cliente cuelga"),
            ("Atendida", "Completada", "finalizar atencion"),
            ("Completada","[*]",       "registrar CDR"),
            ("Abandonada","[*]",       "registrar abandono"),
        ],
    },
}

# Canonical deployment diagram per module
# Uses real product names (Apache, MariaDB, Redis) — these ARE physical nodes
DEPLOY_WITH_CACHE = {"auth"}   # modules that need Redis cache node

def deploy_diagram(uc_title, module):
    with_cache = module in DEPLOY_WITH_CACHE
    lines = [
        "",
        ".. uml::",
        f" :caption: {uc_title} — Deployment View",
        "",
        " @startuml",
        "",
        ' node "Cliente Web" as Client',
        ' node "Apache + mod_wsgi" as WebServer {',
        '   artifact "Django App" as App',
        ' }',
    ]
    if module == "pip":
        lines[-2] = '   artifact "DisparadorETL" as App'
    lines.append(' database "MariaDB" as DB')
    if with_cache:
        lines.append(' node "Redis" as Cache')
    lines += ["", " Client --> WebServer : HTTPS"]
    if module == "pip":
        lines.append(" WebServer --> DB : SP call / TCP")
    else:
        lines.append(" WebServer --> DB : TCP / SQL")
    if with_cache:
        lines.append(" WebServer --> Cache : TCP / Redis")
    lines += ["", " @enduml", ""]
    return "\n".join(lines)


def get_module(filename):
    if filename == "inc-rpt-01.rst":
        return "inc-rpt"
    m = re.match(r"^([a-z]+(?:-[a-z]+)?)-\d+\.rst$", filename)
    return m.group(1) if m else None


def get_uc_title(content):
    m = re.search(r"^={10,}\n(.+)\n={10,}", content, re.MULTILINE)
    if m:
        title = m.group(1).strip()
        title = re.sub(
            r": (Domain Model|Design View|Process View|Deployment View"
            r"|Implementation View|Use Case View)$",
            "", title)
        return title
    return "UC"


def state_machine_section(uc_title, module):
    sm = STATE_MACHINES.get(module)
    if not sm:
        return None
    entity = sm["entity"]
    lines = [
        "",
        ".. uml::",
        f" :caption: {uc_title} — Estado de {entity}",
        "",
        " @startuml",
        " hide empty description",
        "",
    ]
    for src, dst, label in sm["states"]:
        lines.append(f" {src} --> {dst} : {label}")
    lines += ["", " @enduml", ""]
    return "\n".join(lines)


def communication_section(uc_title, actor, module):
    iface, svc = MODULE_ROLES.get(module, ("Interfaz de Usuario", "Servicio de Aplicacion"))
    lines = [
        "",
        ".. uml::",
        f" :caption: {uc_title} — Comunicacion entre Objetos",
        "",
        " @startuml",
        "",
        f' object ":{actor}" as Actor',
        f' object ":{iface}" as Iface',
        f' object ":{svc}" as Svc',
        ' object ":Repositorio" as Repo',
        ' object ":Almacen de Datos" as Store',
        "",
        " Actor -> Iface : 1: solicitar accion",
        " Iface -> Svc : 2: invocar endpoint",
        " Svc -> Svc : 3: validar RBAC",
        " Svc -> Repo : 4: ejecutar operacion",
        " Repo -> Store : 5: query / SP",
        " Store --> Repo : 6: resultado",
        " Repo --> Svc : 7: entidad",
        " Svc --> Iface : 8: respuesta",
        " Iface --> Actor : 9: renderizar",
        "",
        " @enduml",
        "",
    ]
    return "\n".join(lines)


def fix_sequence_names(content, module):
    """Fix technology names in sequence diagrams to semantic roles."""
    iface, svc = MODULE_ROLES.get(module, ("Interfaz de Usuario", "Servicio de Aplicacion"))
    # Replace quoted labels (participant/actor declarations)
    replacements = [
        ('"React Frontend"',   f'"{iface}"'),
        ('"Django API"',       f'"{svc}"'),
        ('"Django API Server"',f'"{svc}"'),
        ('"MariaDB"',          '"Almacen de Datos"'),
        ('"MySQL"',            '"Almacen de Datos"'),
        ('"Redis"',            '"Cache de Sesiones"'),
        # aliases used in message arrows
        ('as Frontend\n',      'as Iface\n'),
        ('as Frontend ',       'as Iface '),
        ('as APIServer\n',     'as SvcNode\n'),
        ('as APIServer ',      'as SvcNode '),
        ('as BaseDatos\n',     'as Store\n'),
        ('as BaseDatos ',      'as Store '),
        # message arrows referencing old aliases
        ('Frontend ->',        'Iface ->'),
        ('Frontend -->',       'Iface -->'),
        ('-> Frontend',        '-> Iface'),
        ('--> Frontend',       '--> Iface'),
        ('APIServer ->',       'SvcNode ->'),
        ('APIServer -->',      'SvcNode -->'),
        ('-> APIServer',       '-> SvcNode'),
        ('--> APIServer',      '--> SvcNode'),
        ('BaseDatos ->',       'Store ->'),
        ('BaseDatos -->',      'Store -->'),
        ('-> BaseDatos',       '-> Store'),
        ('--> BaseDatos',      '--> Store'),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content


def replace_deploy_diagram(content, uc_title, module):
    """Replace the entire @startuml...@enduml block in the deployment diagram."""
    new_diagram = deploy_diagram(uc_title, module)
    # Replace the uml directive block (caption + plantuml content)
    pattern = re.compile(
        r"\.\. uml::\n.*?:caption:.*?\n\n\s*@startuml.*?@enduml",
        re.DOTALL,
    )
    replacement = new_diagram.strip()
    new_content, n = pattern.subn(replacement, content, count=1)
    if n == 0:
        # No match — append
        new_content = content.rstrip() + "\n" + new_diagram
    return new_content


def insert_before_seealso(content, section):
    if ".. seealso::" in content:
        return content.replace(".. seealso::", section + "\n.. seealso::", 1)
    return content.rstrip() + "\n" + section


def process_domain_model():
    view_dir = os.path.join(BASE, "DomainModel")
    modified = 0
    for fname in sorted(os.listdir(view_dir)):
        if fname == "index.rst" or not fname.endswith(".rst"):
            continue
        module = get_module(fname)
        if not module or module not in STATE_MACHINES:
            print(f"  DomainModel SKIP {fname}")
            continue
        fpath = os.path.join(view_dir, fname)
        with open(fpath) as f:
            content = f.read()
        if "hide empty description" in content:
            continue
        uc_title = get_uc_title(content)
        section = state_machine_section(uc_title, module)
        if not section:
            continue
        content = insert_before_seealso(content, section)
        with open(fpath, "w") as f:
            f.write(content)
        modified += 1
    print(f"DomainModel: {modified} files modified (state machine added)")


def process_design_view():
    view_dir = os.path.join(BASE, "DesignView")
    modified = 0
    for fname in sorted(os.listdir(view_dir)):
        if fname == "index.rst" or not fname.endswith(".rst"):
            continue
        module = get_module(fname)
        fpath = os.path.join(view_dir, fname)
        with open(fpath) as f:
            content = f.read()
        new_content = fix_sequence_names(content, module) if module else content
        if "Comunicacion entre Objetos" not in new_content:
            m = re.search(r'actor "([^"]+)"', new_content)
            actor = m.group(1) if m else "Usuario"
            uc_title = get_uc_title(new_content)
            comm = communication_section(uc_title, actor, module or "")
            new_content = insert_before_seealso(new_content, comm)
        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            modified += 1
    print(f"DesignView: {modified} files modified (roles fixed + comm diagram added)")


def process_deploy_view():
    """Replace deployment diagrams with canonical Apache architecture."""
    view_dir = os.path.join(BASE, "DeployView")
    modified = 0
    for fname in sorted(os.listdir(view_dir)):
        if fname == "index.rst" or not fname.endswith(".rst"):
            continue
        module = get_module(fname)
        fpath = os.path.join(view_dir, fname)
        with open(fpath) as f:
            content = f.read()
        uc_title = get_uc_title(content)
        new_content = replace_deploy_diagram(content, uc_title, module or "")
        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            modified += 1
    print(f"DeployView: {modified} files modified (Apache architecture applied)")


if __name__ == "__main__":
    process_domain_model()
    process_design_view()
    process_deploy_view()
    print("Done.")
