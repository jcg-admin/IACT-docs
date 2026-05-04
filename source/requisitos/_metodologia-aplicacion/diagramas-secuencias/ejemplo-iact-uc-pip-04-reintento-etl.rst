10.2 Ejemplo IACT — UC_PIP_04 reintento ETL
-------------------------------------------

.. uml::

   @startuml

   actor "Admin\nPipeline" as Admin
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL" as Sch
   participant ":BDAnalytics" as BDAnalytics
   participant ":AuditLog" as AuditLog

   Admin -> Sup : solicitarReintento(run_id)
   activate Sup

   loop [intentos < 3 AND estado != EXITOSA]
     Sup -> Sch : enqueueReintento(run_id, intentos)
     activate Sch
     Sch -> BDAnalytics : ejecutarCarga()
     activate BDAnalytics

     alt [carga exitosa]
       BDAnalytics --> Sch : commit_ok
       Sch --> Sup : EXITOSA
       Sup ->> AuditLog : registrar(ETL_RETRY_SUCCESS)
     else [error temporal — timeout IVR]
       BDAnalytics --> Sch : timeout
       Sch --> Sup : CON_ERRORES (temporal)
       Sup ->> AuditLog : registrar(ETL_RETRY_FAILED_TEMP)
     else [error permanente]
       BDAnalytics --> Sch : ERROR_PERM
       Sch --> Sup : ERROR_PERMANENTE
       Sup ->> AuditLog : registrar(ETL_RETRY_FAILED_PERM)
     end
     deactivate BDAnalytics
     deactivate Sch
   end

   alt [estado == EXITOSA]
     Sup --> Admin : ✓ ETL recuperado
   else [3 intentos fallidos]
     Sup ->> AuditLog : registrar(ETL_RETRY_GAVE_UP)
     Sup --> Admin : ✗ Requiere intervención manual
   end
   deactivate Sup
   @enduml

----
