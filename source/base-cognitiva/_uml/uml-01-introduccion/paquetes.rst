Paquetes
--------

Sirven para organizar los elementos de un diagrama en un grupo.
Tal vez quiera mostrar que ciertas clases o componentes son parte
de un subsistema en particular.

Los agruparía en un **paquete**, que se representa por una
carpeta tabulada.

.. uml::

   @startuml

   package "Subsistema Lavado" {
     class Tambor
     class Manguera
     class Drenaje
   }
   @enduml
