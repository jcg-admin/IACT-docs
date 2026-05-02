.. _arq-mod-005-casos-uso:

================================================
ARQ_MOD_005 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados (14 UC)
================================

Especificaciones completas: :doc:`/requisitos/casos-uso/reports/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_017
   - Consultar_Reporte_Trimestral
   - Consolidado por trimestre
 * - UC_018
   - Consultar_Reporte_Errores
   - Problemas de menu IVR
 * - UC_019
   - Consultar_Reporte_Transferencias
   - Rutas de llamada
 * - UC_020
   - Aplicar_Filtros_Fecha
   - Presets y rangos (max 2 anos)
 * - UC_021
   - Aplicar_Filtros_Negocio
   - Centro, servicio, cola
 * - UC_022
   - Exportar_Reporte_CSV
   - Formato CSV
 * - UC_023
   - Exportar_Reporte_Excel
   - Formato XLSX
 * - UC_024
   - Exportar_Reporte_PDF
   - Formato PDF
 * - UC_025
   - Consultar_Dashboard_Principal
   - Vista principal IVR
 * - UC_026
   - Consultar_Widgets_Resumen
   - KPIs operativos
 * - UC_027
   - Ver_Graficos_Hora
   - Temporal por hora
 * - UC_028
   - Ver_Graficos_Dia
   - Temporal por dia
 * - UC_029
   - Ver_Distribucion_Centro
   - Por centro/servicio
 * - UC_030
   - Personalizar_Layout_Dashboard
   - Max 10 widgets

----

Requisitos Funcionales Derivados
==================================

.. list-table::
 :widths: 12 45 20 23
 :header-rows: 1

 * - FR ID
   - Nombre
   - Deriva de
   - Descripcion
 * - FR_020
   - Cargar_Dashboard
   - UC_025
   - Widgets priorizados
 * - FR_021
   - Aplicar_Filtros
   - UC_020, UC_021
   - Fecha y negocio
 * - FR_022
   - Generar_CSV
   - UC_022
   - Con limites
 * - FR_023
   - Generar_Excel
   - UC_023
   - Con limites
 * - FR_024
   - Generar_PDF
   - UC_024
   - Con limites
 * - FR_025
   - Renderizar_Widgets
   - UC_026-029
   - Graficos y tablas
 * - FR_026
   - Guardar_Layout_Personalizado
   - UC_030
   - Max 10 widgets
