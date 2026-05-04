17.4 Boundary (integración externa read-only)
---------------------------------------------

.. uml::

   @startuml
   participant "etl_runner" as ETL
   boundary "ivr-host" as IVR
   ETL -> IVR : leer eventos del IVR
   IVR --> ETL : payload
   note right of IVR
     CNST_006: read-only;
     ventana 6-12h
   end note
   @enduml
