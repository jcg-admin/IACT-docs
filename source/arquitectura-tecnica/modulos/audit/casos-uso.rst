.. _arq-mod-007-casos-uso:

================================================
ARQ_MOD_007 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/audit/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_070
   - Consultar_Bitacora_Auditoria
   - Ver eventos funcionales
 * - UC_071
   - Filtrar_Auditoria
   - Por usuario, fecha, recurso, tipo
 * - UC_072
   - Exportar_Eventos_Auditoria
   - CSV/Excel con limites
 * - UC_073
   - Generar_Reporte_Cambios_Permisos
   - Cumplimiento periodico

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
 * - FR_031
   - Listar_Eventos_Auditoria
   - UC_070
   - Paginacion, ordenamiento
 * - FR_032
   - Filtrar_Auditoria
   - UC_071
   - Multiples criterios
 * - FR_033
   - Exportar_Auditoria
   - UC_072
   - CSV/Excel
