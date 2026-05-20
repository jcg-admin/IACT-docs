.. meta::
   :artefacto: PROGRESO-INTEGRAR-DOCS-INTERNOS-MULTI-REPO
   :tipo: Progreso
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-docs-internos-multi-repo
   :repo_objetivo: IACT-docs
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-20T00:00:00
   :ultimo_cambio: 2026-05-20T00:00:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _progreso-integrar-docs-internos-multi-repo:

================================================================
Progreso: Integrar docs internos multi-repo
================================================================

FASE 1 — Inventario clasificatorio (PROVEN)
=============================================

Agent Explore clasifico los 429 archivos en 5 buckets:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Bucket
     - Archivos
     - Decision
   * - 1 — HALLAZGOS / WORK-LOG / BITACORA
     - 20
     - ARCHIVAR
   * - 2 — PLAN-IMPL / IMPLEMENTATION_PLAN
     - 3
     - ARCHIVAR
   * - 3 — ADR / ARCHITECTURE / DESIGN
     - 7 evaluados
     - INTEGRAR (todos sin equivalente)
   * - 4 — SETUP / OPS / DEPLOYMENT / TROUBLESHOOTING
     - 11 evaluados
     - INTEGRAR (todos sin equivalente)
   * - 5 — README / DOCS-INDEX
     - ~386
     - MANTENER in-situ
   * - YA-EXISTEN
     - 2
     - NO-INTEGRAR (equivalente canonico ya presente)

FASE 2 — Portar bucket 3 (Arquitectura) — COMPLETADA
=====================================================

Portados (7 archivos):

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Origen
     - Destino
   * - ``IACT-ui/docs/ARCHITECTURE.md``
     - ``source/arquitectura-tecnica/frontend/architecture.rst``
   * - ``IACT-ui/docs/STATE_DESIGN.md``
     - ``source/arquitectura-tecnica/frontend/state-design.rst``
   * - ``IACT-db/docs/architecture/MAPEO-DID-SEGMENTOS.md``
     - ``source/arquitectura-tecnica/databases/mapeo-did-segmentos.rst``
   * - ``IACT-db/docs/architecture/NOMENCLATURA-TABLAS-BILINGUE.md``
     - ``source/arquitectura-tecnica/databases/nomenclatura-tablas-bilingue.rst``
   * - ``IACT-db/docs/architecture/ANALISIS-ARQUITECTURA-ETL.md``
     - ``source/arquitectura-tecnica/etl/analisis-arquitectura-etl.rst``
   * - ``IACT-db/docs/architecture/FLUJO-ETL-COMPLETO.md``
     - ``source/arquitectura-tecnica/etl/flujo-etl-completo.rst``
   * - ``IACT-db/docs/architecture/FLUJO-ETL-V2.md``
     - ``source/arquitectura-tecnica/etl/flujo-etl-v2.rst``

Cada RST:

* Preserva contenido verbatim del MD origen.
* Tiene bloque ``meta::`` canonico con ``:repo_origen:``.
* Tiene admonition de provenance referenciando el origen.
* Esta wired en ``source/arquitectura-tecnica/index.rst`` via
  toctree "Sub-arquitecturas por capa".

Fixes de conversion aplicados:

* Overlines de title corregidos en ``frontend/index.rst`` y
  ``databases/index.rst`` (longitud ``=`` >= titulo).
* Codeblock JavaScript suelto en ``state-design.rst`` lineas
  174-182 encapsulado en ``.. code-block:: javascript``.
* Campo Fuentes en ``flujo-etl-completo.rst`` separado de
  Fecha para no disparar "Unexpected indentation" en docutils.

FASE 3 — Portar bucket 4 (Setup / Ops) — COMPLETADA
======================================================

Portados (11 archivos): 8 a ``source/onboarding/`` y 3 a
``source/devops/runbooks/``. Wirings en index correspondientes
con captions "Setup por capa" y "Runbooks portados (multi-repo)".

FASE 4 — README archival por repo — COMPLETADA
================================================

Cada repo declaro la politica de archivado en su
``docs/README.md``:

* IACT-api: nuevo ``docs/README.md`` (no existia). Rama
  ``feature/declarar-docs-archival-policy``, commit ``7d9e659``.
* IACT-ui: preamble agregado al ``docs/README.md`` existente.
  Rama ``feature/declarar-docs-archival-policy``, commit
  ``6244ca6``.
* IACT-db: preamble agregado al ``docs/README.md`` existente.
  Rama ``feature/declarar-docs-archival-policy``, commit
  ``f751f78``.

Las 3 ramas estan empujadas a sus remotos respectivos.

Politica declarada explicita:

1. Documentacion canonica vive en ``IACT-docs/source/``.
2. Archivos ``HALLAZGOS-*``, ``PLAN-IMPL-*``, ``BITACORA-*``
   son historicos, no se actualizan.
3. Archivos portados a IACT-docs se preservan in-situ pero la
   version canonica vive en IACT-docs.
4. Nueva documentacion va directamente a IACT-docs/source/.

Sin esta declaracion, el repo origen seria deuda oculta:
contenido obsoleto que podria interpretarse como vigente.

Estado de cierre
================

* Bucket 3 INTEGRAR: 7/7 portados.
* Bucket 4 INTEGRAR: 11/11 portados.
* Bucket 1-2: politica declarada en 3 repos.
* Sphinx build ``-W``: validacion pendiente (build local lento
  por PlantUML; los archivos creados pasan parsing docutils sin
  warnings tras los fixes aplicados).

Pendiente operativo: merge de los 4 PRs (1 docs + 3 repos
archival) cuando el sponsor lo confirme.
