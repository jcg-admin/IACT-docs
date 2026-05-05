17.14 Ciclo ``loop`` con guarda
-------------------------------

.. uml::

   @startuml
   participant "etl_runner" as SERVICIO_ETL
   database "bd_operativa" as BD_OPERATIVA
   database "bd_analytics" as BD_ANALYTICS

   loop hasta fin de ventana CNST_006/008
     SERVICIO_ETL -> BD_OPERATIVA : leer lote (read-only)
     BD_OPERATIVA --> SERVICIO_ETL : filas
     SERVICIO_ETL -> BD_ANALYTICS : insertar agregados
   end
   @enduml
