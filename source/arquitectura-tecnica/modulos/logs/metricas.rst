.. _arq-mod-008-metricas:

================================================
ARQ_MOD_008 — Metricas Tecnicas
================================================

Metricas expuestas por el sistema para observabilidad tecnica.

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Metrica
   - Tipo
   - Descripcion
 * - request_duration_seconds
   - Histogram
   - Tiempo de respuesta por endpoint
 * - active_connections
   - Gauge
   - Conexiones base de datos activas
 * - error_count
   - Counter
   - Errores por tipo
 * - memory_usage_bytes
   - Gauge
   - Uso de memoria
 * - disk_usage_percent
   - Gauge
   - Uso de disco
