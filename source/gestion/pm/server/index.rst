.. meta::
   :artefacto: INDEX-PM-SERVER
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm-server
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-server:

==================================
Gestion del submodulo ``server``
==================================

.. warning::

   Submodulo en bootstrap. Las secciones marcadas ``Pendiente``
   se completan a medida que el trabajo se acumula. Ver criterios
   de madurez en
   :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.

Proposito
=========

Gestion vertical del submodulo ``server``: infraestructura,
despliegue, runbooks operativos, observabilidad y respuesta a
incidentes.

Alcance
=======

Entra
-----

- Stack Ubuntu + Apache + mod_wsgi (CNST-021).
- Estructura de directorios en servidor (CNST-022).
- Estrategia de despliegue y rollback (CNST-023).
- Logs estructurados (CNST-024) y auditoria inmutable (CNST-025).
- Runbooks operativos.

No entra
--------

- Codigo de aplicacion (ver
  :doc:`/gestion/pm/api/index` y
  :doc:`/gestion/pm/ui/index`).
- Esquema y migraciones (ver :doc:`/gestion/pm/db/index`).

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

- MTTR ante incidentes en produccion.
- Porcentaje de releases con rollback documentado y ensayado
  (objetivo: 100% — CNST-023).
- p95 de latencia extremo a extremo respecto a SLA (CNST-017).

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Restricciones aplicables**
     - CNST-021, CNST-022, CNST-023, CNST-024, CNST-025
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice padre**
     - :doc:`/gestion/pm/index`
