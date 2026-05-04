17.10 Self-message (iteración interna)
--------------------------------------

.. uml::

   @startuml
   participant "ExportarReporteFacade" as Facade

   loop por cada filtro
     Facade -> Facade : validar(filtro)
   end
   @enduml
