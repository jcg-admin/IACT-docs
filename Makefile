# Makefile para la documentación generada con Sphinx + uv
#
# Este proyecto usa 'uv' para gestión de dependencias (rápido, moderno).
# Flujo recomendado antes de ejecutar 'make':
#
#   uv sync                        # Instala dependencias del pyproject.toml
#   source .venv/bin/activate      # Activa el entorno virtual
#   make html                      # Genera documentación
#
# ========================================================================================
# INSTALACIÓN INICIAL:
#
#   Si no tienes 'uv' instalado:
#     pip install uv  (o)  apt-get install uv  (o)  brew install uv
#
# ========================================================================================
# NOTA IMPORTANTE PARA WINDOWS (Git Bash):
#
# Para activar el entorno virtual, usar:
#   source .venv/Scripts/activate
#
# El comando de activación '.venv\Scripts\Activate.ps1' es solo para PowerShell.
# ========================================================================================
# CAMBIOS DESDE REQUIREMENTS.TXT:
#
# - requirements.txt eliminado (migration a pyproject.toml + uv.lock)
# - uv reemplaza pip: 10x más rápido, resolución determinística
# - pyproject.toml: fuente única de verdad (estándar PEP 517/518)
# - uv.lock: lock file determinístico (reproducible en CI/CD)
# ========================================================================================

# Directorio del entorno virtual (si existe)
VENV            = .venv

# Estas variables pueden definirse desde la línea de comandos.
SPHINXOPTS      =

# Selección de sphinx-build:
# 1) Si existe el ejecutable en .venv/Scripts, usarlo (entorno virtual).
# 2) Si no existe, usar el sphinx-build global del sistema.
ifeq ("$(wildcard $(VENV)/Scripts/sphinx-build.exe)","")
SPHINXBUILD     = sphinx-build
else
SPHINXBUILD     = $(VENV)/Scripts/sphinx-build.exe
endif

# Selección de sphinx-autobuild:
# Debe estar instalado en el .venv
ifeq ("$(wildcard $(VENV)/Scripts/sphinx-autobuild.exe)","")
SPHINXAUTOBUILD = sphinx-autobuild
else
SPHINXAUTOBUILD = $(VENV)/Scripts/sphinx-autobuild.exe
endif

PAPER           =
BUILDDIR        = build

# Verificación amigable para comprobar que sphinx-build está instalado.
# Si no se encuentra el comando, se muestra un mensaje de error claro.
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error El comando '$(SPHINXBUILD)' no fue encontrado. Asegúrate de tener Sphinx instalado. \
Si ya está instalado, configura la variable de entorno SPHINXBUILD con la ruta completa del ejecutable \
o agrega dicho directorio a tu PATH. Si no tienes Sphinx, descárgalo en http://sphinx-doc.org/)
endif

# Variables internas utilizadas por los distintos targets.
# Especifican tamaño de papel para construcciones LaTeX.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter

# Opciones generales que usan la mayoría de los builders.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source

# El builder de internacionalización (i18n) no puede compartir doctrees con los demás.
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source

# Declaración de targets lógicos para evitar conflictos con archivos existentes.
help: help-uv help-sphinx

help-uv:
	@echo "UV Targets (Dependency Management):"
	@echo "  make sync              Instala dependencias con uv (ejecutar primero)"
	@echo "  make update-deps       Actualiza uv.lock y resuelve dependencias"
	@echo ""

help-sphinx:
	@echo "Sphinx Targets (Documentation Building):"
	@echo "  make html              Genera documentación HTML (DEFAULT)"
	@echo "  make livehtml           HTML con auto-rebuild en cambios"
	@echo "  make clean             Limpia archivos generados"
	@echo "  make latexpdf          Genera PDF (requiere LaTeX)"
	@echo "  make linkcheck         Valida enlaces externos"
	@echo ""

.PHONY: sync update-deps help help-uv help-sphinx requirements help clean html livehtml freeze dirhtml singlehtml pickle json htmlhelp \
qthelp devhelp epub latex latexpdf latexpdfja text man texinfo info \
gettext changes linkcheck doctest xml pseudoxml

sync:
	@echo "Instalando dependencias con uv..."
	@uv sync --no-dev
	@echo "✅ Dependencias instaladas. Ejecuta: make html"

update-deps:
	@echo "Actualizando uv.lock..."
	@uv lock
	@uv sync
	@echo "✅ Dependencias actualizadas"

# Target documental para indicar el uso de requirements.txt
requirements:
	@echo "Instale las dependencias necesarias ejecutando:"
	@echo "  pip install -r requirements.txt"

# Muestra una guía rápida de los targets disponibles.
help:
	@echo "Utiliza 'make <target>' donde <target> es uno de los siguientes:"
	@echo "  html       para generar archivos HTML independientes"
	@echo "  livehtml   para iniciar el servidor de desarrollo con recarga en vivo (Live Reload)"
	@echo "  dirhtml    para generar HTML con estructura basada en directorios"
	@echo "  singlehtml para generar un único archivo HTML"
	@echo "  pickle     para generar archivos pickle"
	@echo "  json       para generar archivos JSON"
	@echo "  htmlhelp   para generar archivos HTML y un proyecto HTML Help"
	@echo "  qthelp     para generar archivos HTML y un proyecto qthelp"
	@echo "  devhelp    para generar archivos aptos para Devhelp"
	@echo "  epub       para generar un archivo ePub"
	@echo "  latex      para generar archivos LaTeX (PAPER=a4 o PAPER=letter)"
	@echo "  latexpdf   para generar LaTeX y convertirlo automáticamente a PDF"
	@echo "  latexpdfja para generar PDFs usando platex/dvipdfmx"
	@echo "  text       para generar archivos de texto plano"
	@echo "  man        para generar páginas de manual tipo man"
	@echo "  texinfo    para generar archivos Texinfo"
	@echo "  info       para generar archivos Info mediante makeinfo"
	@echo "  gettext    para generar catálogos de mensajes PO"
	@echo "  changes    para generar un resumen de elementos modificados"
	@echo "  xml        para generar archivos XML nativos de Docutils"
	@echo "  pseudoxml  para generar pseudo-XML para inspección visual"
	@echo "  linkcheck  para validar enlaces externos"
	@echo "  doctest    para ejecutar doctests incluidos en la documentación"

# Elimina todo el contenido generado dentro del directorio de construcción.
clean:
	rm -rf $(BUILDDIR)/*

# Builder para HTML estándar.
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Construcción finalizada. Los archivos HTML están en $(BUILDDIR)/html."

# Nuevo target para Live Reload (Servidor embebido)
livehtml:
	@echo "Iniciando servidor con recarga en vivo (Live Reload)..."
	@echo "Detenga con Ctrl+C."
	$(SPHINXAUTOBUILD) source $(BUILDDIR)/html
	@echo

# Builder para HTML con estructura basada en directorios.
dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Construcción finalizada. Los archivos HTML están en $(BUILDDIR)/dirhtml."

# Builder para un único archivo HTML.
singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Construcción finalizada. El archivo HTML está en $(BUILDDIR)/singlehtml."

# Builder para formato pickle.
pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Construcción finalizada; ahora puedes procesar los archivos pickle."

# Builder para formato JSON.
json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Construcción finalizada; ahora puedes procesar los archivos JSON."

# Builder para HTML Help (Windows).
htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Construcción finalizada. Puedes abrir el proyecto .hhp en $(BUILDDIR)/htmlhelp."

# Builder para documentación estilo QtHelp.
qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Construcción finalizada. Ejecuta qcollectiongenerator con el archivo .qhcp."

# Builder para documentación compatible con Devhelp.
devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Construcción finalizada."

# Builder para generar un archivo ePub.
epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Construcción finalizada. El archivo ePub está en $(BUILDDIR)/epub."

# Builder para generar archivos LaTeX.
latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Construcción finalizada. Los archivos LaTeX están en $(BUILDDIR)/latex."

# Builder para generar archivos PDF a partir de LaTeX.
latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Ejecutando pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finalizado. Los archivos PDF están en $(BUILDDIR)/latex."

# Builder para PDF con platex/dvipdfmx (común en documentación japonesa).
latexpdfja:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Ejecutando platex y dvipdfmx..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf-ja
	@echo "Conversión finalizada. Los PDF están en $(BUILDDIR)/latex."

# Builder para generar archivos de texto plano.
text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Construcción finalizada. Los archivos de texto están en $(BUILDDIR)/text."

# Builder para generar páginas de manual tipo man.
man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Construcción finalizada. Los archivos man están en $(BUILDDIR)/man."

# Builder para Texinfo.
texinfo:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Construcción finalizada. Los archivos Texinfo están en $(BUILDDIR)/texinfo."

# Builder para generar archivos Info.
info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Ejecutando makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finalizado. Los archivos Info están en $(BUILDDIR)/texinfo."

# Builder para generar catálogos de internacionalización.
gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Construcción finalizada. Los catálogos están en $(BUILDDIR)/locale."

# Builder para generar un resumen de cambios.
changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "El archivo de resumen está en $(BUILDDIR)/changes."

# Builder para validar integridad de enlaces externos.
linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Validación completada. Revisa $(BUILDDIR)/linkcheck/output.txt para detalles."

# Builder para ejecutar doctests incluidos en la documentación.
doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Ejecución de doctests finalizada. Consulta $(BUILDDIR)/doctest/output.txt."

# Builder para generar archivos XML nativos.
xml:
	$(SPHINXBUILD) -b xml $(ALLSPHINXOPTS) $(BUILDDIR)/xml
	@echo
	@echo "Construcción finalizada. Los archivos XML están en $(BUILDDIR)/xml."

# Builder para generar pseudo-XML legible para depuración.
pseudoxml:
	$(SPHINXBUILD) -b pseudoxml $(ALLSPHINXOPTS) $(BUILDDIR)/pseudoxml
	@echo
	@echo "Construcción finalizada. Los archivos pseudo-XML están en $(BUILDDIR)/pseudoxml."