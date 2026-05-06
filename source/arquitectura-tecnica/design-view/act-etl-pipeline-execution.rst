.. meta::
 :artefacto: AT_DESIGN_ACT_ETL
 :tipo: Diagrama Arquitectonico — Design View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :flujo: etl-pipeline-execution
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_act_etl_pipeline_execution:

============================================================
Design View — Flujo: Ejecucion ETL Pipeline
============================================================

Flujo de ejecucion de un job ETL desde el scheduler hasta la
publicacion de metricas y el cierre del PipelineExecution. Cubre
el ciclo extract-transform-load con manejo de errores, retry,
y publicacion incremental al MetricsCache.

Cubre los UCs UC_PIP_01 (supervisar pipeline) y UC_PIP_02
(consultar errores).

.. uml::
 :caption: Flujo ETL — extract -> transform -> load -> metrics.

 @startuml

 start
 :Scheduler dispara job(job_id);
 :PipelineExecution crear(state=running);
 :Persistir via PipelineExecutionRepo;
 :Emitir AuditEvent(type=etl_start);

 partition Extract {
   :Conectar a fuentes (CDR, IVR, CRM);
   if (fuentes disponibles?) then (no)
     :state=failed, error=source_unavailable;
     :Emitir AuditEvent(type=etl_failed);
     stop
   else (si)
   endif
   :Leer batch incremental;
 }

 partition Transform {
   while (mas batches?) is (si)
     :Aplicar mappings + validaciones;
     if (validacion ok?) then (no)
       :Acumular errors[];
     else (si)
       :Producir Metric(s);
       :Actualizar MetricsCache(bucket, value);
     endif
   endwhile (no)
 }

 partition Load {
   :Persistir Metric(s) en TSDB;
   :Refresh PermissionCache si schema cambio;
 }

 if (errors[] vacio?) then (si)
   :state=completed;
   :Emitir AuditEvent(type=etl_completed);
 else (no)
   :state=completed_with_errors;
   :Emitir AuditEvent(type=etl_completed,
   errors_count=len(errors));
 endif

 :PipelineExecutionRepo.update(state, end_time);
 stop

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-pipeline`
 - :doc:`/arquitectura-tecnica/design-view/state-pipeline-execution`
 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/uc-pip-01-supervisar-etl`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
