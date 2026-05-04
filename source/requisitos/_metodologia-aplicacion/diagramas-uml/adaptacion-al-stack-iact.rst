Adaptación al stack IACT
^^^^^^^^^^^^^^^^^^^^^^^^

IACT usa **Sphinx + sphinxcontrib-plantuml** sobre
el stack canónico ADR_DEVOPS_001 (Apache +
mod_wsgi + Django + MySQL + Redis). Eso simplifica
el pipeline:

- ``sphinxcontrib-plantuml`` ya está integrado en
  ``conf.py``.
- ``make html`` invoca el render automáticamente
  desde el código fuente del diagrama.
- No se necesita un paso separado de "convertir
  Mermaid a SVG" — los bloques ``.. uml::``
  invocan al servidor PlantUML.

El pipeline IACT puede limitarse a:

1. **Detectar el evento** (push a la rama de
   docs, o tag de release).
2. **Checkout** del repo.
3. **Instalar dependencias** (``pip install
   -r requirements.txt``).
4. **Build** (``make html``) — incluye el render
   PlantUML.
5. **Publicar** los artefactos al servidor de
   documentación interna.

No requiere conversión Mermaid → SVG ni
generación Jekyll: el motor de render forma
parte del propio Sphinx.
