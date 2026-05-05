16.3 Interfaz requerida (socket)
--------------------------------

.. uml::

   @startuml

   component "rpt_app" as Rpt
   interface ISecurity

   Rpt ..> ISecurity : usa
   @enduml
