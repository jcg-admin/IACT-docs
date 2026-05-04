17.3 Database (BD persistente)
------------------------------

.. uml::

   @startuml
   participant "rpt_app" as Rpt
   database "bd_analytics" as BDA
   Rpt -> BDA : SELECT agregados
   BDA --> Rpt : filas
   @enduml
