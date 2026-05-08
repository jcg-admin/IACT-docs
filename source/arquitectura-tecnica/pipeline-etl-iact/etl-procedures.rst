.. meta::
 :artefacto: AT_PIPELINE_ETL_PROCEDURES
 :tipo: Especificacion de Implementacion — Nivel 3
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 3
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_procedures:

==============================================================
Nivel 3 — SPs ETL (extraccion-transformacion-carga)
==============================================================

Cinco SPs componen el Nivel 3 del pipeline:

- ``sp_etl_base_detalle`` — Nivel 3A, ETL principal. Scan
  mes a mes con ``GROUP BY`` por grain.
- ``sp_etl_base_clientes`` — Nivel 3B. Scan full quarter con
  ``COUNT(DISTINCT)``.
- ``sp_etl_validar`` — validaciones post-ETL.
- ``sp_etl_historico`` — backfill manual de quarters
  historicos.

Todos los SPs usan ``PREPARE/EXECUTE`` por la restriccion
CNST-ETL-008 (nombre de tabla dinamico).

----

Por que se procesa mes a mes
=============================

Con 13.6M filas (Q02_25), un DELETE+INSERT en una sola
transaccion genera varios GB de undo log en MariaDB 10.1.48.
Procesando por mes:

.. code-block:: text

   Enero   → DELETE mes + INSERT ~4.5M filas → COMMIT   (undo log < 1GB)
   Febrero → DELETE mes + INSERT ~4.5M filas → COMMIT
   Marzo   → DELETE mes + INSERT ~4.5M filas → COMMIT

Si falla en Febrero, Enero ya esta commiteado. El checkpoint
del step en ``job_execution_log`` permite saber hasta que mes
llego el ETL.

----

``sp_etl_base_detalle`` (Nivel 3A — ETL principal)
====================================================

Genera ``base_ivr_detalle`` con grain
``(trimestre, fecha_mes, segmento, centro_transferencia,
menu, opcion)``.

.. code-block:: sql

   CREATE PROCEDURE sp_etl_base_detalle(
       IN p_quarter  VARCHAR(10),    -- 'Q02_26'
       IN p_inicio   DATE,           -- '2026-04-01'
       IN p_fin      DATE,           -- '2026-06-30'
       IN p_table    VARCHAR(100),   -- 'tbl_historico_t2_2026'
       IN p_log_id   INT             -- ID en job_execution_log, o NULL
   )
   etl_detalle: BEGIN
       DECLARE v_mes_ini DATE;
       DECLARE v_mes_fin DATE;
       DECLARE v_total_ins INT DEFAULT 0;

       SET v_mes_ini = p_inicio;

       -- Iterar mes a mes dentro del quarter
       WHILE v_mes_ini <= p_fin DO
           SET v_mes_fin = LAST_DAY(v_mes_ini);
           IF v_mes_fin > p_fin THEN SET v_mes_fin = p_fin; END IF;

           -- DELETE idempotente solo para este mes
           DELETE FROM base_ivr_detalle
           WHERE trimestre = p_quarter
             AND fecha = DATE_FORMAT(v_mes_ini, '%Y%m');

           -- PREPARE/EXECUTE porque p_table es nombre dinamico (CNST-ETL-008)
           SET @etl_sql = CONCAT('
               INSERT INTO base_ivr_detalle
                   (trimestre, fecha, segmento, centro_transferencia,
                    menu, opcion,
                    total_llamadas, misma_linea, linea_diferente,
                    no_digito_telefono,
                    llamadas_entre_semana, llamadas_fines_semana)
               SELECT
                   ?,                                        -- trimestre
                   DATE_FORMAT(dFecha, ''%Y%m''),            -- fecha
                   fn_did_segmento(cDID_800Transfer),        -- segmento
                   fn_normalizar_centro(cDID_Centro_Transferencia),
                   fn_normalizar_menu(cMenu),
                   COALESCE(NULLIF(TRIM(cOpcion), ''''), ''SIN_OPCION''),
                   COUNT(*),
                   SUM(cTelefono_Origen = cTelefono_Digitado
                       AND cTelefono_Digitado IS NOT NULL),
                   SUM(cTelefono_Origen != cTelefono_Digitado
                       AND cTelefono_Digitado IS NOT NULL),
                   SUM(cTelefono_Digitado IS NULL),
                   SUM(ivr_es_dia_semana(dFecha)),           -- lun-vie
                   SUM(NOT ivr_es_dia_semana(dFecha))        -- sab-dom
               FROM ', p_table, '
               WHERE dFecha BETWEEN ? AND ?
                 AND cDID_800Transfer IN (''19020084'',''19028031'',''19020001'')
               GROUP BY
                   DATE_FORMAT(dFecha, ''%Y%m''),
                   fn_did_segmento(cDID_800Transfer),
                   fn_normalizar_centro(cDID_Centro_Transferencia),
                   fn_normalizar_menu(cMenu),
                   COALESCE(NULLIF(TRIM(cOpcion), ''''), ''SIN_OPCION'')
               ON DUPLICATE KEY UPDATE
                   total_llamadas        = VALUES(total_llamadas),
                   misma_linea           = VALUES(misma_linea),
                   linea_diferente       = VALUES(linea_diferente),
                   no_digito_telefono    = VALUES(no_digito_telefono),
                   llamadas_entre_semana = VALUES(llamadas_entre_semana),
                   llamadas_fines_semana = VALUES(llamadas_fines_semana),
                   cargado_en            = CURRENT_TIMESTAMP
           ');

           PREPARE etl_stmt FROM @etl_sql;
           SET @etl_q = p_quarter;
           SET @etl_i = v_mes_ini;
           SET @etl_f = v_mes_fin;
           EXECUTE etl_stmt USING @etl_q, @etl_i, @etl_f;
           SET v_total_ins = v_total_ins + ROW_COUNT();
           DEALLOCATE PREPARE etl_stmt;

           SET v_mes_ini = DATE_ADD(LAST_DAY(v_mes_ini), INTERVAL 1 DAY);
       END WHILE;

       -- Actualizar checkpoint si se proporciono log_id
       IF p_log_id IS NOT NULL AND p_log_id > 0 THEN
           UPDATE job_execution_log
           SET records_procesados = v_total_ins,
               status             = 'SUCCESS',
               end_time           = NOW()
           WHERE id = p_log_id;
       END IF;
   END etl_detalle;

Grain de ``base_ivr_detalle``
------------------------------

Una fila por combinacion unica de:
``(trimestre, fecha_mes, segmento, centro_transferencia,
menu, opcion)``.

Con 11-14M registros en la fuente y ~126 combinaciones reales
de ``menu × opcion``, el resultado es del orden de **miles de
filas por quarter** — no millones. Los indices hacen que los
7 SPs de reporte sean instantaneos.

----

``sp_etl_base_clientes`` (Nivel 3B — ETL secundario)
======================================================

``COUNT(DISTINCT cTelefono_Origen)`` no es aditivo: no puede
calcularse sumando valores de ``base_ivr_detalle``. Requiere un
segundo scan completo del quarter. Resultado: exactamente
**3 filas por quarter** (una por segmento).

.. code-block:: sql

   CREATE PROCEDURE sp_etl_base_clientes(
       IN p_quarter  VARCHAR(10),
       IN p_inicio   DATE,
       IN p_fin      DATE,
       IN p_table    VARCHAR(100),
       IN p_log_id   INT
   )
   BEGIN
       DELETE FROM base_ivr_clientes WHERE trimestre = p_quarter;

       SET @sql = CONCAT('
           INSERT INTO base_ivr_clientes (trimestre, segmento, clientes_unicos)
           SELECT
               ?,
               fn_did_segmento(cDID_800Transfer) AS segmento,
               COUNT(DISTINCT cTelefono_Origen)  AS clientes_unicos
               -- P-NEW-04: pendiente confirmar cTelefono_Origen vs cTelefono_Digitado
           FROM ', p_table, '
           WHERE dFecha BETWEEN ? AND ?
             AND cDID_800Transfer IN (''19020084'', ''19028031'', ''19020001'')
           GROUP BY fn_did_segmento(cDID_800Transfer)
       ');

       PREPARE stmt FROM @sql;
       SET @q = p_quarter, @i = p_inicio, @f = p_fin;
       EXECUTE stmt USING @q, @i, @f;
       DEALLOCATE PREPARE stmt;
       -- Resultado esperado: 3 filas (nacional_A, nacional_B, puebla)
   END;

----

``sp_etl_validar`` (validaciones post-ETL)
============================================

Verifica invariantes del resultado:

- ``base_ivr_clientes`` tiene exactamente 3 filas por quarter
  (una por segmento).
- ``base_ivr_detalle`` tiene al menos N filas (umbral
  configurable).
- Los valores agregados son consistentes
  (``total_llamadas = misma_linea + linea_diferente +
  no_digito_telefono``).

Si una validacion falla, marca el checkpoint del paso
``etl_validar`` como ``FAILED`` con el detalle del check
fallido. No revierte los datos cargados — el operador
diagnostica y decide si reintenta.

----

``sp_etl_historico`` (backfill manual)
=========================================

Carga quarters historicos uno a uno. Habilita
``etl_historico`` en ``job_config`` durante la ejecucion y lo
deshabilita al terminar para evitar disparos accidentales del
Event Scheduler.

.. code-block:: sql

   CREATE PROCEDURE sp_etl_historico(
       IN p_anio    INT,    -- 2025
       IN p_quarter INT     -- 1, 2, 3, 4
   )
   BEGIN
       DECLARE v_quarter VARCHAR(10);
       DECLARE v_table   VARCHAR(100);
       DECLARE v_inicio  DATE;
       DECLARE v_fin     DATE;

       -- Habilitar temporalmente
       UPDATE job_config SET is_enabled=TRUE WHERE job_name='etl_historico';

       SET v_quarter = CONCAT('Q0', p_quarter, '_', RIGHT(p_anio, 2));
       SET v_table   = CONCAT('tbl_historico_t', p_quarter, '_', p_anio);
       SET v_inicio  = MAKEDATE(p_anio, 1) + INTERVAL (p_quarter - 1) QUARTER;
       SET v_fin     = LAST_DAY(v_inicio + INTERVAL 2 MONTH);

       -- Ejecutar pipeline ETL para el quarter
       CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table, NULL);
       DO SLEEP(5);
       CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table, NULL);
       DO SLEEP(5);

       -- Deshabilitar al terminar
       UPDATE job_config SET is_enabled=FALSE WHERE job_name='etl_historico';
   END;

Uso (ver tambien :doc:`triggers`):

.. code-block:: sql

   CALL sp_etl_historico(2025, 1);   -- Q01_25
   CALL sp_etl_historico(2025, 2);   -- Q02_25
   CALL sp_etl_historico(2025, 3);   -- Q03_25
   CALL sp_etl_historico(2025, 4);   -- Q04_25
   CALL sp_etl_historico(2026, 1);   -- Q01_26

----

.. seealso::

 - :doc:`utility-functions` — funciones SQL usadas en los SPs.
 - :doc:`orchestration` — ``sp_etl_maestro`` que invoca estos
   SPs.
 - :doc:`intermediate-tables` — DDL de las tablas
   ``base_ivr_*`` y de control.
 - :doc:`report-procedures` — 7 SPs de reporte que leen
   ``base_ivr_*``.
