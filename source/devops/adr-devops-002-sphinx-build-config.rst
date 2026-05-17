.. meta::
 :artefacto: ADR_DEVOPS_002_sphinx_build_config
 :tipo: ADR
 :dominio: devops
 :subdominio: build
 :estado: Aceptada
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Alto

.. _adr_devops_002_sphinx_build_config:

========================================================
ADR-DEVOPS-002: Configuración de Build Sphinx en conf.py
========================================================

Contexto
--------

Durante el WP ``2026-05-05-05-07-43-merge-develop-pr-review`` se
identificaron tres cambios en ``conf.py`` y ``pyproject.toml``
realizados sin ADR visible (hallazgo F-03):

1. Remoción de ``myst-parser`` del entorno de dependencias.
2. ``nitpicky`` ahora controlable via variable de entorno
   ``SPHINX_NITPICKY``.
3. Adición de ``plantuml_cfg_file`` apuntando a
   ``_static/plantuml-styles.puml``.

Además, el CI ``validate.yml`` tenía ``timeout-minutes: 20`` y
``sphinx-build`` sin paralelismo, lo que causaba un timeout al 24%
(hallazgo F-01) dado que el build local toma ~36 min con 965 diagramas
PlantUML.

Decisiones
----------

Remoción de myst-parser
~~~~~~~~~~~~~~~~~~~~~~~~

``myst-parser`` permitía usar Markdown (``.md``) como fuente en
Sphinx. El proyecto IACT adoptó RST puro (ver ADR-GOB-001 y STD-007).
Mantener ``myst-parser`` instalado agrega una dependencia innecesaria
y puede generar advertencias de extensión no utilizada.

**Decisión**: eliminar ``myst-parser`` de ``pyproject.toml`` y del
listado de extensiones en ``conf.py``. Todos los archivos fuente son
``.rst``.

nitpicky via SPHINX_NITPICKY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``nitpicky = True`` activa la detección de cross-references rotas como
errores de build. En desarrollo local, esto ralentiza la iteración
porque cualquier referencia pendiente rompe el build. En CI pre-merge
es el comportamiento correcto.

**Decisión**: controlar ``nitpicky`` con la variable de entorno
``SPHINX_NITPICKY``:

- ``SPHINX_NITPICKY`` no definido (default): ``nitpicky=False`` —
  build rápido para iteración local.
- ``SPHINX_NITPICKY=1 make html``: ``nitpicky=True`` — gate estricto
  antes de merge.

Esto sigue el principio de entornos separados sin bifurcar el
``conf.py``.

plantuml_cfg_file
~~~~~~~~~~~~~~~~~

``sphinxcontrib-plantuml`` escribe cada diagrama a un archivo temporal
en ``/tmp/``. Los estilos globales definidos con ``!include`` en RST
fallan porque el path relativo no se resuelve desde ``/tmp/``.

**Decisión**: usar ``plantuml_cfg_file`` apuntando al archivo
``_static/plantuml-styles.puml`` con un path absoluto calculado
en ``conf.py``. Esto inyecta los estilos en todos los diagramas sin
requerir ``!include`` en cada archivo RST.

El archivo solo se activa si existe en disco; si no existe, Sphinx
continua sin estilos globales (falla silenciosa intencionada para
builds limpios sin el archivo de estilos).

Timeout CI y paralelismo
~~~~~~~~~~~~~~~~~~~~~~~~

Con 965 diagramas PlantUML, ``sphinx-build`` serial tarda ~36 min.
``validate.yml`` tenía ``timeout-minutes: 20``, causando cancelación
al 24%.

**Decisión**:

- ``timeout-minutes: 20 → 60`` para dar margen al build completo.
- ``sphinx-build -j auto`` para usar todos los CPUs disponibles en
  el runner de GitHub Actions (Ubuntu, típicamente 2 vCPUs), reduciendo
  el tiempo estimado a ~18-20 min.

Alternativas Consideradas
-------------------------

Cache de diagramas PlantUML
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cachear ``build/`` entre runs de CI para no regenerar diagramas sin
cambios. Descartado porque: (a) requiere invalidación correcta por
hash de archivos ``.puml``, (b) la caché de GitHub Actions tiene
límite de 10 GB y el build genera ~1 GB de PNGs, (c) complejidad de
mantenimiento. Se puede considerar en un WP posterior si el tiempo
sigue siendo un problema.

Servidor PlantUML remoto
~~~~~~~~~~~~~~~~~~~~~~~~

Usar ``plantuml_server`` en lugar de ``plantuml.jar`` local para
delegar la generación al servidor público de PlantUML. Descartado por:
(a) dependencia de disponibilidad de servicio externo en CI, (b)
privacidad de los diagramas, (c) rate limiting.

Consecuencias
-------------

Positivas
~~~~~~~~~

- CI no expira con 965 diagramas.
- Build local es más rápido (sin ``nitpicky`` por defecto).
- Estilos PlantUML consistentes en todos los diagramas sin boilerplate
  en cada RST.
- Dependencias reducidas al eliminar ``myst-parser``.

Negativas
~~~~~~~~~

- ``nitpicky=False`` local puede ocultar referencias rotas hasta que
  se corra con ``SPHINX_NITPICKY=1``. Mitigación: el CI siempre corre
  con ``-W`` (warnings as errors); agregar ``SPHINX_NITPICKY=1`` al
  paso CI si se requiere.
- ``-j auto`` puede causar condiciones de carrera en builds muy
  grandes si alguna extensión no es thread-safe. Monitorear en las
  primeras runs post-merge.

Referencias
-----------

- Hallazgo F-01 / F-03 — WP ``merge-develop-pr-review``
  (`.thyrox/context/work/2026-05-05-05-07-43-merge-develop-pr-review/discover/merge-pr-review-analysis.md`)
- :doc:`/normativa/gobernanza/adr-gob-002-plantuml-para-diagramas` — PlantUML como estándar
  para diagramas.
- :doc:`/normativa/gobernanza/adr-gob-001-organizacion-proyecto-por-dominio` —
  RST puro como formato de documentación.
- `sphinxcontrib-plantuml docs <https://pypi.org/project/sphinxcontrib-plantuml/>`__
- `sphinx-build -j docs <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`__
