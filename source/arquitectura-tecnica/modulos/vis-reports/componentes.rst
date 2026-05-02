.. _arq-mod-005-componentes:

================================================
ARQ_MOD_005 — Componentes Tecnicos
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
 * - apps.analytics
   - Modelos de metricas, repositorios de consulta
 * - apps.reports
   - Vistas y serializadores de reportes
 * - apps.exports
   - Servicios de generacion CSV/Excel/PDF

----

Modelos de Datos
================

**DSC_MOD_006_DailyMetrics** — Metricas diarias agregadas

.. code-block:: python

 class DailyMetrics(models.Model):
     date = models.DateField
     center_code = models.CharField(max_length=50)
     service_code = models.CharField(max_length=50)
     total_calls = models.IntegerField
     avg_duration = models.DecimalField
     successful_calls = models.IntegerField
     failed_calls = models.IntegerField
     transfers = models.IntegerField

     class Meta:
         unique_together = ['date', 'center_code', 'service_code']

----

APIs Expuestas
==============

**API_005_Dashboard_Endpoints** · **API_006_Reports_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/dashboard
   - Dashboard principal
 * - GET
   - /api/v1/dashboard/widgets
   - Widgets disponibles
 * - GET
   - /api/v1/reports/quarterly
   - Reporte trimestral
 * - GET
   - /api/v1/reports/errors
   - Reporte de errores
 * - GET
   - /api/v1/reports/transfers
   - Reporte transferencias
 * - POST
   - /api/v1/exports/csv
   - Exportar CSV
 * - POST
   - /api/v1/exports/excel
   - Exportar Excel
 * - POST
   - /api/v1/exports/pdf
   - Exportar PDF
