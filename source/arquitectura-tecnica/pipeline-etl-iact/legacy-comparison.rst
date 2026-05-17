.. meta::
 :artefacto: AT_PIPELINE_ETL_LEGACY_COMPARISON
 :tipo: Anexo — Comparacion v1 vs v2.1
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Informativo

.. _at_pipeline_etl_legacy_comparison:

==============================================================
Anexo — Comparacion con el legacy (FUNC_REPORTE_COBRANZA)
==============================================================

El sistema legacy del cliente expone un SP monolitico,
``FUNC_REPORTE_COBRANZA``, que produce todo el reporte en una
sola invocacion sobre ``tbl_historico_*``. El pipeline v2.1
descompone esa misma logica en un ETL nocturno + 7 SPs de
reporte sobre tablas materializadas.

Esta seccion documenta las diferencias estructurales y por
que la arquitectura v2.1 resulta de aplicar restricciones
operacionales (``CNST-ETL-*``) al patron legacy.

----

Tabla comparativa
==================

.. list-table::
 :widths: 22 38 40
 :header-rows: 1

 * - Aspecto
   - Legacy ``FUNC_REPORTE_COBRANZA``
   - Pipeline v2.1
 * - Granularidad
   - Un SP monolitico por reporte
   - ETL + 7 SPs de reporte separados
 * - Fuente de datos en runtime
   - ``tbl_historico_*`` (cliente)
   - ``base_ivr_*`` (IACT, materializada)
 * - Costo por request
   - Full scan al quarter
   - Lectura por indice (instantanea)
 * - Normalizacion
   - CASE inline duplicado en cada SP
   - 4 funciones (``fn_did_segmento``,
     ``fn_normalizar_centro``,
     ``fn_normalizar_menu``, ``fn_duracion_seg``)
 * - G-29 (38.8% con ``dHoraInicio > dHoraFin``)
   - Manejo inconsistente entre SPs
   - ``fn_duracion_seg()`` — una sola version
 * - Dias de semana
   - Catalogo de festivos del cliente
   - ``ivr_es_dia_semana()`` propias (IVR-7-dias)
 * - Procesamiento
   - DELETE+INSERT del quarter en una transaccion
   - Por mes (chunks ~4M filas)
 * - Crash recovery
   - Reintento manual del quarter completo
   - Checkpoint por paso en
     ``job_execution_log``
 * - Deteccion de timeout
   - No existe — ``etl_runs`` sin fin
   - Heartbeat Django + ``timeout_at``
 * - Carga del cliente
   - Una vez por request
   - Una vez por noche (ETL)

----

Por que la descomposicion
===========================

CNST-ETL-001 (solo SELECT en fuente) y CNST-ETL-005 (sin
indices en fuente) hacen inviable que cada request al API
haga scan a ``tbl_historico_*``. Con 13.6M filas en Q02_25,
un full scan toma minutos.

La materializacion en ``base_ivr_*`` mueve el costo de scan
al ETL nocturno, donde:

- Esta acotado en tiempo (``timeout_at`` = inicio + 30 min).
- Se ejecuta una sola vez por dia, no por request.
- Procesa por mes (CNST-ETL-007: undo log MariaDB 10.1
  manejable).
- Tiene checkpoint por paso (diagnostico granular).

Los SPs ``sp_rpt_*`` consultan ``base_ivr_*`` por indice y
son instantaneos. El API REST puede servir requests sin
tocar la base del cliente.

----

Equivalencias funcionales
==========================

Los 7 SPs de reporte v2.1 cubren las secciones que el legacy
producia en un solo monolitico:

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Seccion del reporte legacy
   - SP v2.1
 * - Centros de transferencia (volumen)
   - ``sp_rpt_centros_transferencia``
 * - Centros por segmento (entre-semana / fin)
   - ``sp_rpt_centros_xsegmento``
 * - Llamadas abandonadas
   - ``sp_rpt_llamadas_abandonadas``
 * - Distribucion de menu/opciones
   - ``sp_rpt_menu_redirigidos``
 * - Cruzado menu × centro
   - ``sp_rpt_menu_centro``
 * - Menus marcados como ERROR
   - ``sp_rpt_cMENU_ERROR``
 * - Clientes unicos
   - ``sp_rpt_clientes``

----

Que NO migro de v1
===================

- **CASE inline en SPs.** Reemplazado por funciones
  utilitarias (Nivel 0). Ver :doc:`utility-functions`.
- **DELETE+INSERT en una transaccion.** Reemplazado por
  procesamiento mes a mes. Ver :doc:`etl-procedures`.
- **Catalogo de festivos.** Eliminado. IVR opera 7 dias y
  el criterio de "entre semana" es lun-vie sin festivos
  (decision IVR-7-dias).
- **Reintento manual del quarter.** Reemplazado por
  ``sp_etl_historico`` controlado por ``job_config`` +
  checkpoints granulares.

----

.. seealso::

 - :doc:`index` — vision general del pipeline v2.1.
 - :doc:`utility-functions` — funciones que reemplazan el
   CASE inline del legacy.
 - :doc:`etl-procedures` — procesamiento por mes vs.
   DELETE+INSERT del quarter.
 - :doc:`orchestration` — checkpoints en
   ``job_execution_log`` que el legacy no tiene.
