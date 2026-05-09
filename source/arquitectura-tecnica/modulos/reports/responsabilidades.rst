.. _arq-mod-005-responsabilidades:

================================================
ARQ_MOD_005 — Responsabilidades del Modulo
================================================


PUEDE Hacer
===========

.. list-table::
 :widths: 50 15 15 20
 :header-rows: 1

 * - Responsabilidad
   - UC
   - CNST
   - Subcategoria
 * - Mostrar reporte trimestral consolidado
   - UC_017
   - -
   - Reportes
 * - Mostrar reporte de errores/menu
   - UC_018
   - -
   - Reportes
 * - Mostrar reporte de transferencias
   - UC_019
   - -
   - Reportes
 * - Aplicar filtros de fecha (max 2 anos)
   - UC_020
   - CNST_007
   - Filtros
 * - Aplicar filtros de negocio
   - UC_021
   - -
   - Filtros
 * - Exportar a CSV
   - UC_022
   - CNST_007
   - Export
 * - Exportar a Excel
   - UC_023
   - CNST_007
   - Export
 * - Exportar a PDF
   - UC_024
   - CNST_007
   - Export
 * - Mostrar dashboard principal
   - UC_025
   - -
   - Dashboard
 * - Mostrar widgets de resumen
   - UC_026
   - -
   - Dashboard
 * - Mostrar graficos por hora
   - UC_027
   - -
   - Dashboard
 * - Mostrar graficos por dia
   - UC_028
   - -
   - Dashboard
 * - Mostrar distribucion por centro
   - UC_029
   - -
   - Dashboard
 * - Personalizar layout (max 10 widgets)
   - UC_030
   - -
   - Dashboard

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Ejecutar ETL o agendar jobs**

  - El ETL es nocturno y automatizado
  - Responsabilidad de → :ref:`arq-mod-004`

- **Implementar logica de RBAC**

  - VIS_REPORTS solo **consume** permisos ya calculados
  - Responsabilidad de → :ref:`arq-mod-003`

- **Usar real-time (WebSockets, SSE, auto-refresh)**

  - Viola CNST_003 (no tiempo real)

- **Consultar BD IVR directamente**

  - Solo puede usar datos de BD Analytics
  - Viola CNST_003 (BD dual inmutable)
