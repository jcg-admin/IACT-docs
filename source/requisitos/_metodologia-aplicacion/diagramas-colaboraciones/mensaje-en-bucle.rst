14.8 Mensaje en bucle
---------------------

.. uml::

   @startuml
   allowmixing

   object ":etl_runner" as ETL
   object ":bd_operativa" as BDO

   ETL -> BDO : "1: *[i:1..n] leer_lote(i)"
   @enduml
