13.6 Estado compuesto con subestados
------------------------------------

.. uml::

   @startuml

   state EjecucionETL {
     [*] --> Inicializada
     Inicializada --> Cargando : start
     Cargando --> Validando : datos cargados
     Validando --> Completada : ok
     Completada --> [*]
   }

   [*] --> EjecucionETL
   EjecucionETL --> [*]
   @enduml
