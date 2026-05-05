17.4 Boundary (integración externa read-only)
---------------------------------------------

.. uml::

   @startuml
   participant "etl_runner" as SERVICIO_ETL
   boundary "ivr-host" as SISTEMA_IVR
   SERVICIO_ETL -> SISTEMA_IVR : leer eventos del SISTEMA_IVR
   SISTEMA_IVR --> SERVICIO_ETL : payload
   note right of SISTEMA_IVR
     CNST_006: read-only;
     ventana 6-12h
   end note
   @enduml
