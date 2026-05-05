Adiciones al panorama
=====================

El diagrama de colaboraciones es otro **elemento de
comportamiento**.

.. uml::

   @startuml
   allowmixing

   skinparam packageStyle rectangle

   package "UML" {
     package "Comportamiento" {
       rectangle "Casos de uso"  as CMP1
       rectangle "Estados"       as CMP2
       rectangle "Secuencias"    as CMP3
       rectangle "Colaboraciones\n(NUEVO)" as CMP4
       rectangle "Actividades"   as CMP5
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
   }
   @enduml
