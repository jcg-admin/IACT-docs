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
   - Modelos ETLExecution, vistas de supervision
 * - apps.monitoring
   - Metricas de calidad de datos

----

Modelos de Datos
================

**DSC_MOD_005_ETLExecution** — Registro de ejecuciones

.. code-block:: python

 class ETLExecution(models.Model):
     job_id = models.CharField(max_length=50, unique=True)
     started_at = models.DateTimeField
     finished_at = models.DateTimeField(null=True)
     status = models.CharField(choices=ETL_STATUS)  # RUNNING, SUCCESS, FAILED
     records_extracted = models.IntegerField(default=0)
     records_transformed = models.IntegerField(default=0)
     records_loaded = models.IntegerField(default=0)
     error_message = models.TextField(null=True)
     date_range_start = models.DateField
     date_range_end = models.DateField

 class DataAvailability(models.Model):
     period_type = models.CharField  # TRIMESTRE, MES, DIA
     period_value = models.CharField  # Q1-2024, 2024-01
     status = models.CharField  # COMPLETO, PARCIAL, FALTANTE
     record_count = models.IntegerField
     last_updated = models.DateTimeField

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
   - Listar ejecuciones
 * - GET
   - /api/v1/etl/executions/{id}
   - Detalle de ejecucion
 * - GET
   - /api/v1/etl/availability
   - Disponibilidad por periodo
 * - GET
   - /api/v1/etl/quality-issues
   - Incidencias de calidad
 * - POST
   - /api/v1/etl/retry/{id}
   - Reintentar procesamiento
