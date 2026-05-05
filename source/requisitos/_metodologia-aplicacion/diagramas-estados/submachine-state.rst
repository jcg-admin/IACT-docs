13.10 Submachine state
----------------------

.. uml::

   @startuml

   [*] --> Inicializada

   state Procesando {
     ' Detalles modelados en sub-diagrama
   }

   note right of Procesando
     Sub-maquina:
     ver diagramas-estados § 6.1
   end note

   Inicializada --> Procesando : start
   Procesando --> Completada : ok
   Completada --> [*]
   @enduml
