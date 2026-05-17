Notas
-----

Es frecuente que alguna parte del diagrama no presente una clara
explicación del porqué está allí o la manera en que trabaja.
Cuando este sea el caso, la **nota UML** será útil.

La nota es un rectángulo con una esquina doblada, y dentro del
rectángulo se coloca la explicación. Se adjunta al elemento del
diagrama mediante una línea discontinua.

.. uml::

   @startuml

   class Tambor {
     - capacidad : Float
     + girar()
   }
   note right of Tambor
     El tambor gira en
     ambos sentidos durante
     el ciclo de lavado.
   end note
   @enduml
