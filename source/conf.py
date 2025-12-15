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
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.ifconfig',

    # Extensiones para documentar código Python (desactivadas temporalmente)
    # 'sphinx.ext.autodoc',  # Documentación automática desde docstrings
    # 'sphinx.ext.autosummary',  # Resúmenes automáticos de módulos
    # 'sphinx.ext.viewcode',  # Enlaces al código fuente
    # 'sphinx.ext.napoleon',  # Soporte para docstrings Google/NumPy style
    # 'sphinx_autodoc_typehints',  # Type hints en la documentación

    # Extensiones de interactividad y diseño
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_toolbox.collapse',
    'notfound.extension',
    'myst_parser',
    'sphinx-prompt',

    # Nuevas extensiones
    'sphinxcontrib.spelling',  # Corrector ortográfico
    'openapi',  # Documentación de APIs REST
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