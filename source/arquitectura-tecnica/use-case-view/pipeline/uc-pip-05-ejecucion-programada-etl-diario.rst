.. meta::
 :artefacto: AT_UC_PIP_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :ultimo_cambio: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_pip_05_ejecucion_programada_etl_diario:

==============================================
UC_PIP_05 — Ejecucion Programada ETL Diario
==============================================

Sistema dispara automaticamente el pipeline ETL IVR a las 2:00 AM
via MariaDB EVENT ``evt_etl_diario``, con control operacional
explicito en tabla ``job_config`` (enable/disable / timeout /
ventana / intervalo). Complementario a UC_PIP_04
(``solicitar-reintento-de-pipeline`` — accion manual): UC_PIP_05
cubre el disparo automatico nocturno.

Vista canonica del requisito en
:doc:`/requisitos/requisitos-funcionales/pipeline/uc-091-ejecucion-programada-etl-diario/index`.

.. uml::
 :caption: UC_PIP_05 — actores y casos asociados (cron automatico).

 @startuml

 left to right direction

 actor "Sistema" as Sistema <<scheduler>>
 actor "DBA Operator" as DBA <<actor humano>>
 actor "MariaDB EventScheduler" as EventScheduler <<sistema>>
 actor "sp_etl_maestro" as SP <<sistema>>
 actor "job_config" as JobConfig <<tabla>>
 actor "etl_runs" as EtlRuns <<tabla>>
 actor "ETLScheduler (APScheduler)" as APScheduler <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_05\nEjecucion Programada\nETL Diario" as UC_PIP_05
   usecase "Disparo cron\n02:00 AM diario\n(evt_etl_diario)" as CRON
   usecase "Validar job_config\nis_enabled=TRUE" as VALIDAR_ENABLED
   usecase "Verificar no hay\nrun en curso\n(min_intervalo_h)" as VERIFY_IDLE
   usecase "Ejecutar\nsp_etl_maestro()" as EJECUTAR
   usecase "Registrar run\nen etl_runs" as REGISTRAR
   usecase "Timeout watcher\n(timeout_seconds)" as TIMEOUT
   usecase "Control operacional\nUPDATE job_config" as CONTROL_OPS
 }

 Sistema --> CRON
 CRON --> EventScheduler
 EventScheduler --> SP : CALL sp_etl_maestro()
 SP --> JobConfig : SELECT is_enabled
 SP --> VALIDAR_ENABLED
 SP --> VERIFY_IDLE
 SP --> EJECUTAR
 SP --> EtlRuns : INSERT/UPDATE row
 SP --> REGISTRAR
 APScheduler --> TIMEOUT : observa etl_runs.timeout_at
 DBA --> CONTROL_OPS
 CONTROL_OPS --> JobConfig

 UC_PIP_05 ..> VALIDAR_ENABLED : <<include>>
 UC_PIP_05 ..> VERIFY_IDLE : <<include>>
 UC_PIP_05 ..> EJECUTAR : <<include>>
 UC_PIP_05 ..> REGISTRAR : <<include>>
 UC_PIP_05 ..> TIMEOUT : <<extend>>
 UC_PIP_05 ..> CONTROL_OPS : <<extend>>

 @enduml

Componentes
===========

.. list-table::
 :header-rows: 1
 :widths: 30 20 50

 * - Componente
   - Capa
   - Responsabilidad
 * - ``evt_etl_diario``
   - MariaDB EVENT
   - Cron nativo. ``ON SCHEDULE EVERY 1 DAY STARTS 02:00:00``.
     ``DO CALL sp_etl_maestro()``.
 * - ``sp_etl_maestro``
   - MariaDB SP
   - Orquesta sp_etl_base_clientes + sp_etl_base_detalle +
     sp_etl_validar. Consulta ``job_config`` al inicio.
 * - ``job_config`` table
   - MariaDB schema_base_ivr
   - Configuracion operacional por job. PK ``job_name``.
     Modificable sin redeploy.
 * - ``etl_runs`` table
   - MariaDB schema_base_ivr
   - Bitacora de cada corrida. Estados:
     ``en_ejecucion -> terminado | timeout | error | skipped``.
 * - ``ETLScheduler``
   - Django (APScheduler)
   - Watcher del lado API. Detecta runs con
     ``timeout_at < NOW()`` y los marca timeout.

Restricciones
=============

* **CNST-013** (no Celery / no RabbitMQ): el cron canonico vive en
  MariaDB EVENT, no en un message broker externo. APScheduler
  Django es complementario, no critico.
* ``event_scheduler=ON`` en MariaDB es prerequisito de despliegue
  (verificar en provisioner).
* Idempotencia: ``min_intervalo_h`` impide ejecuciones concurrentes
  si una corrida anterior aun esta ``en_ejecucion``.

Trazabilidad
============

* **DB:** ``IACT-db/provisioners/mariadb/objetos/jobs/evt_etl_diario.sql``
* **SP:** ``IACT-db/provisioners/mariadb/objetos/sps/sp_etl_maestro.sql``
* **Tabla config:** ``IACT-db/provisioners/mariadb/schema_base_ivr.sql``
  lineas 189-207.
* **API watcher:** ``IACT-api/callcentersite/apps/pipeline/scheduler.py``.
* **Spec funcional:**
  :doc:`/requisitos/requisitos-funcionales/pipeline/uc-091-ejecucion-programada-etl-diario/index`.

Solape con UC_PIP_04
====================

UC_PIP_04 (``solicitar-reintento-de-pipeline``) es la **accion
manual** del operador via API. UC_PIP_05 es el **disparo
automatico** del cron. Ambos invocan ``sp_etl_maestro()`` pero
provienen de actores y triggers distintos:

* UC_PIP_04: operador humano + RBAC ``request_pipeline_retry`` +
  reason obligatoria + audit ``PIPELINE_RETRY_REQUESTED``.
* UC_PIP_05: sistema (cron) + sin reason + sin audit emit
  individual (la traza vive en ``etl_runs``).
