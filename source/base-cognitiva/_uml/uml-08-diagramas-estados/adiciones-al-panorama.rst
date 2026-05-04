Adiciones al panorama
=====================

Ahora puede agregar los **elementos de comportamiento** al
panorama del UML.

.. uml::

   @startuml

   skinparam packageStyle rectangle

   package "UML" {
     package "Estructurales" {
       rectangle Clase
       rectangle Objeto
       rectangle Actor
       rectangle Interfaz
       rectangle "Caso de uso" as CU
     }
     package "Comportamiento" {
       rectangle "Casos de uso"  as CMP1
       rectangle "Estados"       as CMP2
       rectangle "Secuencias"    as CMP3
       rectangle "Actividades"   as CMP4
     }
     package "Relaciones" {
       rectangle Asociacion
       rectangle Generalizacion
       rectangle Dependencia
       rectangle Realizacion
     }
     package "Agrupamiento" {
       rectangle Paquete
     }
     package "Anotacion" {
       rectangle Nota
     }
     package "Extension" {
       rectangle Estereotipo
     }
   }
   @enduml

----
