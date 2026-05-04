13.2 Estado con entry/do/exit
-----------------------------

.. uml::

   @startuml

   state Procesando {
     Procesando : entry / inicializar contador
     Procesando : do / leer y agregar lote
     Procesando : exit / consolidar batch
   }

   [*] --> Procesando
   Procesando --> [*]
   @enduml
