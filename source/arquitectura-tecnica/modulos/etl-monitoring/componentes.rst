.. _arq-mod-004-componentes:

================================================
ARQ_MOD_004 — Componentes Tecnicos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Componentes de Aplicacion
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripcion
 * - apps.etl
   - DisparadorETL (management command), ETLEjecucionRepo,
     vistas de supervision via cursor sobre etl_runs
 * - apps.monitoring
   - Consultas directas a etl_runs; metricas de calidad de datos

----

Acceso a Datos — etl_runs (Almacen de Datos)
============================================

El ETL no usa el ORM del backend para persistir ejecuciones. El estado
se almacena directamente en la tabla ``etl_runs`` de Almacen de Datos,
accedida via ``cursor.execute`` / ``cursor.callproc``.

**DSC_MOD_005_etl_runs** — Tabla de registro de ejecuciones

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
**ETLEjecucionRepo** — Repositorio Python sobre cursor

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
----

APIs Expuestas
==============

**API_004_ETL_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/etl/executions
   - Listar filas de etl_runs
 * - GET
   - /api/v1/etl/executions/{id}
   - Detalle de ejecucion en etl_runs
 * - GET
   - /api/v1/etl/availability
   - Disponibilidad de datos (base_ivr_*)
 * - POST
   - /api/v1/etl/retry/{id}
   - Disparar reintento via DisparadorETL
