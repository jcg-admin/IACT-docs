2.1 Símbolos básicos
--------------------

Cuatro elementos canónicos: **límite del sistema**
(rectángulo), **caso de uso** (elipse),**actor** (figura
de palo) y **línea asociativa**.

.. uml::

   @startuml

   left to right direction
   actor "Actor\n(figura de palo)" as Actor

   rectangle "Límite del sistema (rectángulo)" {
     usecase "Caso de uso\n(elipse)" as CasoDeUso
   }

   Actor --> CasoDeUso : línea asociativa
   @enduml
