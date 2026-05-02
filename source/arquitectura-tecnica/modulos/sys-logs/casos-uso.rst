.. _arq-mod-008-casos-uso:

================================================
ARQ_MOD_008 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/logs/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_080
   - Consultar_Bitacoras_Tecnicas
   - Logs de aplicacion con filtros
 * - UC_081
   - Consultar_Estado_Salud
   - Health endpoints, servicios
 * - UC_082
   - Descargar_Paquetes_Logs
   - Comprimido para analisis
 * - UC_083
   - Consultar_Metricas_Tecnicas
   - CPU, memoria, tiempos respuesta

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
 * - FR_034
   - Listar_Logs_Sistema
   - UC_080
   - Con filtros y paginacion
 * - FR_035
   - Consultar_Health_Check
   - UC_081
   - Estado de servicios
 * - FR_036
   - Empaquetar_Logs
   - UC_082
   - Compresion y descarga
