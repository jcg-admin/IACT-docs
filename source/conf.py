# -*- coding: utf-8 -*-
import sys
import os

# Path setup necesario para autodoc (documentar código Python)
# Permite importar módulos del proyecto para generar documentación automática
# sys.path.insert(0, os.path.abspath('../../backend'))  # Descomenta cuando tengas el backend

# -- Información General del Proyecto IACT --
project = 'IACT - Sistema de Dashboard Analytics'
copyright = '2025, Equipo IACT'
author = 'Equipo de Desarrollo IACT'

# Versión del Proyecto
version = '1.0'
release = '1.0.0'

# -- Extensiones --
extensions = [
    # Extensiones de trazabilidad y requerimientos
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',

    # Extensiones para documentar código Python
    'sphinx.ext.autodoc',  # Documentación automática desde docstrings
    'sphinx.ext.autosummary',  # Resúmenes automáticos de módulos
    'sphinx.ext.viewcode',  # Enlaces al código fuente
    'sphinx.ext.napoleon',  # Soporte para docstrings Google/NumPy style

    # Extensiones de interactividad y diseño
    'sphinx_design',
    'sphinx_copybutton',
    'myst_parser',

    # PlantUML para diagramas
    'sphinxcontrib.plantuml',
]

# -- Configuración de Autodoc --
# Generar automáticamente documentación de miembros
autodoc_default_options = {
    'members': True,  # Documentar todos los miembros
    'member-order': 'bysource',  # Orden según aparecen en el código
    'special-members': '__init__',  # Incluir __init__
    'undoc-members': True,  # Incluir miembros sin docstring
    'exclude-members': '__weakref__'
}

# Configuración de Autosummary
autosummary_generate = True  # Generar archivos stub automáticamente

# Configuración de Napoleon (docstrings estilo Google/NumPy)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Configuración de Type Hints
typehints_fully_qualified = False
always_document_param_types = True

# -- Configuración de Archivos --
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# Excluye carpetas de build y entornos virtuales
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'venv',
    '.git'
]

# -- Configuración de Lenguaje --
language = 'es'
html_search_language = 'es'

# Dominio primario (útil para documentación de APIs)
primary_domain = 'py'

# -- Estética y Resaltado --
pygments_style = 'sphinx'

# Comillas tipográficas inteligentes
smartquotes = True
smartquotes_action = 'De'  # (D)ashes y (e)llipses

# -- Configuración de Lexers --
# Ignorar warnings de lexers desconocidos (plantuml, mermaid, cql)
suppress_warnings = ['misc.highlighting_failure']

# -- Configuración de Salida HTML (Tema FURO) --
html_theme = 'furo'
html_title = 'IACT Docs'

html_static_path = ['_static']

# Archivos CSS y JS personalizados
html_css_files = [
    'css/custom.css',
]

html_js_files = [
    'js/custom.js'
]

# Opciones del tema FURO (Colores corporativos IACT)
html_theme_options = {
    'dark_css_variables': {
        'color-brand-primary': '#199cd7',
        'color-brand-content': '#199cd7',
        'color-sidebar-link-text--top-level': '#4ab8ea',
    },
    'sidebar_hide_name': True,
    'navigation_with_keys': True,  # Navegación con flechas del teclado
}

# Mostrar información de Sphinx
html_show_sphinx = True

# No copiar archivos fuente .rst al build
html_copy_source = False

# Logo y Favicon
html_favicon = '_static/img/favicon.ico'
html_logo = '_static/img/logo.svg'

# -- Configuración del Corrector Ortográfico --
spelling_word_list_filename = 'spelling_wordlist.txt'

# Excluir patrones de archivos del corrector
spelling_exclude_patterns = []

# -- Configuración del Botón de Copiado --
# Excluir prompts y salidas de consola
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = "$ "

# -- Configuración de Autosectionlabel --
# Permite referenciar secciones automáticamente con prefijos
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# -- Configuración de Salida LaTeX / PDF --
latex_elements = {}

latex_documents = [
    ('index', 'iact.tex', 'IACT - Documentación del Proyecto',
     'Equipo IACT', 'manual'),
]

# -- Configuración de Salida Man Pages --
man_pages = [
    ('index', 'iact', 'IACT - Documentación del Proyecto',
     ['Equipo IACT'], 1)
]

# -- Configuración de Salida Texinfo --
texinfo_documents = [
    ('index', 'iact', 'IACT - Documentación del Proyecto',
     'Equipo IACT', 'iact', 'Documentación centralizada del proyecto IACT.', 'Misceláneo'),
]

# -- Configuración de Salida EPUB --
epub_title = 'IACT - Documentación del Proyecto'
epub_author = 'Equipo IACT'
epub_publisher = 'Equipo IACT'
epub_copyright = '2025, Equipo IACT'
epub_exclude_files = ['search.html']

# -- Configuración de PlantUML --
plantuml = 'plantuml'
plantuml_output_format = 'png'
plantuml_latex_output_format = 'pdf'

# Centralizar imágenes y diagramas en _static/img/
# sphinxcontrib.plantuml genera en _plantuml/ por defecto
# Post-build hook reorganiza en _static/img/diagrams/
plantuml_output_dir = '_static/img/diagrams'

# Hook post-build para reorganizar archivos de imagen
def setup(app):
    """Configurar hooks post-build para organizar imagen de forma centralizada."""
    app.connect('build-finished', reorganize_static_assets)

def reorganize_static_assets(app, exception):
    """
    Post-build hook: reorganiza _images/ y _plantuml/ → _static/img/
    Luego reorganiza diagrams por módulo/tipo basado en metadatos PlantUML.
    """
    import shutil
    from pathlib import Path

    if exception:
        return  # No reorganizar si la build falló

    build_dir = Path(app.outdir)
    static_img_dir = build_dir / '_static' / 'img'

    # Crear directorio de destino si no existe
    static_img_dir.mkdir(parents=True, exist_ok=True)

    # Mover _images/ → _static/img/raster/
    images_src = build_dir / '_images'
    if images_src.exists():
        images_dst = static_img_dir / 'raster'
        if images_dst.exists():
            shutil.rmtree(images_dst)
        shutil.move(str(images_src), str(images_dst))

    # Mover _plantuml/ → _static/img/diagrams/
    plantuml_src = build_dir / '_plantuml'
    if plantuml_src.exists():
        diagrams_dst = static_img_dir / 'diagrams'
        if diagrams_dst.exists():
            shutil.rmtree(diagrams_dst)
        shutil.move(str(plantuml_src), str(diagrams_dst))

    # Reorganizar diagrams usando metadatos PlantUML
    reorganize_by_plantuml_metadata(static_img_dir / 'diagrams', app.srcdir)


def reorganize_by_plantuml_metadata(diagrams_dir, source_dir):
    """
    Lee metadatos @IACT-DIAGRAM de archivos RST
    y reorganiza PNGs en diagrams/{modulo}/{tipo}/
    Formato de metadatos PlantUML:
      ' @IACT-DIAGRAM
      ' module: requisitos
      ' type: use-case
      ' description: ...
    """
    import re
    import hashlib
    from pathlib import Path
    import shutil

    if not diagrams_dir.exists():
        return

    # Paso 1: Extraer metadatos de todos los RST files
    metadata_map = extract_diagram_metadata(source_dir)

    # Paso 2: Crear estructura de directorios
    modulos = {
        "requisitos": ["use-case", "activity", "state"],
        "arquitectura_tecnica": ["component", "deployment", "sequence", "activity"],
        "base_cognitiva": ["use-case", "activity"],
        "normativa": ["diagram"],
        "gestion": ["diagram"],
        "plantuml-guide": ["use-case", "component", "sequence", "activity", "diagram"],
    }

    for modulo, tipos in modulos.items():
        for tipo in tipos:
            dest_dir = diagrams_dir / modulo / tipo
            dest_dir.mkdir(parents=True, exist_ok=True)

    # Paso 3: Reorganizar PNGs basándose en metadatos
    hash_dirs = sorted([d for d in diagrams_dir.iterdir() if d.is_dir() and len(d.name) == 2])

    for hash_dir in hash_dirs:
        pngs = list(hash_dir.glob("*.png"))
        if not pngs:
            continue

        # Buscar en metadatos (usando la ubicación del RST como clave)
        modulo, tipo = "plantuml-guide", "diagram"  # Defaults

        for puml_content, (found_modulo, found_tipo) in metadata_map.items():
            if found_modulo and found_tipo:
                modulo, tipo = found_modulo, found_tipo
                break

        dest = diagrams_dir / modulo / tipo
        dest.mkdir(parents=True, exist_ok=True)

        for png in pngs:
            try:
                shutil.move(str(png), str(dest / png.name))
            except Exception:
                pass

    # Limpiar directorios vacíos
    for hash_dir in hash_dirs:
        try:
            hash_dir.rmdir()
        except Exception:
            pass


def extract_diagram_metadata(source_dir):
    """
    Extrae metadatos @IACT-DIAGRAM de bloques PlantUML en RST files.
    Retorna dict: {contenido_puml: (modulo, tipo)}
    """
    import re
    from pathlib import Path
    from collections import defaultdict

    metadata_map = {}

    # Buscar todos los archivos RST con bloques .. uml::
    for rst_file in Path(source_dir).rglob("*.rst"):
        try:
            with open(rst_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        # Regex para bloques .. uml:: ... (incluyendo @enduml)
        pattern = r'\.\. uml::.*?\n((?:(?:\n)?(?:^|\s{1,}).+?)*?)(?=\n[^ \t]|\Z)'

        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            puml_block = match.group(1)

            # Extraer metadatos @IACT-DIAGRAM
            modulo = None
            tipo = None

            meta_pattern = r"'\s*@IACT-DIAGRAM.*?'?\s*module:\s*(\w+).*?'?\s*type:\s*(\w+(?:-\w+)?)"
            meta_match = re.search(meta_pattern, puml_block, re.DOTALL)

            if meta_match:
                modulo = meta_match.group(1)
                tipo = meta_match.group(2)
                metadata_map[puml_block] = (modulo, tipo)

    return metadata_map