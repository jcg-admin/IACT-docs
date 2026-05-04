Diagramas de componentes en el panorama
=======================================

El diagrama de componentes se enfoca en una **arquitectura de
software del sistema**.

.. uml::

   @startuml
   allowmixing

   skinparam packageStyle rectangle
   package "UML" {
     package "Estructurales" {
       rectangle Clase
       rectangle Objeto
       rectangle Actor
       rectangle Interfaz
       rectangle "Caso de uso" as CU
       rectangle "Componente\n(NUEVO)" as CMP
     }
     package "Comportamiento" {
       rectangle "Casos de uso"
       rectangle "Estados"
       rectangle "Secuencias"
       rectangle "Colaboraciones"
       rectangle "Actividades"
     }
   }
   @enduml

----
