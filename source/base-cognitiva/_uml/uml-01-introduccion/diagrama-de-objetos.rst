Diagrama de objetos
===================

Un objeto es una **instancia de clase** (una entidad que tiene
valores específicos de los atributos y acciones).

Su lavadora, por ejemplo, podría tener la marca *Laundatorium*,
el modelo *Washmeister*, el número de serie *GL57774* y una
capacidad de 7 Kg.

El nombre de la instancia específica se encuentra a la izquierda
de los dos puntos (``:``), y el nombre de la clase a la derecha.

.. uml::

   @startuml

   object "miLavadora : Lavadora" as ml {
     marca = "Laundatorium"
     modelo = "Washmeister"
     numeroSerie = "GL57774"
     capacidad = 7.0
   }
   @enduml
