.. meta::
 :artefacto: INDEX_BUSINESS_REQUIREMENTS
 :tipo: Indice
 :dominio: requisitos
 :subdominio: business-requirements
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==============================
Business Requirements (BReq)
==============================

Esta sección contiene los **Business Requirements (BReq)** del
proyecto IACT — el nivel **más alto** (nivel 1 de 5) de la
jerarquía de requisitos canónica del proyecto.

Per :doc:`/normativa/gobernanza/adr-gob-003-jerarquia-requerimientos-5-niveles`,
los BReq representan **objetivos de negocio de alto nivel** que
el sistema debe satisfacer.

Diferencia BReq vs BR
=====================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Tipo
   - Descripción
 * - **BReq** (este cajón)
   - Objetivo de negocio nivel 1. Abstracto. Deriva en BR + UC.
 * - **BR** (Business Rule)
   - Regla operativa nivel 2. Concreta. Vive en
     :doc:`/requisitos/reglas-negocio/index`.

Catálogo de BReq
================

.. toctree::
 :maxdepth: 1

 breq-001-visibilidad-metricas

Convención
==========

Naming: `breq-NNN-{descripcion-kebab}.rst` per
:doc:`/normativa/estandares/std-007-convencion-naming`.

Plantilla aplicable:
:doc:`/normativa/estandares/plantillas/tpl-breq-objetivos-negocio`.

Skill guía: ``ba-elicitation`` (BABOK).

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ADR origen**
   - :doc:`/normativa/gobernanza/adr-gob-003-jerarquia-requerimientos-5-niveles`
 * - **Nivel jerárquico**
   - 1 (más alto)
 * - **Deriva en**
   - BR (reglas-negocio/), UC (casos-uso/), FR (requisitos-funcionales/)
