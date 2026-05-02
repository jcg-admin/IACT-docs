.. _arq-mod-004-casos-uso:

================================================
ARQ_MOD_004 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/pipeline/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_051
   - Consultar_Ejecuciones_ETL
   - Historico de jobs con duracion y resultado
 * - UC_052
   - Ver_Detalle_Ejecucion_ETL
   - Metricas, errores, rangos de fecha
 * - UC_053
   - Consultar_Disponibilidad_Datos
   - Trimestres completos/parciales/faltantes
 * - UC_054
   - Consultar_Incidencias_Calidad
   - Nulos, duplicados, inconsistencias
 * - UC_055
   - Reintentar_Procesamiento
   - Reprocesar metricas sin tocar origen

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
 * - FR_016
   - Listar_Ejecuciones_ETL
   - UC_051
   - Paginacion, filtros por fecha
 * - FR_017
   - Cargar_Detalle_ETL
   - UC_052
   - Incluir metricas y errores
 * - FR_018
   - Consultar_Disponibilidad
   - UC_053
   - Por trimestre, mes, dia
 * - FR_019
   - Listar_Incidencias_Calidad
   - UC_054
   - Filtrar por tipo y severidad
