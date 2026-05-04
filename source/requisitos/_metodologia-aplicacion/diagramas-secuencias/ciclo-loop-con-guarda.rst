17.14 Ciclo ``loop`` con guarda
-------------------------------

.. uml::

   @startuml
   participant "etl_runner" as ETL
   database "bd_operativa" as BDO
   database "bd_analytics" as BDA

   loop hasta fin de ventana CNST_006/008
     ETL -> BDO : leer lote (read-only)
     BDO --> ETL : filas
     ETL -> BDA : insertar agregados
   end
   @enduml
