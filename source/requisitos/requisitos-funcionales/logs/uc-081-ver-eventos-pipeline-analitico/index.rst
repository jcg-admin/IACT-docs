.. _uc_081_ver_eventos_pipeline_analitico:

==================================================
UC-081: Ver Eventos del Pipeline Analítico
==================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``documentar-ucs-implementados-no-declarados``. El
   marker ``UC_LOG_08`` ya existia en codigo
   (apps/logs/, apps/pipeline/) con la descripcion
   "Eventos del pipeline analitico (pipeline_event_log)"
   pero carecia de RST en docs.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-081
   * - **Marker código**
     - ``UC_LOG_08``
   * - **Nombre**
     - Ver Eventos del Pipeline Analítico
   * - **Actor**
     - Admin / Operations
   * - **Módulo**
     - MOD_Logs
   * - **Tipo**
     - Consulta / Observabilidad

2. Especificación
-----------------

Endpoint de lectura sobre la tabla MariaDB
``pipeline_event_log`` (vista ``v_eventos_recientes``).
Lista eventos discretos del pipeline ETL — granularidad
mayor que UC-072 (errores) y UC-071 (estado): cada step
de cada job emite eventos con su payload, timing y
correlation_id.

Diferencia con UC_LOG_02 (Tail del log ETL): este UC
trabaja sobre eventos estructurados en tabla, no sobre
log file. Permite filtros por job_name, step, status,
ventana temporal.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker código**
     - ``UC_LOG_08``
   * - **Implementación**
     - ``apps/pipeline/pipeline_event_views.py``
   * - **TEST**
     - TST-fr-081-XX (pendiente)
   * - **Iniciativa origen**
     - documentar-ucs-implementados-no-declarados
   * - **Tabla DB**
     - ``pipeline_event_log`` (MariaDB ivr_legacy)
