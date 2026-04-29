.. IACT - Sistema de Dashboard Analytics — documentación raíz

=====================================
IACT — Sistema de Dashboard Analytics
=====================================

.. image:: _static/img/logo.svg
   :alt: IACT Logo
   :align: center
   :width: 200px

----

Bienvenido a la Documentación del Proyecto IACT
===============================================

El proyecto IACT es una solución de **Dashboard Analytics** que conecta
datos operativos (origen MySQL, modo solo-lectura) con necesidades de
análisis de negocio (destino PostgreSQL, optimizado) mediante un proceso
ETL trazable. El frontend (React + Webpack) consume la API REST del
backend (Django REST Framework) servido por Apache + mod_wsgi sobre
Ubuntu.

Stack del producto
==================

================ ========================================================
Capa             Tecnología
================ ========================================================
Frontend         React + Webpack
Backend          Django REST Framework (Python 3.11+)
Infraestructura  Ubuntu + Apache (mod_wsgi)
Bases de datos   MySQL (operativa, RO) + PostgreSQL (analítica)
================ ========================================================

Estado de la documentación
==========================

.. note::

   La documentación del producto IACT está organizada en tres
   capas ortogonales (ver :doc:`base_cognitiva/_metadata/META_05_Estructura_Documental`):

   - **Capa 1 — Methodology / Governance:** standards, plantillas,
     procedimientos, restricciones, ADRs internos.
   - **Capa 2 — Product spec + Tech implementation:** UCs, FRs,
     NFRs, BRs + arquitectura + cajones por tier técnico.
   - **Capa 3 — Project lifecycle:** charter, roadmap, OKRs,
     épicas, releases, retrospectives, team.

   La estructura se construye de forma **incremental dominio por
   dominio**. Los cajones aparecen en la navegación cuando su
   contenido inicial está disponible.

Contenido publicado
===================

.. toctree::
   :maxdepth: 2
   :caption: Base Cognitiva

   base_cognitiva/index

.. toctree::
   :maxdepth: 2
   :caption: Normativa

   normativa/index

.. toctree::
   :maxdepth: 2
   :caption: Requisitos

   requisitos/index

----

Índices y Búsqueda
==================

* :ref:`genindex`
* :ref:`search`
