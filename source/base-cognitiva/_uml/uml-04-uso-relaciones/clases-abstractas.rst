Clases abstractas
=================

Las clases que **no proveen objetos** se dice que son
**abstractas**. Una clase abstracta se distingue por tener su
nombre en *cursivas*.

Las clases secundarias son importantes en el modelo dado que
finalmente usted querrá tener instancias de tales clases.

En el modelado de baloncesto necesitará instancias de
``Defensa``, ``Delantero``, ``Central``, ``CronometroDeJuego`` y
``LapsoDeTiro``. ``Jugador`` y ``Reloj`` **no proporcionan
ninguna instancia** al modelo. Un objeto de la clase ``Jugador``
no serviría a ningún propósito, así como tampoco uno de la clase
``Reloj``.

.. uml::

   @startuml

   abstract class Jugador {
     nombre : String
     estatura : Float
     --
     driblar()
     pasar()
     rebotar()
     tirar()
   }
   class Defensa
   class Delantero
   class Central
   Jugador <|-- Defensa
   Jugador <|-- Delantero
   Jugador <|-- Central

   abstract class Reloj {
     --
     controlarTiempo()
   }
   class CronometroDeJuego
   class LapsoDeTiro
   Reloj <|-- CronometroDeJuego
   Reloj <|-- LapsoDeTiro
   @enduml

----
