.. meta::
 :artefacto: FR-091.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-091-02:

==========================================================
FR-091.02: Control operacional via tabla ``job_config``
==========================================================

1. Identificacion
-----------------

* **ID:** FR-091.02
* **UC origen:** UC-091
* **Modulo:** MOD_Pipeline
* **Tipo:** Configuracion operacional
* **Actor:** Operador DBA / Admin de sistema

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE permitir habilitar/deshabilitar
y parametrizar el ETL nocturno via UPDATE en tabla
``job_config`` SIN requerir cambios de codigo, redeploy ni
recrear el EVENT.

**Comportamiento implementado:**

Tabla ``job_config`` con columnas operacionales:

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Columna
   - Significado
 * - ``job_name`` (PK)
   - Nombre canonico del job (``etl_diario``).
 * - ``is_enabled``
   - BOOL — habilita / pausa el job. Default ``TRUE``.
 * - ``timeout_seconds``
   - INT — tiempo maximo de ejecucion. Default ``1800``
     (30 min).
 * - ``ventana_inicio`` / ``ventana_fin``
   - TIME — ventana valida de ejecucion. Default 02:00-04:00.
 * - ``min_intervalo_h``
   - INT — minimo de horas entre ejecuciones (evita
     concurrencia accidental).
 * - ``notas``
   - TEXT libre.
 * - ``actualizado_en``
   - DATETIME auto-update.

Operaciones tipicas:

.. code-block:: sql

   -- Deshabilitar el ETL nocturno (incidente)
   UPDATE job_config
   SET is_enabled = FALSE,
       notas = 'Deshabilitado por incidente INC-2026-05-20-001'
   WHERE job_name = 'etl_diario';

   -- Ajustar timeout
   UPDATE job_config
   SET timeout_seconds = 3600
   WHERE job_name = 'etl_diario';

3. Criterios de aceptacion
--------------------------

* CA-01: ``is_enabled=FALSE`` evita que ``sp_etl_maestro``
  procese — la corrida termina inmediatamente con
  ``status='skipped'`` en ``etl_runs``.
* CA-02: ``is_enabled=TRUE`` reanuda procesamiento sin
  necesidad de reiniciar el EVENT o el scheduler.
* CA-03: cambios en ``job_config`` actualizan
  ``actualizado_en`` automaticamente (``ON UPDATE
  CURRENT_TIMESTAMP``).
* CA-04: el SP ``sp_etl_maestro`` consulta ``job_config`` al
  inicio de cada corrida.

4. Trazabilidad
---------------

* **Tabla:** ``provisioners/mariadb/schema_base_ivr.sql``
  lines 189-207.
* **Configuracion inicial:** insert por defecto para
  ``etl_diario`` (lines 210-214).
* **Consumido por:** ``sp_etl_maestro`` (chequeo
  ``is_enabled``) + APScheduler ``ETLScheduler``.

5. Solape
---------

UC_PIP_05 (uc-082 ``gestionar-configuracion-job-etl``) en otra
rama feature todavia no mergeada a develop documenta la API
REST para administrar ``job_config`` desde la aplicacion
(no solo SQL directo). Cuando ese UC se mergee, esta FR se
amplia con el contrato API.
