17.5 Control (orquestador)
--------------------------

.. uml::

   @startuml
   actor Supervisor
   control "ExportarReporteFacade" as Facade
   participant "perm_app" as Perm
   participant "rpt_app" as Rpt

   Supervisor -> Facade : ejecutar(user, cfg)
   Facade -> Perm : verificar
   Facade -> Rpt : encolar
   @enduml
