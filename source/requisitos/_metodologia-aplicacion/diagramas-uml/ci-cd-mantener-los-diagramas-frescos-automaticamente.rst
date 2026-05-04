CI/CD — mantener los diagramas frescos automáticamente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una preocupación recurrente con cualquier
documentación: **se desactualiza**. Las técnicas
manuales (``make html`` local, exportar SVG
puntuales) dependen de que alguien las ejecute.

La práctica robusta: **automatizar la generación
en el pipeline** del proyecto, de modo que cada
cambio en el código fuente de un diagrama
(``.rst`` con ``.. uml::`` o archivos
``.puml``) produzca el render actualizado sin
intervención manual.

Antes de implementar, visualizar el plan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Un patrón útil — sugerido en la literatura de
diagramado — es **diagramar el flujo del propio
pipeline** antes de escribirlo. Convierte una
discusión informal en una propuesta concreta:

::

   Inicio → Detectar evento → Checkout repo
         → Render PlantUML (sphinxcontrib-plantuml)
         → Build Sphinx (make html)
         → Publicar artefactos
         → Fin

Cada paso anterior se traduce a una etapa del
pipeline. Si la lista no encaja con el stack
disponible, el plan se ajusta antes de tocar
código.

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

Diferencia con el enfoque del libro citado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La obra de la que tomamos el patrón conceptual
asume Mermaid + Jekyll + GitHub Pages, con un
paso explícito de "convertir Mermaid a SVG" en
el CI antes de generar Jekyll. En IACT ese paso
**no existe**: PlantUML + Sphinx ya integran el
render como parte del build.

Esto refuerza la decisión documentada en la
sección "Historia de la diagramación y por qué
IACT eligió PlantUML": la toolchain del proyecto
elimina pasos intermedios que el enfoque Mermaid
requiere.

Política IACT — pipeline de diagramas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **No depender del build local** como
   única ruta de generación. El servidor de
   documentación se actualiza desde el pipeline.
2. **Diagramar el flujo del pipeline** antes de
   modificarlo — el flowchart se versiona
   junto con el ADR del cambio.
3. **Pipeline mínimo** — checkout, install,
   build, publish. Sin pasos accesorios que el
   stack ya cubre.
4. **Cualquier broker de CI externo** o
   herramienta adicional al stack canónico
   (GitHub Actions self-hosted, GitLab CI,
   Jenkins) requiere ADR si modifica las
   garantías del pipeline actual.
5. **Verificación**: cada deploy del sitio de
   documentación debe garantizar que **todos**
   los ``.. uml::`` rinden sin error. Un fallo
   de render bloquea el deploy.

Patrón "visualizar antes de actuar"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Más allá del CI específico, la lección
operativa es general: cuando hay que armar un
flujo de pasos (pipeline, deploy, refactor,
migración), **dibujar el flowchart** primero
suele:

- Exponer pasos olvidados.
- Mostrar dependencias entre pasos.
- Servir de contrato para la implementación.
- Actuar como referencia para el siguiente
  ingeniero que toque el flujo.

Es la misma idea que sostiene el resto del
cajón: el diagrama no decora — **anticipa
problemas y comunica intención**.
