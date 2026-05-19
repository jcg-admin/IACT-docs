.. meta::
   :artefacto: INDEX-PM-API
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm-api
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-api:

================================
Gestion del submodulo ``api``
================================

.. warning::

   Submodulo en bootstrap. Las secciones marcadas ``Pendiente``
   se completan a medida que el trabajo se acumula. Ver criterios
   de madurez en
   :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`.

Proposito
=========

Gestion vertical del submodulo ``api`` (capa de servicios REST
Django + DRF): roadmap tecnico, iniciativas con impacto en la
capa de API, decisiones arquitectonicas vigentes, riesgos
abiertos e indicadores.

Alcance
=======

Entra
-----

- Endpoints DRF (URLs, verbos, contratos de request/response).
- Versionado y politica de deprecacion de la API.
- Permisos y throttling al nivel de vista.
- Contratos de error y mapeo HTTP.
- Trazabilidad UC ↔ endpoint.

No entra
--------

- Esquema de base de datos (ver :doc:`/gestion/pm/db/index`).
- Despliegue y observabilidad de runtime (ver
  :doc:`/gestion/pm/server/index`).
- Frontend (ver :doc:`/gestion/pm/ui/index`).

Roadmap
=======

Pendiente. Registrar aqui hitos versionados del submodulo o link
al tablero externo donde se gestiona.

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

- Cobertura de tests por endpoint.
- p95 de latencia por endpoint en runtime.
- Numero de endpoints sin permission class explicita
  (objetivo: 0 — ver CNST-010).

Trazabilidad
============

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-014-gestion-por-submodulo`
   * - **Iniciativas globales**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Naming**
     - :doc:`/normativa/estandares/std-007-convencion-naming`
   * - **Indice padre**
     - :doc:`/gestion/pm/index`
