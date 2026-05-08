.. meta::
 :artefacto: AT_DESIGN_MOD_PIPELINE
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_pipeline:

============================================================
Design View — MOD_Pipeline: Vista de Diseño
============================================================

Caja del modulo **MOD_Pipeline** (orquestacion del ETL nocturno
desde el sistema operacional IVR hacia el Almacen de Datos
analitico). Cubre el ciclo extract-transform-load, manejo de
errores y reintentos, supervision del estado de ejecucion, y
publicacion incremental de metricas al cache.

Materializa los UCs UC_PIP_01..04 documentados en
:doc:`/arquitectura-tecnica/use-case-view/pipeline/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Pipeline — PipelineExecution + ETL flow.
           Detalle de Disparador, ErroresETLService en
           :doc:`class`.

 @startuml

 package "MOD_Pipeline" {
   class PipelineExecution <<entity>>
   class DisparadorETL <<service>>
   class ErroresETLService <<service>>
 }

 class Metric <<external>>
 class MetricsCache <<external>>
 class AuditService <<external>>

 DisparadorETL ..> PipelineExecution : <<inicia>>
 PipelineExecution ..> Metric : <<produce>>
 Metric ..> MetricsCache : <<publica>>

 PipelineExecution ..> ErroresETLService : <<reporta errores>>
 PipelineExecution ..> AuditService : <<emite ciclo>>

 note bottom of PipelineExecution
   FSM (idle → running → completed |
   failed) en :doc:`state`.
   Flujo ETL completo en :doc:`activity`.
 end note

 @enduml

Lectura del diagrama
====================

- **Entidad central:** ``PipelineExecution`` representa una
  ejecucion concreta del ETL con timestamps, estado,
  contadores y errores recopilados.
- **DisparadorETL** lanza el ETL nocturno (BR-002 — 02:00 AM)
  o retries on-demand.
- **ErroresETLService** captura, clasifica y permite consulta
  de errores ETL para diagnostico.
- **Metric** producido por la pipeline se publica
  incrementalmente al ``MetricsCache`` para consumo de
  dashboards y alerts.
- FSM de PipelineExecution en :doc:`state`; flujo ETL
  completo en :doc:`activity`.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
  — PipelineExecution.
- :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`
  — PipelineExecutionRepo.
- :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
  PipelineLog.
- :doc:`/arquitectura-tecnica/domain-model/disparador-etl` —
  DisparadorETL.
- :doc:`/arquitectura-tecnica/domain-model/errores-etl-service`
  — ErroresETLService.
- :doc:`/arquitectura-tecnica/domain-model/metric` — Metric.
- :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
  MetricsCache.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Pipeline

 class
 sequence
 state
 activity

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/alerts/index` —
   consume Metric publicada al cache.
 - :doc:`/arquitectura-tecnica/design-view/reports/index` —
   consume Metric agregada.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
