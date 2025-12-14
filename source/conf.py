# -*- coding: utf-8 -*-
import sys
import os

# -- Extensiones --
extensions = [
    # Extensiones de trazabilidad y requerimientos
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.ifconfig',
    
    # Extensiones de para interactividad y diseño
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_toolbox.collapse',
    'notfound.extension',
    'sphinx_sitemap',
    'myst_parser',
]

# -- Configuración de Archivos --
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# -- Información General del Proyecto IACT --
project = u'IACT - Sistema de Dashboard Analytics'
copyright = u'2025, Equipo IACT'
author = u'Equipo de Desarrollo IACT'

# Versión del Proyecto
version = '1.0'
release = '1.0.0'

# Excluye carpetas de build y entornos virtuales para mantener la fuente limpia.
exclude_patterns = [
    '_build', 
    'Thumbs.db', 
    '.DS_Store', 
    'venv', 
    '.git'
]

# -- Estética y Resaltado --
pygments_style = 'sphinx'

# -- Configuración de Lenguaje --
language = 'es'

# Esto ayuda a que el buscador sea más preciso con términos técnicos
html_search_language = 'es'

# -- Configuración de Salida HTML (Tema FURO, Estilo IACT) --
html_theme = 'furo' 
html_title = 'IACT Docs' # Título que aparecerá en la pestaña del navegador

html_static_path = ['_static']

# Archivos CSS y JS para personalización (similar al modelo ODK)
html_css_files = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css',
    'css/custom.css',
]
html_js_files = ["js/custom.js"]

# Opciones específicas del tema FURO (Colores de marca y comportamiento)
html_theme_options = {
    'light_css_variables': {
        'color-brand-primary': '#009ECC',
        'color-brand-content': '#009ECC',
    },
    'dark_css_variables': {
        'color-brand-primary': '#009ECC',
        'color-brand-content': '#009ECC',
    },
    'sidebar_hide_name': True,
}

# Configuración del botón de copiado (para la extensión sphinx_copybutton)
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = "$ " 

# -- Configuración de Autosectionlabel --
# Permite referenciar secciones automáticamente con prefijos basados en el documento.
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# -- Configuración de Salida LaTeX / PDF --
# Genera el manual en formato .tex para compilar a PDF.
latex_elements = { }

latex_documents = [
  # Archivo maestro, Nombre del archivo de salida, Título del documento, Autor, Tipo
  ('index', 'iact.tex', u'IACT - Documentación del Proyecto',
   u'Equipo IACT', 'manual'),
]

# -- Configuración de Salida Man Pages --
# Genera el archivo para sistemas tipo UNIX.
man_pages = [
    # Archivo maestro, Nombre de salida, Descripción, Autores, Sección
    ('index', 'iact', u'IACT - Documentación del Proyecto',
     [u'Equipo IACT'], 1)
]

# -- Configuración de Salida Texinfo --
# Genera el archivo para el sistema de ayuda de GNU.
texinfo_documents = [
  # Archivo maestro, Nombre de salida, Título, Autor, Top Level Index, Descripción
  ('index', 'iact', u'IACT - Documentación del Proyecto',
   u'Equipo IACT', 'iact', u'Documentación centralizada del proyecto IACT.', 'Misceláneo'),
]

# -- Configuración de Salida EPUB --
# Genera el libro electrónico.
epub_title = u'IACT - Documentación del Proyecto'
epub_author = u'Equipo IACT'
epub_publisher = u'Equipo IACT'
epub_copyright = u'2025, Equipo IACT'
epub_exclude_files = ['search.html']