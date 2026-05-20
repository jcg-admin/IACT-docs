.. meta::
   :artefacto: INICIATIVA-INTEGRAR-DOCS-INTERNOS-MULTI-REPO
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: EN-CURSO
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T23:30:00
   :ultimo_cambio: 2026-05-19T23:30:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-integrar-docs-internos-multi-repo:

====================================================================
Iniciativa: Integrar docs/ internos de api/ui/db a IACT-docs
====================================================================

Origen
======

El sponsor identifico que ``IACT-api/docs/``, ``IACT-ui/docs/``
e ``IACT-db/docs/`` contienen 429 archivos markdown con
decisiones de arquitectura, ADRs, planes, hallazgos de
implementacion y conveciones que **no estan reflejados** en
``IACT-docs/source/*``. Esto rompe el principio de fuente unica:
las decisiones viven en el repo donde se ejecutaron, no en el
repo canonico de documentacion.

Inventario base (PROVEN, ``find -name '*.md' | wc -l``)
========================================================

* ``IACT-api/docs/`` — 87 archivos
* ``IACT-ui/docs/`` — 99 archivos
* ``IACT-db/docs/`` — 243 archivos
* **Total: 429**

Alcance
=======

Esta iniciativa NO integra los 429 archivos verbatim. La gran
mayoria son logs de hallazgos de fases (``HALLAZGOS-FASE-N-*.md``)
cuyo contenido **ya fue absorbido** en iniciativas COMPLETADAs
en ``IACT-docs/source/gestion/pm/iniciativas/``. Re-integrarlos
duplicaria informacion contradictoria.

Clasificacion (5 buckets):

1. **HALLAZGOS / WORK-LOG / BITACORA** — logs de sesion.
   **ARCHIVAR** en su repo, no promover.
2. **PLAN-IMPL / IMPLEMENTATION_PLAN** — planes superseded por
   iniciativas vigentes. **ARCHIVAR**.
3. **ADR / ARCHITECTURE / DESIGN / CONVENCIONES** — decisiones
   arquitectonicas vivas. **INTEGRAR** si no existe equivalente.
4. **SETUP / OPS / DEPLOYMENT / TROUBLESHOOTING** — guias
   operativas. **INTEGRAR** en ``source/operaciones/`` /
   ``arquitectura_tecnica/`` si falta.
5. **README / DOCS-INDEX** — entrypoints locales. **NO migrar**.

Decisiones del bucket 3 y 4 las determina el audit-clasificatorio
que se ejecuta como sub-task de esta iniciativa.

Politica de archivado (no es deuda oculta)
============================================

Los archivos del bucket 1 y 2 no se borran del repo origen
(I-002: git como persistencia). Permanecen en
``{repo}/docs/`` como historico de implementacion. Cada
``docs/`` debe tener un ``README.md`` indicando:

* "Este directorio contiene logs historicos de implementacion."
* "La documentacion canonica vive en IACT-docs/source/*."
* "Los archivos ``HALLAZGOS-*`` y ``PLAN-IMPL-*`` son
  archivales, no actualizados."

De esta forma el lector sabe explicitamente que la fuente
de verdad es IACT-docs y los docs locales son referencia
historica.

Fases
=====

FASE 1 — Inventario clasificatorio
   Agent Explore clasifica los 429 archivos en los 5 buckets.
   Reporta tabla compacta de los buckets 3-4 con decision
   INTEGRAR / YA_EXISTE / ARCHIVAR.

FASE 2 — Integrar bucket 3 (ADR / Arquitectura) sin equivalente
   Para cada archivo INTEGRAR del bucket 3, crear RST en
   ``source/arquitectura_tecnica/`` o
   ``source/normativa/decisiones/`` segun aplique, preservando
   contenido sustantivo y agregando metadata canonica.

FASE 3 — Integrar bucket 4 (SETUP / OPS) sin equivalente
   Para cada archivo INTEGRAR del bucket 4, crear RST en
   ``source/operaciones/`` o
   ``source/arquitectura_tecnica/despliegue/`` segun aplique.

FASE 4 — README archival por repo
   Crear ``docs/README.md`` (o actualizar) en cada repo con
   la politica de archivado explicita.

Criterio de cierre
==================

* Bucket 3 INTEGRAR: 100% reflejado en IACT-docs.
* Bucket 4 INTEGRAR: 100% reflejado en IACT-docs.
* Buckets 1-2: README archival declarado en cada repo.
* Sphinx build ``-W`` sin warnings nuevos.

Estado de progreso: ver
:doc:`progreso-integrar-docs-internos-multi-repo`.

.. toctree::
   :maxdepth: 1
   :hidden:

   progreso-integrar-docs-internos-multi-repo
