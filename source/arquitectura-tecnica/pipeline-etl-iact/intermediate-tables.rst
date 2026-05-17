.. meta::
 :artefacto: AT_PIPELINE_ETL_INTERMEDIATE_TABLES
 :tipo: Especificacion de Implementacion — Nivel 4
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 4
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_intermediate_tables:

==============================================================
Nivel 4 — Tablas intermedias y de control
==============================================================

Cinco tablas en la base IACT componen el Nivel 4:

- ``base_ivr_detalle`` — agregado principal por grain
  ``(trimestre, fecha_mes, segmento, centro_transferencia,
  menu, opcion)``.
- ``base_ivr_clientes`` — clientes unicos por segmento
  (3 filas por quarter).
- ``etl_runs`` — historial de ejecuciones del pipeline
  con detección de timeout via heartbeat.
- ``job_execution_log`` — checkpoint por paso del pipeline
  para diagnostico granular.
- ``job_config`` — configuracion runtime de jobs
  (habilitado/deshabilitado, intervalos minimos).

----

``base_ivr_detalle``
=====================

Agregado principal. Una fila por combinacion unica de
``(trimestre, fecha_mes, segmento, centro_transferencia,
menu, opcion)``. Los 7 SPs de reporte la leen sin scan a la
fuente.

.. code-block:: sql

   CREATE TABLE base_ivr_detalle (
       trimestre              VARCHAR(10)  NOT NULL,   -- 'Q02_26'
       fecha                  CHAR(6)      NOT NULL,   -- 'YYYYMM'
       segmento               VARCHAR(20)  NOT NULL,   -- nacional_A | nacional_B | puebla
       centro_transferencia   VARCHAR(50)  NOT NULL,
       menu                   VARCHAR(50)  NOT NULL,
       opcion                 VARCHAR(50)  NOT NULL,

       total_llamadas         INT          NOT NULL DEFAULT 0,
       misma_linea            INT          NOT NULL DEFAULT 0,
       linea_diferente        INT          NOT NULL DEFAULT 0,
       no_digito_telefono     INT          NOT NULL DEFAULT 0,
       llamadas_entre_semana  INT          NOT NULL DEFAULT 0,
       llamadas_fines_semana  INT          NOT NULL DEFAULT 0,

       cargado_en             TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                              ON UPDATE CURRENT_TIMESTAMP,

       PRIMARY KEY (trimestre, fecha, segmento,
                    centro_transferencia, menu, opcion),
       INDEX idx_trimestre_segmento (trimestre, segmento),
       INDEX idx_centro             (centro_transferencia),
       INDEX idx_menu_opcion        (menu, opcion)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

Cardinalidad esperada
----------------------

Con ~126 combinaciones reales de ``menu × opcion`` × 3
segmentos × 3 meses ≈ orden de **miles de filas por
quarter**. Los ``sp_rpt_*`` consultan por indices y son
instantaneos.

----

``base_ivr_clientes``
======================

``COUNT(DISTINCT cTelefono_Origen)`` no es aditivo desde
``base_ivr_detalle``. Se calcula con un segundo scan al
quarter y se materializa en esta tabla — exactamente
**3 filas por quarter** (una por segmento).

.. code-block:: sql

   CREATE TABLE base_ivr_clientes (
       trimestre        VARCHAR(10)  NOT NULL,
       segmento         VARCHAR(20)  NOT NULL,
       clientes_unicos  INT          NOT NULL,

       cargado_en       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

       PRIMARY KEY (trimestre, segmento)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

----

``etl_runs``
=============

Historial de ejecuciones del pipeline completo con deteccion
de timeout via heartbeat (CNST-003 + ADR-BACK-012).

.. code-block:: sql

   CREATE TABLE etl_runs (
       id              INT AUTO_INCREMENT PRIMARY KEY,
       trimestre       VARCHAR(10)  NOT NULL,
       inicio_at       DATETIME     NOT NULL,
       fin_at          DATETIME     NULL,
       timeout_at      DATETIME     NOT NULL,    -- inicio_at + 30 min
       heartbeat_at    DATETIME     NULL,        -- ultimo heartbeat Django
       status          ENUM('en_ejecucion', 'success',
                            'failed', 'timeout', 'partial')
                       NOT NULL DEFAULT 'en_ejecucion',
       trigger_source  ENUM('mysql_event', 'django_command',
                            'manual_historico')
                       NOT NULL,
       error_message   TEXT         NULL,

       INDEX idx_trimestre (trimestre),
       INDEX idx_status    (status),
       INDEX idx_timeout   (timeout_at)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

Politica de timeout
--------------------

El management command ``run_etl`` actualiza ``heartbeat_at``
cada 60 segundos en un ``threading.Thread`` paralelo. Si el
proceso muere (crash de MariaDB, OOM kill), el heartbeat se
detiene. Una tarea de housekeeping detecta ``status =
'en_ejecucion' AND heartbeat_at < NOW() - INTERVAL 5 MINUTE``
y la marca como ``timeout``.

Sin Redis/RabbitMQ (ADR-BACK-012), este es el mecanismo de
liveness usado.

----

``job_execution_log``
======================

Checkpoint por paso. Cada SP del pipeline registra una fila
al inicio (status ``RUNNING``) y la actualiza al terminar
(``SUCCESS`` / ``FAILED`` / ``PARTIAL``). Permite diagnostico
preciso: "el ETL fallo en el paso ``etl_validar`` con error
X" en lugar de "el ETL fallo".

.. code-block:: sql

   CREATE TABLE job_execution_log (
       id                  INT AUTO_INCREMENT PRIMARY KEY,
       run_id              INT          NULL,         -- FK a etl_runs.id
       step_name           VARCHAR(50)  NOT NULL,     -- 'etl_base_detalle', 'etl_validar', ...
       trimestre           VARCHAR(10)  NULL,
       start_time          DATETIME     NOT NULL,
       end_time            DATETIME     NULL,
       status              ENUM('RUNNING', 'SUCCESS',
                                'FAILED', 'PARTIAL',
                                'SKIP', 'TIMEOUT')
                           NOT NULL DEFAULT 'RUNNING',
       records_procesados  INT          NULL,
       error_code          VARCHAR(20)  NULL,
       error_message       TEXT         NULL,

       INDEX idx_run_step   (run_id, step_name),
       INDEX idx_step_status(step_name, status),
       INDEX idx_start      (start_time)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

----

``job_config``
================

Configuracion runtime. Habilita/deshabilita jobs sin
redeploy, y ajusta el intervalo minimo entre ejecuciones
(CNST-003).

.. code-block:: sql

   CREATE TABLE job_config (
       job_name         VARCHAR(50)  PRIMARY KEY,
       is_enabled       BOOLEAN      NOT NULL DEFAULT TRUE,
       min_intervalo_h  INT          NOT NULL DEFAULT 6,
       last_run_at      DATETIME     NULL,
       descripcion      VARCHAR(200) NULL
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

Filas iniciales:

.. code-block:: sql

   INSERT INTO job_config (job_name, is_enabled, min_intervalo_h, descripcion) VALUES
     ('etl_diario',     TRUE,  6,  'ETL diario via MySQL Event'),
     ('etl_django',     TRUE,  6,  'ETL via management command'),
     ('etl_historico',  FALSE, 0,  'Backfill manual — habilitado solo durante carga');

----

.. seealso::

 - :doc:`etl-procedures` — SPs que escriben en
   ``base_ivr_*``.
 - :doc:`orchestration` — ``sp_etl_maestro`` que escribe
   en ``etl_runs`` y ``job_execution_log``.
 - :doc:`triggers` — heartbeat Django que actualiza
   ``etl_runs.heartbeat_at``.
 - :doc:`report-procedures` — SPs que leen
   ``base_ivr_detalle`` y ``base_ivr_clientes``.
