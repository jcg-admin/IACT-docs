17.15 Paralelismo ``par``
-------------------------

.. uml::

   @startuml
   participant "ExportarReporteFacade" as Facade
   database "audit_log" as Audit
   participant "log_app" as Log

   Facade -> Facade : encolar tarea

   par
     Facade ->> Audit : registrar evento
   else
     Facade ->> Log : notificar buzon
   end
   @enduml
