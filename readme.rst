########################################################################
Repositorio de documentación para `oracle.rtfd.io <http://oracle.rtfd.io>`_
########################################################################

Esta es la rama de documentación en **español mexicano** del proyecto
**Oracle SQL & PL/SQL Optimization for Developers**.

La versión local de esta adaptación es **0.0.2**, basada en el proyecto
original en inglés (versión 4.0.0) iniciado por
`Ian Reppel <https://ianreppel.org>`_.

El propósito del proyecto es ayudar a personas desarrolladoras a escribir
SQL y PL/SQL eficientes para bases de datos Oracle modernas. Además,
recopila experiencias (exitosas y no tanto) obtenidas al trabajar con
sistemas de producción reales.

Este repositorio público de Git contiene los archivos en
**reStructuredText (reST)** y la configuración necesaria para construir
la documentación con **Sphinx** y publicarla en
`Read the Docs (RTD) <http://readthedocs.org>`_.

La estructura de encabezados sigue las
`convenciones por defecto de Sphinx <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections>`_:

* ``#`` (con línea superior) para partes
* ``*`` (con línea superior) para capítulos
* ``=`` para secciones
* ``-`` para subsecciones
* ``^`` para sub-subsecciones
* ``"`` para niveles inferiores

En los archivos de este repositorio se utiliza con frecuencia la
directiva ``include`` para reutilizar contenido. La interpretación de
los adornos (``#``, ``*``, ``=``, etc.) es **relativa al archivo que
incluye**, no al archivo incluido. Por ello, es importante que el nivel
más alto de cada archivo incluido sea coherente con el lugar donde se
usa la directiva ``include``.

La directiva ``include`` lee el contenido del archivo como si formara
parte del documento en el que está escrita. Se recomienda revisar el
directorio ``source`` para ver ejemplos de uso y patrones de
estructuración.

****************
Agradecimientos
****************

Se agradece especialmente al equipo de
`Read the Docs <http://readthedocs.org>`_ por proporcionar la
infraestructura que permite la construcción y distribución automatizada
de esta documentación.

*****************
Cómo contribuir
*****************

¿Te interesa contribuir al proyecto o a la adaptación en español?

* Revisa primero la estructura del repositorio y los archivos bajo
  ``source/``.
* Abre un issue o un pull request en el repositorio público.
* Para contactar con la persona autora original, visita
  `https://ianreppel.org <https://ianreppel.org>`_.

Las contribuciones que mejoran la claridad del contenido, corrigen
errores o actualizan enlaces serán especialmente bienvenidas.