Adiciones al panorama
=====================

.. uml::

   @startuml

   skinparam packageStyle rectangle
   package "UML" {
     package "Comportamiento" {
       rectangle "Casos de uso"
       rectangle "Estados"
       rectangle "Secuencias"
       rectangle "Colaboraciones"
       rectangle "Actividades\n(NUEVO)" as ACT
     }
   }
   @enduml

----
