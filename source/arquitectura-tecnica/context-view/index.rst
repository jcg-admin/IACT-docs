.. meta::
 :artefacto: INDEX_AT_CONTEXT_VIEW
 :tipo: Indice — Context Viewpoint
 :dominio: arquitectura_tecnica
 :subdominio: ContextView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-context-view-index:

==================================
Context View — Vista de Contexto
==================================

Viewpoint Context del sistema IACT segun el framework de Rozanski & Woods.
Describe las relaciones, dependencias e interacciones entre el sistema IACT
y su entorno: las personas, sistemas y entidades externas con las que interactua.

Esta vista es el viewpoint **overarching**: informa el scope y el contenido
de todas las demas vistas arquitectonicas (Functional, Information, Concurrency,
Development, Deployment, Operational).

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Documento
   - Descripcion
 * - :doc:`context-diagram`
   - Diagrama de contexto del sistema: frontera del sistema, entidades
     externas e interacciones. Incluye DFD nivel 0 y diagrama de
     componentes de contexto.
 * - :doc:`external-interfaces`
   - Definicion de las interfaces externas: Sistema IVR (BD Operativa),
     APScheduler y restricciones de integracion (P-01, CNST-007).
 * - :doc:`stakeholders`
   - Mapa de stakeholders: grupos RBAC, instituciones adquirentes
     y sus concerns arquitectonicos.

.. toctree::
 :maxdepth: 1
 :caption: Context View

 context-diagram
 external-interfaces
 stakeholders

----

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/vistas-y-viewpoints`
