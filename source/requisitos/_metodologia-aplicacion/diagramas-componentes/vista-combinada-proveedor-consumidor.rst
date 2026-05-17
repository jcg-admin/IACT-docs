16.9 Vista combinada — proveedor + consumidor
---------------------------------------------

.. uml::

   @startuml

   component "perm_app" as Perm
   component "rpt_app" as Rpt
   interface ISecurity

   Perm ..|> ISecurity : implementa
   Rpt ..> ISecurity : usa
   @enduml
