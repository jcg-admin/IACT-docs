.. meta::
 :artefacto: Index_Plantillas
 :tipo: Indice
 :dominio: normativa
 :subdominio: estandares/plantillas
 :estado: Aprobado
 :version: 2.0.0
 :fecha_creacion: 2026-01-07
 :ultimo_cambio: 2026-04-28
 :autor: Equipo IACT
 :clasificacion: Interno

.. _index-plantillas:

================
Plantillas (TPL)
================

Descripción
===========

Este subdominio contiene las **plantillas estándar** del proyecto
IACT. Cada plantilla define la estructura obligatoria para crear
artefactos de documentación consistentes y trazables.

Naming
======

Per :ref:`std-007` §4.1, las plantillas siguen el patrón:

::

 TPL_<KEY>_<Descripcion_PascalCase>.rst

La versión vive en el metadata YAML del archivo, **no** en el
filename (per :ref:`std-006`).

----

Plantillas por categoría
========================

.. toctree::
 :maxdepth: 1
 :caption: Spec — Requisitos

 TPL_BReq_Objetivos_Negocio
 TPL_BR_Business_Rules
 TPL_BR_Decision_Tipo
 TPL_FR_Requisitos_Funcionales
 TPL_FR_Documentacion_10_Componentes
 TPL_FR_Query_SQL
 TPL_FR_Validacion_Reglas
 TPL_NFR_No_Funcionales

.. toctree::
 :maxdepth: 1
 :caption: Casos de Uso (7 patrones)

 TPL_UC_Casos_de_Uso
 TPL_UC_Construccion_7_Pasos
 TPL_UC_Actor_Secundario
 TPL_UC_CRUD_Operaciones
 TPL_UC_Larman_Contratos
 TPL_UC_Stakeholder_Driven
 TPL_UC_Temporal_Schedulers
 TPL_UC_UI_Driven

.. toctree::
 :maxdepth: 1
 :caption: Spec — Trazabilidad

 TPL_TRZ_Matriz_RTM

.. toctree::
 :maxdepth: 1
 :caption: Arquitectura técnica

 TPL_ADR_Decisiones_Arquitectonicas
 TPL_API_Documentacion_API
 TPL_CNST_Restricciones
 TPL_FD_Flujos_Datos
 TPL_MOD_Modulos
 TPL_VIEW_Vistas_Arquitectonicas

.. toctree::
 :maxdepth: 1
 :caption: Gobernanza

 TPL_INDEX_Indices
 TPL_POL_Politicas
 TPL_PROC_Procedimientos
 TPL_STD_Estandares
 TPL_TST_Pruebas

----

Uso de plantillas
=================

1. Identificar el tipo de artefacto a crear y elegir la plantilla
   correspondiente.
2. Para casos de uso, elegir el patrón apropiado entre las 7
   variantes disponibles según el tipo de UC (CRUD, Larman,
   Stakeholder_Driven, etc.).
3. Copiar la sección "Plantilla" del archivo TPL al nuevo
   artefacto.
4. Reemplazar los placeholders.
5. Aplicar :ref:`std-007` al filename del nuevo archivo.
6. Aplicar :ref:`std-006` para versionado en metadata.
7. Validar con ``make html`` (sin warnings).

----

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **STD relacionado**
   - :ref:`std-002` (Nomenclatura del Proyecto),
     :ref:`std-007` (Convención de Naming).
 * - **Ubicación canónica**
   - ``source/normativa/estandares/plantillas/``.

----

Historial
=========

.. list-table::
 :header-rows: 1
 :widths: 12 15 73

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-01-07
   - Versión inicial con 17 plantillas (priorización P0-P3,
     versiones en filenames).
 * - 2.0.0
   - 2026-04-28
   - **Bump MAJOR.** Reorganización por categoría (Spec /
     Casos de Uso / Trazabilidad / Arquitectura / Gobernanza).
     Renombrado de los 17 archivos legacy: removida la versión
     del filename, mantenida en metadata YAML
     (per :ref:`std-006`). Incorporadas 12 plantillas
     adicionales del set curado v1.3.0 / v1.2.0 (las 7
     variantes UC distintas + 3 variantes FR + TPL_TRZ +
     TPL_BR_Decision_Tipo). Eliminados 2 archivos obsoletos:
     ``TPL_002_Plantilla_UC_v2.rst`` (naming irregular) y
     ``TPL_RTM_Trazabilidad_1_0_0.rst`` (fusión con
     ``TPL_TRZ_Matriz_RTM``). **Total final: 28 plantillas.**
