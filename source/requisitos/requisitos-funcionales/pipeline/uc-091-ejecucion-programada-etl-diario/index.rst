.. meta::
 :artefacto: UC-091
 :tipo: Caso de Uso (spec-from-code, db-derived)
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc-091:

============================================================
UC-091: Ejecucion Programada Automatica del ETL Diario
============================================================

.. list-table::
 :widths: 25 75

 * - **Marker codigo DB**
   - ``evt_etl_diario`` (MariaDB EVENT) + ``job_config`` table
 * - **Marker codigo API**
   - APScheduler ``ETLScheduler`` (apps/pipeline/scheduler.py)
 * - **Actor**
   - Sistema (cron interno MariaDB + APScheduler Django)
 * - **Modulo**
   - MOD_Pipeline
 * - **Origen**
   - spec-from-code retroactivo (inspeccion DB layer)

.. admonition:: Hallazgo del audit
   :class: note

   Este UC fue identificado cuando el sponsor pregunto sobre
   posible deuda inversa desde IACT-db. La inspeccion de
   ``provisioners/mariadb/objetos/jobs/`` revelo un EVENT cron
   (``evt_etl_diario``) + tabla ``job_config`` con control
   operacional (enable/disable) que NO estaban documentados
   como UC propio.

   UC_PIP_04 (uc-074) cubre **reintentar** el pipeline (accion
   manual). Este UC-091 cubre el **disparo automatico
   nocturno** y el control operacional via ``job_config``,
   que son funcionalidad distinta.

Proposito
=========

Garantizar que el pipeline ETL IVR se ejecute automaticamente
cada noche a las 2:00 AM sin intervencion humana, con control
operacional explicito (enable/disable) en tabla ``job_config``
para responder a incidentes sin tocar codigo ni recrear
EVENTs.

Componentes
===========

.. list-table::
 :header-rows: 1
 :widths: 30 35 35

 * - Componente
   - Ubicacion
   - Responsabilidad
 * - ``evt_etl_diario`` EVENT
   - ``provisioners/mariadb/objetos/jobs/evt_etl_diario.sql``
   - Cron MariaDB que ejecuta ``CALL sp_etl_maestro()`` cada
     dia a las 2:00 AM. Requiere ``event_scheduler=ON``.
 * - ``job_config`` table
   - ``provisioners/mariadb/schema_base_ivr.sql`` lines 189-207
   - Configuracion operacional por job: ``is_enabled``,
     ``timeout_seconds``, ``ventana_inicio/fin``,
     ``min_intervalo_h``.
 * - ``ETLScheduler``
   - ``apps/pipeline/scheduler.py``
   - APScheduler Django que tambien dispara el ETL desde el
     lado API (redundancia controlada).
 * - ``sp_etl_maestro``
   - ``provisioners/mariadb/objetos/sps/sp_etl_maestro.sql``
   - Orquestador principal del ETL: llama
     sp_etl_base_clientes, sp_etl_base_detalle, sp_etl_validar.
 * - ``job_execution_log`` + ``etl_runs``
   - tables (schema_base_ivr.sql)
   - Persistencia de cada corrida del ETL para auditoria
     posterior (consumido por UC_PIP_01..03).

FR derivados
============

.. toctree::
 :hidden:
 :maxdepth: 1

 fr-091-01-disparo-cron-mariadb-2am
 fr-091-02-control-operacional-job-config
