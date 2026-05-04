Los diagramas de distribución en el panorama
============================================

El panorama del UML queda finalizado al incluir el diagrama de
distribución.

.. uml::

   @startuml

   skinparam packageStyle rectangle
   package "UML — panorama completo" {
     package "Estructurales" {
       rectangle Clase
       rectangle Objeto
       rectangle Actor
       rectangle Interfaz
       rectangle "Caso de uso"
       rectangle Componente
       rectangle "Nodo\n(NUEVO)" as NODO
     }
     package "Comportamiento" {
       rectangle "Casos de uso"
       rectangle "Estados"
       rectangle "Secuencias"
       rectangle "Colaboraciones"
       rectangle "Actividades"
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

----
