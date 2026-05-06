.. meta::
 :artefacto: INDEX_AT_DESIGNVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 3.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-designview-index:

=====================================
Design View — Vista de Diseno
=====================================

**Vista Logica (Kruchten 4+1) / Functional + Information
(Rozanski)** del sistema IACT. Materializa los UCs ya
documentados en una representacion de diseno: paquetes
(modulos), interacciones (secuencias), flujos cross-modulo
(actividades) y ciclos de vida (estados).

NO duplica las definiciones del domain-model — los class
diagrams referencian las clases canonicas via ``:doc:``.

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

Class diagrams (estructura por modulo)
=======================================

.. toctree::
 :maxdepth: 1
 :caption: Estructura de clases por modulo

 class-auth
 class-users
 class-access
 class-permissions
 class-admin
 class-audit
 class-caller
 class-operator
 class-supervision
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
 seq-access
 seq-permissions
 seq-admin
 seq-audit
 seq-caller
 seq-operator
 seq-supervision
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
 act-sod-check
 act-etl-pipeline-execution
 act-alert-evaluation
 act-export-async

----

State diagrams (ciclos de vida)
================================

.. toctree::
 :maxdepth: 1
 :caption: Ciclos de vida de entidades

 state-call
 state-session
 state-assignment
 state-pipeline-execution
 state-alert-event
 state-export-job

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/index` — vocabulario
   canonico de las 85 clases del sistema.
 - :doc:`/arquitectura-tecnica/use-case-view/index` — UCs por
   modulo que motivan esta vista.
 - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama/index`
   — guia interna de seleccion de tipo de diagrama UML.
