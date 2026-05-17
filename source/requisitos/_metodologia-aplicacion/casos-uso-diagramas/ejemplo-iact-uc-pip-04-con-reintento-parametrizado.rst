7.2 Ejemplo IACT — UC_PIP_04 con reintento parametrizado
--------------------------------------------------------

.. uml::

   @startuml

   left to right direction
   actor "Admin\nPipeline" as Admin

   rectangle "IACT" {
     usecase "UC_PIP_04\nSolicitar reintento\n(BASE)"           as GESTION_PIPELINE_ETL
     usecase "UC_PIP_04b\nReintentar con\nparámetros ajustados" as P4B
   }

   Admin --> GESTION_PIPELINE_ETL
   Admin --> P4B

   P4B --|> GESTION_PIPELINE_ETL

   note right of P4B
     UC_PIP_04b HEREDA de UC_PIP_04:
       + permite ajustar la ventana
         CNST_008 (6-12h) si la
         ejecución original falló por
         timeout o conexión IVR.
   end note
   @enduml
