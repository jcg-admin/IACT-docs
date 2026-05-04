13.7 Shallow history
--------------------

.. uml::

   @startuml

   state Procesando {
     state H <<history>>
     [*] --> H

     state Cargando
     state Validando
     state Insertando

     Cargando --> Validando : ok
     Validando --> Insertando : valido
   }

   Procesando --> Pausada : pausar
   Pausada --> Procesando : reanudar
   @enduml
