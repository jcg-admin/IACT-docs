Publicación con Sphinx
~~~~~~~~~~~~~~~~~~~~~~

El pipeline canónico del proyecto:

1. Diagrama embebido en ``.rst`` con
   ``.. uml::`` (Sphinx directive).
2. Estilos compartidos vía
   ``!include ../../_static/plantuml-styles.puml``.
3. ``make html`` invoca ``sphinxcontrib-plantuml`` →
   genera SVG/PNG → embebe en el sitio.

Ver :doc:`/base-cognitiva/plantuml-guide/guidelines`
para detalles de configuración.
