.. meta::
 :artefacto: INDEX_AT_DESIGNVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 4.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-designview-index:

=====================================
Design View — Vista de Diseno
=====================================

**Vista Logica (Kruchten 4+1) / Functional + Information
(Rozanski)** del sistema IACT. Materializa los UCs en scope
de implementacion en una representacion de diseno: paquetes
(modulos), interacciones (secuencias), flujos cross-modulo
(actividades) y ciclos de vida (estados).

NO duplica las definiciones del domain-model — los class
diagrams referencian las clases canonicas via ``:doc:``.

.. note::

 **Scope de implementacion:** los modulos MOD_Operator,
 MOD_Supervision y MOD_Caller estan documentados en
 ``use-case-view/`` como vista de requisitos pero **NO entran
 en este DesignView**. Su construccion queda diferida a WP
 futuros si/cuando se decida implementarlos.

.. note::

 **Reorganizacion v4.0.0 (2026-05-08):** los archivos planos
 ``class-X.rst``, ``seq-X.rst``, ``state-Y.rst`` y
 ``act-Z.rst`` migraron a directorios por modulo
 (``access/``, ``admin/``, ``alerts/``, ``audit/``, ``auth/``,
 ``logs/``, ``permissions/``, ``pipeline/``, ``reports/``,
 ``users/``), siguiendo la convencion ya establecida en
 ``use-case-view/``. Cada modulo gana su ``index.rst``
 (caja Kruchten) con vista panoramica curated y toctree a
 sub-vistas (class, sequence, state, activity).

Tipos de diagramas
==================

.. list-table::
 :header-rows: 1
 :widths: 25 15 60

 * - Tipo
   - UML lesson
   - Proposito
 * - Module box (caja)
   - uml-04 + uml-07
   - Vista panoramica del modulo: entidades centrales y
     puntos de contacto inter-modulo. Punto de entrada.
 * - Package overview
   - uml-04
   - Vista global de modulos y dependencias inter-modulo.
 * - Class per modulo
   - uml-03 + uml-04 + uml-05
   - Estructura cohesiva del bounded context (con
     repositories y servicios internos).
 * - Sequence per modulo
   - uml-09
   - Patron de interaccion canonico del modulo.
 * - Activity (flujos)
   - uml-11
   - Flujos de proceso cross-modulo con decisiones.
 * - State (entidades)
   - uml-08
   - Ciclos de vida con eventos y transiciones.

----

Vista global
============

.. toctree::
 :maxdepth: 1
 :caption: Overview

 package-overview

----

Modulos del DesignView
=======================

Diez modulos en scope de implementacion. Cada modulo es
una caja autonoma con su panorama, class diagram, sequence
canonica, y opcionalmente state machine y activity flow.

.. toctree::
 :maxdepth: 2
 :caption: Modulos (cajas por modulo)

 access/index
 admin/index
 alerts/index
 audit/index
 auth/index
 logs/index
 permissions/index
 pipeline/index
 reports/index
 users/index

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/index` — vocabulario
   canonico de las clases del sistema.
 - :doc:`/arquitectura-tecnica/use-case-view/index` — UCs por
   modulo (incluyendo los out-of-scope para implementacion).
 - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/index`
   — guia interna de seleccion de tipo de diagrama UML.
