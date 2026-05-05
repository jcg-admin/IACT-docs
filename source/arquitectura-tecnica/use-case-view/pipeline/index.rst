.. meta::
 :artefacto: AT_UC_MOD_PIPELINE
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_pipeline:

==================================================
MOD_Pipeline — Gestion del Pipeline: UC por Modulo
==================================================

Supervisión, monitoreo y reintento del pipeline IVR. El
pipeline transforma los datos del Repositorio IVR a la
Base Analítica IVR vía ``sp_pipeline_master``. El registro
de ejecuciones vive en ``pipeline_runs``.

.. uml::
 :caption: MOD_Pipeline — PipelineAdmin gestiona;
           Scheduler ejecuta automáticamente; Auditor lee.

 @startuml
 left to right direction

 actor User
 actor PipelineAdmin
 actor Auditor
 actor "Scheduler\n<<system>>" as Scheduler

 rectangle "MOD_Pipeline" {   usecase "UC_PIP_01\nVer Estado\nPipeline\n.. extension points ..\nVer errores / Ejecucion automatica" as VER_ESTADO
   usecase "UC_PIP_02\nVer Errores\nPipeline" as VER_ERRORES
   usecase "UC_PIP_03\nVer Disponibilidad\nde Datos" as VER_DISPONIBILIDAD
   usecase "UC_PIP_04\nReintentar Pipeline" as REINTENTAR
   usecase "Ejecutar Pipeline\nAutomatico" as EJECUCION_AUTO
 }

 User          --> VER_ESTADO
 User          --> VER_DISPONIBILIDAD
 PipelineAdmin --> VER_ERRORES
 PipelineAdmin --> REINTENTAR
 Auditor       --> VER_ESTADO
 Scheduler     --> EJECUCION_AUTO

 VER_ERRORES ..> VER_ESTADO : <<extend>>
 REINTENTAR ..> VER_ESTADO : <<include>>
 VER_ESTADO ..> EJECUCION_AUTO : <<extend>>

 note right of MOD_Pipeline
   Codenames RBAC:
     User → view_pipeline_status,
       view_data_availability
     PipelineAdmin (AGR-009) →
       view_pipeline_errors, request_pipeline_retry
     Auditor (AGR-008) → view_pipeline_status
     Scheduler: actor sistema (cron / APScheduler).
   Tabla: pipeline_runs (CNST-033 §3.5).
 end note

 @enduml

Lectura del diagrama
====================

- Cualquier ``User`` autenticado consulta estado y
  disponibilidad de datos.
- ``PipelineAdmin`` (AGR-009) ejecuta acciones de
  diagnóstico y recuperación: ver errores, reintentar.
- ``Auditor`` lee el estado para generar reportes de
  cumplimiento.
- ``Scheduler`` es **actor sistema**: ejecuta el
  pipeline automáticamente según cron y registra en
  ``pipeline_runs`` (sin intervención humana).
- ``UC_PIP_04`` ``<<include>>`` ``UC_PIP_01``: el
  reintento siempre consulta el estado actual antes de
  proceder.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` — PipelineExecution (UC_PIP_01/04).
- :doc:`/arquitectura-tecnica/domain-model/pipeline-log` — PipelineLog (registro de ejecución).

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_PIP_01 </requisitos/casos-uso/pipeline/uc-pip-01/index>`
   - Supervisar ETL
   - :doc:`Diagrama </requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PIP_02 </requisitos/casos-uso/pipeline/uc-pip-02/index>`
   - Consultar Errores ETL
   - :doc:`Diagrama </requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PIP_03 </requisitos/casos-uso/pipeline/uc-pip-03/index>`
   - Consultar Disponibilidad de Datos
   - :doc:`Diagrama </requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PIP_04 </requisitos/casos-uso/pipeline/uc-pip-04/index>`
   - Solicitar Reintento de Pipeline
   - :doc:`Diagrama </requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
