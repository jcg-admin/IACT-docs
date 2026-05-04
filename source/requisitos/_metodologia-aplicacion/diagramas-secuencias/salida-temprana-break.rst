17.16 Salida temprana ``break``
-------------------------------

.. uml::

   @startuml
   participant "etl_runner" as ETL
   database "bd_operativa" as BDO

   loop hasta fin de ventana
     ETL -> BDO : leer lote
     break [ventana agotada]
       ETL -> ETL : marcar carga incompleta
     end
   end
   @enduml
