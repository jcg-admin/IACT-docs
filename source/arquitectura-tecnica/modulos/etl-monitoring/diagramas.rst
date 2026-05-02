.. _arq-mod-004-diagramas:

================================================
ARQ_MOD_004 — Diagramas de Comportamiento
================================================


Flujo ETL Nocturno — sp_etl_maestro
======================================

.. uml::
 :caption: Secuencia ETL nocturno con sp_etl_maestro sobre MariaDB (CNST-006/008).

 @startuml

 actor "APScheduler\n/ Cron" as SCH
 participant "sp_etl_maestro\n(MariaDB)" as ETL
 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio IVR — solo lectura)" as SRC
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica — escribible)" as DEST
 database "etl_runs\n(MariaDB)" as LOG
 participant "SupervisionETLEndpoint\n(/api/v1/etl/supervision/)" as MON

 SCH -> ETL : CALL sp_etl_maestro(trimestre)\n(ventana nocturna CNST-006/008)
 ETL -> LOG : INSERT etl_runs (estado=en_ejecucion)
 ETL -> SRC : SELECT tbl_historico_detalle\n(solo lectura CNST-007)
 SRC --> ETL : registros IVR del trimestre
 ETL -> DEST : TRUNCATE + INSERT base_ivr_detalle
 ETL -> SRC : SELECT tbl_historico_clientes
 SRC --> ETL : datos clientes del trimestre
 ETL -> DEST : TRUNCATE + INSERT base_ivr_clientes
 ETL -> LOG : UPDATE etl_runs SET estado=exitoso

 note over MON
   view_pipeline_status consulta etl_runs.
   No interviene en el proceso ETL.
   Solo observa y reporta estado.
 end note

 @enduml

----

Sub-estados del proceso ETL
==============================

.. uml::
 :caption: Maquina de estados de una ejecucion ETL (etl_runs).

 @startuml

 [*] --> en_ejecucion : sp_etl_maestro invocado\n(automatico o manual)

 state en_ejecucion {
   [*] --> procesando_detalle : sp_etl_base_detalle
   procesando_detalle --> procesando_clientes : INSERT exitoso
   procesando_clientes --> [*] : INSERT exitoso
 }

 en_ejecucion --> exitoso : ambos sp_etl_* completan sin error
 en_ejecucion --> fallido : cualquier sp_etl_* lanza error

 exitoso --> [*] : datos disponibles en base_ivr_*
 fallido --> en_ejecucion : request_pipeline_retry manual (RBAC)
 fallido --> [*] : sin reintento

 note right of fallido
   BR-016: alerta si tasa
   de abandono >30% y ETL
   permanece fallido.
 end note

 @enduml

----

Diagrama de componentes — MOD_Pipeline
==========================================

.. uml::
 :caption: Componentes de MOD_Pipeline y sus dependencias de datos.

 @startuml

 actor "APScheduler" as SCH
 actor "request_pipeline_retry" as USR

 component "sp_etl_maestro\n(MariaDB SP)" as ETL_SP
 component "SupervisionEndpoint\n(/api/v1/etl/supervision/)" as SVC
 component "ETLScheduler\n(Django background task)" as SCHED

 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio IVR)" as HIST
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ANAL
 database "etl_runs\n(registro de ejecuciones)" as RUNS
 database "audit_log\n(PostgreSQL)" as AUDIT

 SCH --> SCHED : disparo automatico
 USR --> SVC : POST reintento (request_pipeline_retry)
 SCHED --> ETL_SP : CALL sp_etl_maestro
 SVC --> ETL_SP : CALL sp_etl_maestro (reintento)
 ETL_SP --> HIST : SELECT (solo lectura)
 ETL_SP --> ANAL : TRUNCATE + INSERT
 ETL_SP --> RUNS : INSERT/UPDATE ejecucion
 SVC --> AUDIT : INSERT auditoria

 @enduml
