#################################################
IACT - Sistema de Dashboard Analytics
#################################################

La documentación de IACT es un proyecto centralizado que articula el conocimiento 
del Dashboard de Analytics. Su objetivo es facilitar la trazabilidad entre los 
requerimientos de negocio, la implementación técnica y el control de gestión.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Dominio de Producto

   producto/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Dominio del Sistema

   sistema/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Dominio de Gestión

   gestion/index

Estructura de Documentación
===========================

El proyecto se divide en tres dominios fundamentales para garantizar la 
separación de responsabilidades y la claridad del sistema:

.. grid:: 1 1 3 3
   :gutter: 3

   .. grid-item-card:: Dominio de Producto
      :link: producto/index

      Contiene la definición del "Qué". Incluye las Reglas de Negocio (BR), 
      Casos de Uso (UC) y el análisis de requerimientos funcionales 
      del Dashboard.

   .. grid-item-card:: Dominio del Sistema
      :link: sistema/index

      Detalla el "Cómo". Describe la arquitectura dual de bases de datos 
      (MySQL y PostgreSQL), el flujo del proceso ETL y la implementación 
      en Django y React.

   .. grid-item-card:: Dominio de Gestión
      :link: gestion/index

      Presenta el "Cuándo". Incluye el WBS del proyecto, la gestión de 
      riesgos, el plan de pruebas y el seguimiento de tareas pendientes (TODO).