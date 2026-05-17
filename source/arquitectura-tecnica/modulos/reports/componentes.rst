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
 * - ``apps.reports``
   - Vistas de API y serializadores de reportes IVR. Lee datos
     via ``cursor.callproc()`` sobre la conexion Almacen de Datos ``ivr``;
     no usa modelos ORM para datos IVR analiticos.
 * - ``apps.exports``
   - Servicios de generacion CSV/Excel/PDF sobre los datasets
     retornados por los SPs de reporte.

----

Patron de Consulta — cursor.callproc()
=======================================

Los datos de reportes IVR no provienen del ORM del backend.
Provienen de stored procedures en Almacen de Datos, invocados via el cursor
de la conexion ``ivr``:

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

Este patron se repite para cada uno de los 7 SPs de reporte.
Las vistas de API reciben el resultado como lista de diccionarios y
lo serializan directamente.

----

Stored Procedures de Reporte
==============================

Los SPs de reporte son de lectura exclusiva sobre ``base_ivr_detalle``
y ``base_ivr_clientes`` (tablas analiticas en Almacen de Datos). El parametro
principal de todos es ``quarter_name`` (ej: ``'Q3_25'``).

.. list-table::
 :widths: 45 55
 :header-rows: 1

 * - Stored Procedure
   - Datos que retorna
 * - ``sp_rpt_centros_transferencia(quarter)``
   - Llamadas por centro de transferencia y segmento
 * - ``sp_rpt_llamadas_abandonadas(quarter)``
   - Conteo y tasa de abandonos por segmento
 * - ``sp_rpt_menu_redirigidos(quarter)``
   - Llamadas por menu y resultado de redireccion
 * - ``sp_rpt_clientes(quarter)``
   - Dimension de clientes IVR del trimestre
 * - ``sp_rpt_centros_xsegmento(quarter)``
   - Distribucion de centros por segmento
 * - ``sp_rpt_menu_centro(quarter)``
   - Cruze menu x centro de transferencia
 * - ``sp_rpt_cMENU_ERROR(quarter)``
   - Registros con cMenu en estado de error

----

APIs Expuestas
==============

**API_005_Dashboard_Endpoints** ·**API_006_Reports_Endpoints**

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
   - Reporte trimestral (llama sp_rpt_centros_transferencia)
 * - GET
   - /api/v1/reports/abandoned
   - Reporte de abandonos (llama sp_rpt_llamadas_abandonadas)
 * - GET
   - /api/v1/reports/redirects
   - Reporte de redireccionados (llama sp_rpt_menu_redirigidos)
 * - GET
   - /api/v1/reports/errors
   - Reporte de errores de menu (llama sp_rpt_cMENU_ERROR)
 * - GET
   - /api/v1/reports/transfers
   - Reporte de transferencias por centro
 * - POST
   - /api/v1/exports/csv
   - Exportar CSV
 * - POST
   - /api/v1/exports/excel
   - Exportar Excel
 * - POST
   - /api/v1/exports/pdf
   - Exportar PDF
