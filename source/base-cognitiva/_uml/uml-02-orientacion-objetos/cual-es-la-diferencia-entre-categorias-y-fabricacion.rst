¿Cuál es la diferencia entre categorías y fabricación?
-------------------------------------------------------

Si en la clase ``Lavadora`` se indica la marca, el modelo, el
número de serie y la capacidad (junto con las acciones de
agregar ropa, agregar detergente y sacar ropa), tendrá un
mecanismo para **fabricar nuevas instancias** a partir de su
clase; es decir, podrá **crear nuevos objetos**.

.. note::

 Los nombres de las clases, como lavadora, se escribirán como
 ``Lavadora``, y si constara de dos palabras se escribiría como
 ``LavadoraIndustrial``. Las características como número de
 serie se escribirán como ``numeroSerie``.

.. uml::

   @startuml

   class Lavadora {
     - marca : String
     - modelo : String
     - numeroSerie : String
     - capacidad : Float
     --
     + agregarRopa()
     + agregarDetergente()
     + sacarRopa()
   }

   object "lavadora1 : Lavadora" as l1
   object "lavadora2 : Lavadora" as l2
   object "lavadora3 : Lavadora" as l3

   Lavadora ..> l1 : <<instantiate>>
   Lavadora ..> l2 : <<instantiate>>
   Lavadora ..> l3 : <<instantiate>>
   @enduml

**Las clases en los programas orientados a objetos pueden crear
nuevas instancias.** El propósito de la orientación a objetos es
desarrollar software que refleje (es decir, que modele) un
esquema del mundo.

  **Entre más atributos y acciones tome en cuenta, mayor será
  la similitud de su modelo con la realidad.**

El ejemplo de la lavadora tendrá un modelo más exacto si incluye
los siguientes atributos: ``volumenTambor``, ``cronometroInterno``,
``trampa``, ``motor`` y ``velocidadMotor``. Podría hacerlo más
preciso si incluye las acciones de ``agregarBlanqueador``,
``cronometrarRemojo``, ``cronometrarLavado``, ``cronometrarEnjuague``
y ``cronometrarCentrifugado``.

.. uml::

   @startuml

   class Lavadora {
     - marca : String
     - modelo : String
     - numeroSerie : String
     - capacidad : Float
     - volumenTambor : Float
     - cronometroInterno : Cronometro
     - trampa : Trampa
     - motor : Motor
     - velocidadMotor : Integer
     --
     + agregarRopa()
     + agregarDetergente()
     + agregarBlanqueador()
     + cronometrarRemojo()
     + cronometrarLavado()
     + cronometrarEnjuague()
     + cronometrarCentrifugado()
     + sacarRopa()
   }
   @enduml

La orientación a objetos se refiere a algo más que tan sólo
atributos y acciones. Dichos aspectos se conocen como
**abstracción**, **herencia**, **polimorfismo**, **encapsulamiento**,
el **envío de mensajes**, las **asociaciones** y la **agregación**.
