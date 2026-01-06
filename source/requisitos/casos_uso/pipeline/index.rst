.. meta::
   :artefacto: index_pipeline
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :estado: En Desarrollo
   :version: 2.0.0

.. _casos-uso-pipeline-index:

==============================================================================
MOD_Pipeline: Casos de Uso de Pipeline ETL
==============================================================================

Indice de Casos de Uso del modulo de Pipeline ETL.

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Pipeline
   * - **UC Planificados**
     - 4 (UC-050 a UC-053)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **BReq Origen**
     - BReq-001, BReq-005

----

Casos de Uso
------------

.. list-table::
   :widths: 15 40 20 25
   :header-rows: 1

   * - ID
     - Nombre
     - Complejidad
     - Estado
   * - UC-050
     - Supervisar Estado ETL
     - Media
     - Pendiente
   * - UC-051
     - Consultar Errores ETL
     - Baja
     - Pendiente
   * - UC-052
     - Consultar Disponibilidad Datos
     - Baja
     - Pendiente
   * - UC-053
     - Reiniciar Proceso ETL
     - Media
     - Pendiente

----

.. toctree::
   :maxdepth: 1
   :caption: Casos de Uso

   UC_050_Supervisar_ETL
   UC_051_Consultar_Errores_ETL
   UC_052_Consultar_Disponibilidad
   UC_053_Reiniciar_ETL
EOF

cat > /mnt/user-data/outputs/casos_uso_v2/reports/index.rst << 'EOF'
.. meta::
   :artefacto: index_reports
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :estado: En Desarrollo
   :version: 2.0.0

.. _casos-uso-reports-index:

==============================================================================
MOD_Reports: Casos de Uso de Reportes y Dashboard
==============================================================================

Indice de Casos de Uso del modulo de Reportes y Dashboard.

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Reports
   * - **UC Planificados**
     - 14 (UC-017 a UC-030)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **BReq Origen**
     - BReq-001, BReq-003

----

Casos de Uso - Reportes
-----------------------

.. list-table::
   :widths: 15 40 20 25
   :header-rows: 1

   * - ID
     - Nombre
     - Complejidad
     - Estado
   * - UC-017
     - Generar Reporte Predefinido
     - Media
     - Pendiente
   * - UC-018
     - Crear Reporte Personalizado
     - Alta
     - Pendiente
   * - UC-019
     - Programar Reporte Automatico
     - Media
     - Pendiente
   * - UC-020
     - Filtrar Reportes por Fecha
     - Baja
     - Pendiente
   * - UC-021
     - Filtrar Reportes por Centro
     - Baja
     - Pendiente
   * - UC-022
     - Exportar Reporte a CSV
     - Baja
     - Pendiente
   * - UC-023
     - Exportar Reporte a Excel
     - Media
     - Pendiente
   * - UC-024
     - Exportar Reporte a PDF
     - Media
     - Pendiente

----

Casos de Uso - Dashboard
------------------------

.. list-table::
   :widths: 15 40 20 25
   :header-rows: 1

   * - ID
     - Nombre
     - Complejidad
     - Estado
   * - UC-025
     - Visualizar Dashboard Operativo
     - Alta
     - Pendiente
   * - UC-026
     - Ver KPIs en Tiempo Real
     - Media
     - Pendiente
   * - UC-027
     - Analizar Tendencias
     - Media
     - Pendiente
   * - UC-028
     - Comparar Periodos
     - Media
     - Pendiente
   * - UC-029
     - Filtrar Dashboard por Centro
     - Baja
     - Pendiente
   * - UC-030
     - Exportar Vista Dashboard
     - Baja
     - Pendiente

----

.. toctree::
   :maxdepth: 1
   :caption: Casos de Uso

   UC_017_Generar_Reporte
   UC_018_Crear_Reporte_Personalizado
   UC_019_Programar_Reporte
   UC_020_Filtrar_Por_Fecha
   UC_021_Filtrar_Por_Centro
   UC_022_Exportar_CSV
   UC_023_Exportar_Excel
   UC_024_Exportar_PDF
   UC_025_Visualizar_Dashboard
   UC_026_Ver_KPIs
   UC_027_Analizar_Tendencias
   UC_028_Comparar_Periodos
   UC_029_Filtrar_Dashboard_Centro
   UC_030_Exportar_Dashboard
