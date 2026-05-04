Clases de asociación
====================

Una **clase de asociación** puede contener atributos y
operaciones. Tiene cosas en común para las otras clases: si se
usa con otras clases, éstas tienen los mismos atributos y
operaciones que la clase asociada.

Puede concebir a una clase de asociación de la misma forma en que
lo haría con una clase estándar, y utilizará una **línea
discontinua** para conectarla a la línea de asociación. Una clase
de asociación puede tener asociaciones con otras clases.

Por ejemplo, un ``Jugador`` y un ``Equipo`` tienen un
``Contrato``. Este contrato es el mismo tanto para el jugador
como para el equipo; quien genera el contrato es el director
general. La clase de asociación ``Contrato`` se asocia con la
clase ``DirectorGeneral``, que a su vez se asocia con
``Jugador`` y ``Equipo``.

.. uml::

   @startuml

   class Jugador
   class Equipo
   class Contrato {
     fechaInicio : Date
     duracion : Integer
     monto : Float
   }
   class DirectorGeneral

   Jugador "1" -- "1" Equipo : participa en
   (Jugador, Equipo) .. Contrato
   Contrato -- DirectorGeneral : generado por
   @enduml

----
