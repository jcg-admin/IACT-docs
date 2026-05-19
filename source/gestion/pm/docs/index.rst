.. meta::
   :artefacto: INDEX-PM-DOCS
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm-docs
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-docs:

================================
Gestion del submodulo ``docs``
================================

.. warning::

   Submodulo en bootstrap. Las secciones marcadas ``Pendiente``
   se completan a medida que el trabajo se acumula. Ver criterios
   de madurez en
   :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.

Proposito
=========

Gestion vertical del submodulo ``docs`` (este repositorio
``IACT-docs``): corpus Sphinx + reStructuredText, normativa,
ADRs, modelos de dominio y documentos vivos del proyecto.

Alcance
=======

Entra
-----

- Estructura del corpus en ``source/``.
- Build Sphinx, extensiones, theme.
- Normativa (estandares, procedimientos, restricciones,
  gobernanza).
- Politica de cero warnings y trazabilidad de cambios.
- Saneamientos masivos del corpus.

No entra
--------

- Implementacion de API / BD / UI / Server (los otros
  submodulos).

Roadmap
=======

Pendiente.

Iniciativas activas
===================

Sin entradas. Pendiente.

Decisiones recientes
====================

Sin entradas. Pendiente.

Riesgos abiertos
================

Sin entradas. Pendiente.

Indicadores
===========

Pendiente. Candidatos a definir baseline:

- ``make html`` warnings/errors (objetivo: 0/0/0).
- Cobertura del corpus contra el catalogo de
  artefactos esperados.
- Numero de referencias rotas detectadas en
  validacion.

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Estandar de documentacion**
     - :doc:`/normativa/estandares/std-009-profesional-documentacion`
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice padre**
     - :doc:`/gestion/pm/index`
