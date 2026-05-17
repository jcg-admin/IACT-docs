Herencia
========

Una clase es una categoría de objetos (y en el mundo del
software, una plantilla sirve para crear otros objetos).

Un objeto es una instancia de una clase; como instancia de una
clase, un objeto tiene todas las características de la clase de
la que proviene. A esto se le conoce como **herencia**.

Cada objeto de la clase heredará dichos atributos y operaciones.
Un objeto no sólo hereda de una clase, sino que **una clase
también puede heredar de otra**.

Las lavadoras, refrigeradores, hornos de microondas, tostadores,
lavaplatos, radios, licuadoras y planchas son clases y forman
parte de una **clase más genérica** llamada ``Electrodomestico``.
Un electrodoméstico cuenta con los atributos de ``interruptor`` y
``cableElectrico``, y las operaciones de ``encender()`` y
``apagar()``.

Otra forma de explicarlo es que son **subclases** de la clase.
Decimos que la clase ``Electrodomestico`` es una **superclase** de
todas las demás.

.. uml::

   @startuml

   class Electrodomestico {
     - interruptor
     - cableElectrico
     + encender()
     + apagar()
   }
   class Lavadora
   class Refrigerador
   class HornoMicroondas
   class Tostador
   class Lavaplatos
   class Radio
   class Licuadora
   class Plancha

   Electrodomestico <|-- Lavadora
   Electrodomestico <|-- Refrigerador
   Electrodomestico <|-- HornoMicroondas
   Electrodomestico <|-- Tostador
   Electrodomestico <|-- Lavaplatos
   Electrodomestico <|-- Radio
   Electrodomestico <|-- Licuadora
   Electrodomestico <|-- Plancha
   @enduml

La herencia no tiene por qué terminar aquí. ``Electrodomestico``
es una subclase de ``ArticulosHogar``.

.. uml::

   @startuml

   class ArticulosHogar
   class Electrodomestico
   class Mueble
   class Decoracion

   ArticulosHogar <|-- Electrodomestico
   ArticulosHogar <|-- Mueble
   ArticulosHogar <|-- Decoracion

   class Lavadora
   class Refrigerador
   Electrodomestico <|-- Lavadora
   Electrodomestico <|-- Refrigerador
   @enduml
