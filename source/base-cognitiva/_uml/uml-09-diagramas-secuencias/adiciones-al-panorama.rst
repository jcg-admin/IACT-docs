Adiciones al panorama
=====================

El diagrama de secuencias va bajo la categoría **Elementos de
comportamiento**.

.. uml::

   @startuml

   skinparam packageStyle rectangle

   package "UML" {
     package "Comportamiento" {
       rectangle "Casos de uso"  as CMP1
       rectangle "Estados"       as CMP2
       rectangle "Secuencias\n(NUEVO)" as CMP3
       rectangle "Actividades"   as CMP4
     }
     package "Estructurales" {
       rectangle Clase
       rectangle Objeto
       rectangle Actor
       rectangle Interfaz
       rectangle "Caso de uso" as CU
     }
     package "Relaciones" {
       rectangle Asociacion
       rectangle Generalizacion
       rectangle Dependencia
       rectangle Realizacion
     }
     package "Agrupamiento" { rectangle Paquete }
     package "Anotacion"    { rectangle Nota    }
     package "Extension"    { rectangle Estereotipo }
   }
   @enduml
