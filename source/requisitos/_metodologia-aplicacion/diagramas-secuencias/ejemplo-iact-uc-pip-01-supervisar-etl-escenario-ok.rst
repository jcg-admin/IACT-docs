4.1 Ejemplo IACT — UC_PIP_01 (Supervisar ETL, escenario OK)
-----------------------------------------------------------

.. uml::

   @startuml

   actor "Admin\nPipeline" as Admin
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL"  as Sch
   participant ":BDAnalytics"   as BDAnalytics
   participant ":AuditLog"      as AuditLog

   Admin -> Sup  : abrirSupervision()
   activate Sup

   Sup -> Sch : ultimoRun()
   activate Sch
   Sch --> Sup : run_id, fecha_inicio, estado
   deactivate Sch

   Sup -> BDAnalytics  : SELECT errores WHERE run_id=?
   activate BDAnalytics
   BDAnalytics --> Sup : []  (sin errores)
   deactivate BDAnalytics

   Sup -> AuditLog  : registrar(VIEW_ETL_STATUS)
   activate AuditLog
   AuditLog --> Sup : ok
   deactivate AuditLog

   Sup --> Admin : panel ETL: estado OK,\nprox_ejecucion=02:00 AM
   deactivate Sup

   note over Admin,AuditLog
     Escenario feliz:
     última ejecución exitosa,
     CNST_008 ventana 6-12h
     respetada.
   end note
   @enduml

----
