.. meta::
 :artefacto: DB_002
 :tipo: Pipeline ETL
 :dominio: databases
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Alto

============
Pipeline ETL
============

Documenta el proceso ETL que transforma datos de llamadas IVR desde
las tablas fuente del cliente hacia las tablas analiticas de IACT,
todo dentro del mismo servidor MariaDB 10.1.48.

1. Restricciones canonicas
===========================

- **Frecuencia:** cada 6 a 12 horas (CNST_008). NO puede ser menor a
  6h ni mayor a 12h.
- **Mecanismo:** APScheduler o cron llama ``python manage.py run_etl``
  en la ventana programada.
- **Ventana preferente:** 02:00-04:00 hora local.
- **Motor:** stored procedures en MariaDB 10.1.48 (CNST_ETL_007).
  No hay window functions — el SP usa subqueries y agregaciones
  compatibles con MariaDB 10.1.x.
- **Prohibido:** Debezium, WebSockets, polling agresivo, replicacion
  sincrona, triggers cross-database, Python classes de transformacion.

2. Arquitectura del ETL
========================

El ETL es completamente SP-based (stored procedures en MariaDB).
Django actua exclusivamente como disparador via management command;
no ejecuta transformaciones en Python.

2.1 Stored Procedures del ETL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Stored Procedure
   - Responsabilidad
 * - ``sp_etl_maestro(p_fecha)``
   - Orquesta el ETL completo para la fecha indicada. Llama a
     ``sp_etl_base_detalle`` y ``sp_etl_base_clientes`` en secuencia.
 * - ``sp_etl_base_detalle(p_fecha)``
   - TRUNCATE + INSERT en ``base_ivr_detalle`` desde
     ``tbl_historico_*``. Normaliza ``cMenu`` a ``'VACIO'`` cuando
     el campo esta vacio o nulo.
 * - ``sp_etl_base_clientes(p_fecha)``
   - TRUNCATE + INSERT en ``base_ivr_clientes`` con dimension de
     clientes derivada de ``base_ivr_detalle``.
 * - ``sp_etl_historico(year, quarter_num)``
   - Reprocesa un trimestre completo (backfill o reintento).
     Usado por UC_PIP_04.

2.2 Patron TRUNCATE + INSERT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El ETL usa TRUNCATE + INSERT, no upsert. Esto garantiza idempotencia:
ejecutar el ETL dos veces para el mismo periodo produce el mismo
resultado que ejecutarlo una vez.

.. code-block:: sql

 -- patron dentro de sp_etl_base_detalle
 TRUNCATE TABLE base_ivr_detalle;
 INSERT INTO base_ivr_detalle (...)
 SELECT
     dFecha,
     cDID_800Transfer,
     cDID_Centro_Transferencia,
     CASE
         WHEN cMenu IS NULL OR cMenu = '' THEN 'VACIO'
         ELSE cMenu
     END AS menu,
     cOpcion,
     cTelefono_Origen,
     dHoraInicio,
     dHoraFin
 FROM tbl_historico_t3_2025;

2.3 Tabla de tracking etl_runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cada ejecucion del ETL queda registrada en ``etl_runs`` (tabla
propia de IACT en MariaDB):

.. code-block:: sql

 CREATE TABLE etl_runs (
     id              INT AUTO_INCREMENT PRIMARY KEY,
     tabla_origen    VARCHAR(100) NOT NULL,
     trimestre       VARCHAR(20)  NOT NULL,
     iniciado_en     DATETIME     NOT NULL,
     finalizado_en   DATETIME,
     estado          ENUM('en_ejecucion','exitoso','fallido')
                     DEFAULT 'en_ejecucion',
     registros_base  INT     DEFAULT 0,
     mensaje_error   TEXT,
     ejecutado_por   VARCHAR(100) DEFAULT 'scheduler',
     INDEX idx_estado_inicio (estado, iniciado_en DESC),
     INDEX idx_trimestre     (trimestre)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

3. Disparador Django
=====================

Django no ejecuta el ETL directamente. El flujo es:

1. APScheduler o cron invoca ``python manage.py run_etl`` en la
   ventana 02:00-04:00.
2. El management command ``run_etl`` inserta en ``etl_runs`` con
   estado ``en_ejecucion``.
3. Llama ``CALL sp_etl_maestro(p_fecha)`` via ``cursor.execute()``.
4. Actualiza ``etl_runs`` con el resultado (``exitoso`` o
   ``fallido``) y los registros procesados.

Para reintento manual (UC_PIP_04), el AdminPipeline dispara
``python manage.py run_etl --quarter Q3_25 --force``, que invoca
``CALL sp_etl_historico(year, quarter_num)``.

4. Stored Procedures de reporte
=================================

Los SPs de reporte son de lectura exclusiva, llamados por Django
al servir las vistas de reportes IVR. No participan en el ETL.

.. list-table::
 :widths: 45 55
 :header-rows: 1

 * - Stored Procedure
   - Datos que retorna
 * - ``sp_rpt_centros_transferencia(quarter)``
   - Llamadas por centro de transferencia y segmento
 * - ``sp_rpt_llamadas_abandonadas(quarter)``
   - Conteo y tasa de abandonos por segmento
 * - ``sp_rpt_menu_redirigidos(quarter)``
   - Llamadas por menu y resultado de redireccion
 * - ``sp_rpt_clientes(quarter)``
   - Dimension de clientes IVR del trimestre
 * - ``sp_rpt_centros_xsegmento(quarter)``
   - Distribucion de centros por segmento
 * - ``sp_rpt_menu_centro(quarter)``
   - Cruze menu x centro de transferencia
 * - ``sp_rpt_cMENU_ERROR(quarter)``
   - Registros con cMenu en estado de error

Django los invoca via ``cursor.callproc()`` sobre la conexion
``ivr`` (MariaDB). Ver patron en
:doc:`/arquitectura-tecnica/modulos/vis-reports/componentes`.

5. Casos de uso relacionados
=============================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index`
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index`
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/index`
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index`

6. Reglas de negocio
=====================

- :doc:`/requisitos/reglas-negocio/br-002-etl-batch-nocturno`
- :doc:`/requisitos/reglas-negocio/br-016-tasa-abandono`

7. UI obligatoria
==================

Las vistas que muestran datos IVR DEBEN mostrar el ``timestamp``
de la ultima ejecucion ETL exitosa (campo ``finalizado_en`` de la
ultima fila ``estado = 'exitoso'`` en ``etl_runs``) para que la
edad de los datos sea explicita (CNST_008 §UI obligatoria).
