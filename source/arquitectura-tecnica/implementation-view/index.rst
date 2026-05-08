.. meta::
 :artefacto: INDEX_AT_IMPLEMENTATIONVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 3.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-implementationview-index:

=============================================
Implementation View — Vista de Implementacion
=============================================

Componentes y paquetes de codigo del sistema IACT por modulo
funcional. Cada modulo muestra el diagrama canonico:
``<<api>>``, ``<<serializer>>``, ``<<service>>``,
``<<repository>>``, ``<<orm>>``, mas la base de datos, con
los nombres de clases y servicios del codigo fuente y las
restricciones de acceso a datos aplicables (CNST-007,
CNST-025, CNST-031).

Granularidad: una caja modular por cada modulo funcional
in-scope, con su panorama y su diagrama de estructura de
capas.

.. note::

 **Scope de implementacion:** los modulos MOD_Operator,
 MOD_Supervision y MOD_Caller estan documentados en
 ``use-case-view/`` como vista de requisitos pero **NO entran
 en este ImplementationView modular**. Su contenido se
 preserva como referencia en archivos planos
 (``impl-operator.rst``, ``impl-supervision.rst``,
 ``impl-caller.rst``) hasta que se decida implementarlos.

.. note::

 **Reorganizacion v3.0.0 (2026-05-08):** los archivos planos
 ``impl-X.rst`` migraron a directorios por modulo
 (``access/``, ``admin/``, ``alerts/``, ``audit/``, ``auth/``,
 ``logs/``, ``permissions/``, ``pipeline/``, ``reports/``,
 ``users/``), siguiendo la convencion validada en
 ``use-case-view/`` y ``design-view/``. Cada modulo gana su
 ``index.rst`` (caja del modulo) con vista panoramica
 curated y toctree a ``layer-structure.rst`` (estructura de
 capas). Naming basado en contenido (``layer-structure``)
 no en tipo de diagrama (no ``components``).

----

Modulos del ImplementationView
===============================

Diez modulos en scope de implementacion. Cada modulo es una
caja autonoma con su panorama de capas y el diagrama de
estructura de capas con nombres reales de codigo fuente.

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

Modulos out-of-scope (preservados como referencia)
====================================================

Estos archivos se preservan flat hasta que se decida
implementarlos. NO entran en el modular ni en la cadena de
dependencias DesignView → ImplementationView del corpus.

.. toctree::
 :maxdepth: 1
 :caption: Out-of-scope (referencia historica)

 impl-caller
 impl-operator
 impl-supervision

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/index` —
   vocabulario canonico de las clases del sistema.
 - :doc:`/arquitectura-tecnica/use-case-view/index` —
   UCs por modulo (vista de requisitos).
 - :doc:`/arquitectura-tecnica/design-view/index` —
   estructura de diseño por modulo.
 - :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/relaciones-dependencia-iact`
   — DAG de dependencias entre vistas arquitectonicas.
