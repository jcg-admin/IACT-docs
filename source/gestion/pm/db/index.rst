.. meta::
   :artefacto: INDEX-PM-DB
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm-db
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-db:

==============================
Gestion del submodulo ``db``
==============================

.. warning::

   Submodulo en bootstrap. Las secciones marcadas ``Pendiente``
   se completan a medida que el trabajo se acumula. Ver criterios
   de madurez en
   :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.

Proposito
=========

Gestion vertical del submodulo ``db``: esquema relacional,
migraciones, seeds, ETL IVR → operacional, politicas de
retencion, ownership de tablas y dominio de datos.

Alcance
=======

Entra
-----

- Esquema y migraciones (Django ORM).
- Arquitectura de bases de datos dual (CNST-006) y ETL
  (CNST-008).
- Politicas de retencion y purga.
- Indices, particionado y planes de capacidad.
- Datos sensibles: clasificacion (CNST-027) y cifrado (CNST-028).

No entra
--------

- Contratos REST que consumen el modelo (ver
  :doc:`/gestion/pm/api/index`).
- Infraestructura de hosting de la BD (ver
  :doc:`/gestion/pm/server/index`).

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

- Numero de migraciones sin rollback documentado.
- Tamanio de la ventana ETL respecto a la ventana objetivo
  (CNST-008: 6 a 12 horas).
- Porcentaje de campos clasificados (CNST-027).

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Restricciones aplicables**
     - CNST-006, CNST-007, CNST-008, CNST-027, CNST-028
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice padre**
     - :doc:`/gestion/pm/index`
