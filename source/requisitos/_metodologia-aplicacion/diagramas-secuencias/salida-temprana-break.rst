17.16 Salida temprana ``break``
-------------------------------

.. uml::

   @startuml
   participant "etl_runner" as SERVICIO_ETL
   database "bd_operativa" as BD_OPERATIVA

   loop hasta fin de ventana
     SERVICIO_ETL -> BD_OPERATIVA : leer lote
     break [ventana agotada]
       SERVICIO_ETL -> SERVICIO_ETL : marcar carga incompleta
     end
   end
   @enduml
