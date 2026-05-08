Diagrama de clases
==================

Una clase es una categoría o grupo de cosas que tienen atributos y
acciones similares. Podríamos imaginar cada una de esas acciones
como un conjunto de tareas.

La clase **Lavadora** tiene atributos como son la marca, el
modelo, el número de serie y la capacidad. Entre las acciones de
las cosas de esta clase se encuentran: *agregar ropa*, *agregar
detergente*, *activarse* y *sacar ropa*.

.. uml::

   @startuml

   class WashingMachine {
     - brand : String
     - model : String
     - serialNumber : String
     - capacity : Float
     --
     + addClothes()
     + addDetergent()
     + activate()
     + removeClothes()
   }
   @enduml
