14.8 Mensaje en bucle
---------------------

.. uml::

   @startuml
   allowmixing

   object ":etl_runner" as SERVICIO_ETL
   object ":bd_operativa" as BD_OPERATIVA

   SERVICIO_ETL -> BD_OPERATIVA : "1: *[i:1..n] leer_lote(i)"
   @enduml
