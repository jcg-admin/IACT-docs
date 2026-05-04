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
=====================================

El ETL no usa Django ORM para persistir ejecuciones. El estado
se almacena directamente en la tabla ``etl_runs`` de Almacen de Datos,
accedida via ``cursor.execute`` / ``cursor.callproc``.

**DSC_MOD_005_etl_runs** — Tabla de registro de ejecuciones

.. code-block:: sql

 -- Tabla etl_runs en Almacen de Datos (no Django ORM)
 CREATE TABLE etl_runs (
     id            INT AUTO_INCREMENT PRIMARY KEY,
     job_id        VARCHAR(50) UNIQUE NOT NULL,
     started_at    DATETIME NOT NULL,
     finished_at   DATETIME NULL,
     estado        ENUM('en_ejecucion','exitoso','fallido') NOT NULL,
     registros_extraidos   INT DEFAULT 0,
     registros_cargados    INT DEFAULT 0,
     error_mensaje TEXT NULL,
     fecha_inicio  DATE NOT NULL,
     fecha_fin     DATE NOT NULL
 );

**ETLEjecucionRepo** — Repositorio Python sobre cursor

.. code-block:: python

 from django.db import connections

 class ETLEjecucionRepo:
     def listar(self, limit=50):
         with connections['mariadb'].cursor() as cursor:
             cursor.execute(
                 "SELECT * FROM etl_runs ORDER BY started_at DESC LIMIT %s",
                 [limit]
             )
             return cursor.fetchall()

     def historial(self, job_id):
         with connections['mariadb'].cursor() as cursor:
             cursor.callproc('sp_etl_historico', [job_id])
             return cursor.fetchall()

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
