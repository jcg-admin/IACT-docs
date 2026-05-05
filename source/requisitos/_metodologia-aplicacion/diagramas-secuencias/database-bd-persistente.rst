17.3 Database (BD persistente)
------------------------------

.. uml::

   @startuml
   participant "rpt_app" as Rpt
   database "bd_analytics" as BD_ANALYTICS
   Rpt -> BD_ANALYTICS : SELECT agregados
   BD_ANALYTICS --> Rpt : filas
   @enduml
