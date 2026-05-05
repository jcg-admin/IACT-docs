Operaciones
===========

Una operación es **algo que la clase puede realizar**, o que
usted (u **otra clase**) pueden hacer a una clase.

El nombre de una operación se escribe en minúsculas si consta de
una sola palabra. Si consta de más de una palabra, únalas e
inicie todas con mayúscula exceptuando la primera (``camelCase``,
igual que en atributos).

La lista de operaciones se inicia **debajo de una línea que las
separa de los atributos**.

.. uml::

   @startuml

   class Lavadora {
     marca : String
     modelo : String
     capacidad : Float
     --
     agregarRopa()
     agregarDetergente()
     activarse()
     sacarRopa()
   }
   @enduml

.. note::

 Es posible establecer información adicional de los atributos y
 de las operaciones.

En los paréntesis que preceden al nombre de la operación podrá
mostrar el **parámetro** con el que funcionará la operación
junto con su tipo de dato.

La **función**, que es un tipo de operación, devuelve un valor
luego que finaliza su trabajo; la función podrá mostrar el tipo
de valor que regresará.

Estas secciones de información acerca de una operación se
conocen como la **firma de la operación**.

.. uml::

   @startuml

   class Lavadora {
     marca : String
     capacidad : Float
     --
     agregarDetergente(d : Integer)
     activarse(modo : String) : Boolean
     obtenerCapacidad() : Float
   }
   @enduml

No es muy útil mostrar siempre los nombres de los atributos y de
las operaciones — se puede ver un diagrama saturado. En lugar de
ello podrá tan sólo mostrar el nombre de la clase y dejar ya
sea el área de atributos o el de operaciones (o ambas) vacía.

.. uml::

   @startuml

   class Lavadora1 as "Lavadora"
   class Lavadora2 as "Lavadora" {
     marca
     modelo
   }
   class Lavadora3 as "Lavadora" {
     --
     agregarRopa()
     activarse()
   }
   @enduml

.. tip::

 En ocasiones será bueno **mostrar algunos (pero no todos)** de
 los atributos u operaciones. Para indicar que sólo enseñará
 algunos de ellos, seguirá la lista de aquellos que mostrará
 **con tres puntos (...)**.

A la omisión de ciertos o todos los atributos y operaciones se
le conoce como **abreviar una clase**.

.. uml::

   @startuml

   class Lavadora {
     marca
     modelo
     ...
     --
     agregarRopa()
     ...
   }
   @enduml

Si tiene una larga lista de atributos u operaciones podrá
utilizar un **estereotipo** para organizarla de forma que sea
más comprensible.

Un **estereotipo** es el modo en que UML le permite extenderlo,
es decir, **crear nuevos elementos** que son específicos de un
problema en particular que intente resolver.

Para mostrar un estereotipo, su nombre va bordeado por dos pares
de paréntesis angulares: ``<<info ejemplo>>``. Para una lista
de atributos, podrá utilizar un estereotipo como encabezado de
un subconjunto de atributos.

.. uml::

   @startuml

   class Lavadora {
     <<identidad>>
     marca : String
     modelo : String
     numeroSerie : String
     <<operacion>>
     capacidad : Float
     velocidadMotor : Integer
     --
     agregarRopa()
     activarse()
   }
   @enduml

También podrá utilizar el estereotipo sobre el nombre de una
clase para indicar algo respecto al **papel** de la clase.
