6.2 Solicitar reintento ETL — UC_PIP_04
---------------------------------------

.. uml::

   @startuml

   participant ":AdminPipeline" as AdminPipeline
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL" as Sch
   participant ":AuditLog"     as AuditLog

   AdminPipeline  -> Sup  : 1. solicitarReintento(ejecucion_id)
   Sup -> Sup  : 2. validarEstado(FALLIDA)
   Sup -> Sch  : 3. enqueueReintento(jobId)
   Sch --> Sup : 4. jobEncolado
   Sup -> AuditLog   : 5. registrar(REINTENTO_SOLICITADO)
   Sup --> AdminPipeline  : 6. confirmación + ETA
   @enduml
