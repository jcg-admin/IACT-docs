13.8 Deep history
-----------------

.. uml::

   @startuml

   state Procesando {
     state H_deep <<historyDeep>>
     [*] --> H_deep

     state Cargando {
       [*] --> LeyendoLote
       LeyendoLote --> Transformando : leido
       Transformando --> Insertando : transformado
     }
   }

   Procesando --> Pausada : pausar
   Pausada --> Procesando : reanudar (deep)
   @enduml
