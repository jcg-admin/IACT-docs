.. meta::
 :artefacto: INDEX_AT_DESIGNVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 3.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-06
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

Tipos de diagramas
==================

.. list-table::
 :header-rows: 1
 :widths: 25 15 60

 * - Tipo
   - UML lesson
   - Proposito
 * - Package overview
   - uml-04
   - Vista global de modulos y dependencias inter-modulo.
 * - Class per modulo
   - uml-03 + uml-04 + uml-05
   - Estructura cohesiva del bounded context.
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

Modulos (cajas por modulo)
==========================

.. toctree::
 :maxdepth: 2
 :caption: Modulos del DesignView

 access/index

----

Class diagrams (estructura por modulo)
=======================================

.. toctree::
 :maxdepth: 1
 :caption: Estructura de clases por modulo

 class-auth
 class-users
 class-permissions
 class-admin
 class-audit
 class-pipeline
 class-reports
 class-alerts
 class-logs

----

Sequence diagrams (patrones de interaccion)
============================================

.. toctree::
 :maxdepth: 1
 :caption: Patrones de interaccion canonicos

 seq-auth
 seq-users
 seq-permissions
 seq-admin
 seq-audit
 seq-pipeline
 seq-reports
 seq-alerts
 seq-logs

----

Activity diagrams (flujos cross-modulo)
========================================

.. toctree::
 :maxdepth: 1
 :caption: Flujos de proceso

 act-rbac-effective-set-eval
 act-jwt-auth
 act-etl-pipeline-execution
 act-alert-evaluation
 act-export-async

----

State diagrams (ciclos de vida)
================================

.. toctree::
 :maxdepth: 1
 :caption: Ciclos de vida de entidades

 state-session
 state-pipeline-execution
 state-alert-event
 state-export-job

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/index` — vocabulario
   canonico de las 85 clases del sistema.
 - :doc:`/arquitectura-tecnica/use-case-view/index` — UCs por
   modulo (incluyendo los out-of-scope para implementacion).
 - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/index`
   — guia interna de seleccion de tipo de diagrama UML.
