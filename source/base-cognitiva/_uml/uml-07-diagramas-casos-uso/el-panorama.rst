El panorama
-----------

.. uml::

   @startuml

   skinparam packageStyle rectangle

   package "UML" as UML {
     package "Estructurales" as STR {
       rectangle Clase
       rectangle Objeto
       rectangle Actor
       rectangle Interfaz
       rectangle "Caso de uso" as CU
     }
     package "Relaciones" as REL {
       rectangle Asociacion
       rectangle Generalizacion
       rectangle Dependencia
       rectangle Realizacion
       note bottom of Dependencia
         Inclusion / Extension
       end note
     }
     package "Agrupamiento" as AGR {
       rectangle Paquete
     }
     package "Anotacion" as ANO {
       rectangle Nota
     }
     package "Extension" as EXT {
       rectangle Estereotipo
     }
     package "Comportamiento" as VALIDAR_COMPLEJIDAD {
       rectangle "Casos de uso\nEstados\nSecuencias\nActividades" as CMP
     }
   }
   @enduml
