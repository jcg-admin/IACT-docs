#!/usr/bin/env python3
"""
Fix technology names in UC narrative files (NOT implementacion-tecnica.rst).

Rule (D-ETL-005): source/requisitos/ narrative uses ABSTRACT vocabulary.
source/arquitectura-tecnica/ and implementacion-tecnica.rst CAN use tech names.

Targets:
  - flujo-principal.rst
  - actores-precondiciones.rst
  - criterios-aceptacion.rst
  - datos-involucrados.rst
  - informacion-general.rst
  - patrones-diseno.rst
  - requisitos-no-funcionales.rst
  - excepciones.rst
  - diagramas-uml.rst  (participant labels only)

Excluded:
  - implementacion-tecnica.rst  (explicitly technical)
  - _metodologia-aplicacion/    (pattern/methodology docs)
"""
import os
import re

BASE = "/home/user/IACT-docs/source/requisitos/casos-uso"

NARRATIVE_TARGETS = {
    "flujo-principal.rst",
    "actores-precondiciones.rst",
    "criterios-aceptacion.rst",
    "datos-involucrados.rst",
    "informacion-general.rst",
    "patrones-diseno.rst",
    "requisitos-no-funcionales.rst",
    "excepciones.rst",
    "diagramas-uml.rst",
}

# Order: most specific first (avoid partial matches)
REPLACEMENTS = [
    # Library/framework names with context
    (r'djangorestframework-simplejwt',      'Servicio de Tokens JWT'),
    (r'simplejwt',                           'Servicio de Tokens JWT'),
    (r'Frontend\s*\(React\)',               'Interfaz de Usuario'),
    (r'frontend\s*\(React\)',               'Interfaz de Usuario'),
    (r'"Frontend\\n\(React\)"',             '"Interfaz de Usuario"'),
    (r'"Frontend\s*\(React\)"',             '"Interfaz de Usuario"'),
    # bcrypt in code references (PlantUML / pseudocode)
    (r'bcrypt\.checkpw\(\)',               'verificarHash()'),
    (r'bcrypt\.check_password\(\)',        'verificarHash()'),
    (r'bcrypt\.hashpw\(\)',               'generarHash()'),
    (r'bcrypt\.hashpw\(([^,]+),\s*cost=12\)',   r'generarHash(\1)'),
    (r'bcrypt\.hashpw\(([^)]+)\)',        r'generarHash(\1)'),
    (r'bcrypt\s+cost\s+12',              'costo de hash configurado'),
    (r'bcrypt\s+with\s+cost\s+\d+',     'hash criptografico configurable'),
    (r'bcrypt\(([^)]+)\)',               r'hash(\1)'),
    # bcrypt in natural language (with context words)
    (r'\(bcrypt\)',                        '(hash criptografico)'),
    (r'vía bcrypt',                       'vía algoritmo de hash'),
    (r'via bcrypt',                        'via algoritmo de hash'),
    (r'con bcrypt',                        'con algoritmo de hash'),
    (r'bcrypt mismatch',                  'fallo de verificacion de hash'),
    (r'bcrypt domina la latencia',        'verificacion criptografica domina la latencia'),
    (r'bcrypt cost \d+',                  'costo de hash configurado'),
    (r'bcrypt \(libreria[^)]*\)',         'algoritmo de hash criptografico'),
    (r'bcrypt sobre',                      'hash criptografico sobre'),
    (r'con bcrypt\.',                      'con algoritmo de hash.'),
    (r'Hashear bcrypt cost \d+',          'Generar hash criptografico'),
    (r'reemplazado con bcrypt\(([^)]+)\)', r'reemplazado con hash(\1)'),
    # PBKDF2
    (r'PBKDF2',                            'algoritmo de derivacion de clave'),
    # mod_wsgi in narrative context
    (r'mod_wsgi\)',                        'Servicio de Aplicacion)'),
    (r'Apache \+ mod_wsgi',               'Servidor de Aplicacion'),
    (r'mod_wsgi',                          'Servicio de Aplicacion'),
    # React standalone (only in specific contexts — narrative, not code)
    (r'"Frontend\\n\(React\)"',           '"Interfaz de Usuario"'),
    # OperationalError / IntegrityError (Python exceptions in narrative)
    (r'OperationalError',                  'error de base de datos'),
    (r'IntegrityError',                    'error de integridad de datos'),
    # MySQL in narrative (not implementacion-tecnica)
    (r'MySQL',                             'Base de Datos'),
    # nginx in narrative (negative comparison is OK in impl-tecnica, remove from narrative)
    (r'Nginx — no \(Apache \+ mod_wsgi\)\.', ''),
    # Celery in narrative
    (r'Celery',                            'Procesador Asincrono'),
    # React 18 / Redux in narrative
    (r'React 18',                          'Framework de Interfaz'),
    (r'React Router v\d+',               'Enrutador de Interfaz'),
    (r'Redux Toolkit',                     'Gestor de Estado'),
    # DRF in narrative
    (r'DRF \d+\.\d+\+',                  'Framework de API REST'),
    (r'Django \d+\.\d+\+,\s*DRF [^,]+',  'Backend Django'),
]


def fix_file(fpath):
    with open(fpath) as f:
        content = f.read()
    new_content = content
    for pattern, replacement in REPLACEMENTS:
        new_content = re.sub(pattern, replacement, new_content)
    if new_content != content:
        with open(fpath, "w") as f:
            f.write(new_content)
        return True
    return False


def run():
    total = 0
    for root, dirs, files in os.walk(BASE):
        # Skip methodology docs
        if "_metodologia-aplicacion" in root:
            continue
        for fname in files:
            if fname not in NARRATIVE_TARGETS:
                continue
            fpath = os.path.join(root, fname)
            if fix_file(fpath):
                total += 1
                rel = fpath.replace("/home/user/IACT-docs/", "")
                print(f"  fixed: {rel}")
    print(f"\nTotal files modified: {total}")


if __name__ == "__main__":
    run()
