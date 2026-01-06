.. meta::
   :artefacto: index_reports
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :estado: Completado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _casos-uso-reports-index:

==============================================================================
MOD_Reports: Casos de Uso de Reportes y Dashboard
==============================================================================

Modulo de Reportes y Dashboard - Version 2.0 con diagramas PlantUML.

.. contents:: Contenido
   :local:
   :depth: 2

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Reports
   * - **UC Documentados**
     - 14 (UC-017 a UC-030)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **Estado**
     - Completado
   * - **BReq Origen**
     - BReq-002 (Reportes), BReq-003 (Dashboard)
   * - **BR Aplicables**
     - BR_008, BR_009, BR_011-BR_019

----

Reportes Contables (UC-017 a UC-025)
------------------------------------

.. list-table::
   :widths: 12 40 15 15 18
   :header-rows: 1

   * - ID
     - Nombre
     - Complej.
     - Diag.
     - Funcion
   * - UC-017
     - Reporte Saldos por Cuenta
     - Media
     - 3
     - RPT-001
   * - UC-018
     - Reporte de Movimientos
     - Media
     - 3
     - RPT-002
   * - UC-019
     - Balance General
     - Alta
     - 3
     - RPT-003
   * - UC-020
     - Estado de Resultados
     - Alta
     - 3
     - RPT-004
   * - UC-021
     - Flujo de Efectivo
     - Alta
     - 3
     - RPT-005
   * - UC-022
     - Analisis de Cuentas
     - Media
     - 3
     - RPT-006
   * - UC-023
     - Comparativo Periodos
     - Media
     - 3
     - RPT-007
   * - UC-024
     - Presupuesto vs Real
     - Alta
     - 3
     - RPT-008
   * - UC-025
     - Antiguedad de Saldos
     - Media
     - 3
     - RPT-009

----

Dashboard (UC-026 a UC-030)
---------------------------

.. list-table::
   :widths: 12 40 15 15 18
   :header-rows: 1

   * - ID
     - Nombre
     - Complej.
     - Diag.
     - Funcion
   * - UC-026
     - Dashboard Principal
     - Media
     - 3
     - DSH-001
   * - UC-027
     - Dashboard Financiero
     - Media
     - 3
     - DSH-002
   * - UC-028
     - Dashboard Operativo
     - Media
     - 3
     - DSH-003
   * - UC-029
     - Personalizar Dashboard
     - Media
     - 3
     - DSH-004
   * - UC-030
     - Exportar Dashboard
     - Baja
     - 3
     - DSH-005

----

Metricas
--------

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Metrica
     - Valor
     - Notas
   * - UC Documentados
     - 14
     - 9 Reportes + 5 Dashboard
   * - FR Derivados
     - ~130
     - ~9 por UC
   * - Diagramas PlantUML
     - 42
     - 3 por UC
   * - Lineas documentacion
     - ~5,400
     - Total modulo

----

Funciones RBAC: Reportes
------------------------

.. list-table::
   :widths: 12 40 48
   :header-rows: 1

   * - Codigo
     - Nombre
     - UC
   * - RPT-001
     - Reporte Saldos
     - UC-017
   * - RPT-002
     - Reporte Movimientos
     - UC-018
   * - RPT-003
     - Balance General
     - UC-019
   * - RPT-004
     - Estado Resultados
     - UC-020
   * - RPT-005
     - Flujo Efectivo
     - UC-021
   * - RPT-006
     - Analisis Cuentas
     - UC-022
   * - RPT-007
     - Comparativo
     - UC-023
   * - RPT-008
     - Presupuesto vs Real
     - UC-024
   * - RPT-009
     - Antiguedad Saldos
     - UC-025

----

Funciones RBAC: Dashboard
-------------------------

.. list-table::
   :widths: 12 40 48
   :header-rows: 1

   * - Codigo
     - Nombre
     - UC
   * - DSH-001
     - Dashboard Principal
     - UC-026
   * - DSH-002
     - Dashboard Financiero
     - UC-027
   * - DSH-003
     - Dashboard Operativo
     - UC-028
   * - DSH-004
     - Personalizar Dashboard
     - UC-029
   * - DSH-005
     - Exportar Dashboard
     - UC-030

----

.. toctree::
   :maxdepth: 1
   :caption: Reportes Contables

   UC_017_Generar_Reporte_Saldos
   UC_018_Generar_Reporte_Movimientos
   UC_019_Reporte_Balance_General
   UC_020_Reporte_Estado_Resultados
   UC_021_Reporte_Flujo_Efectivo
   UC_022_Reporte_Analisis_Cuentas
   UC_023_Reporte_Comparativo_Periodos
   UC_024_Reporte_Presupuesto_Real
   UC_025_Reporte_Antiguedad_Saldos

.. toctree::
   :maxdepth: 1
   :caption: Dashboard

   UC_026_Ver_Dashboard_Principal
   UC_027_Dashboard_Financiero
   UC_028_Dashboard_Operativo
   UC_029_Personalizar_Dashboard
   UC_030_Exportar_Dashboard

----

Historial de Cambios
--------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Fase 5 completada: 14 UC con PlantUML embebido (regenerados uno por uno)
