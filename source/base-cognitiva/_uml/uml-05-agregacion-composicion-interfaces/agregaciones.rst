Agregaciones
============

Una clase que consta de otras clases es un tipo especial de
relación conocida como **agregación** o **acumulación**.

.. note::

 La **agregación** o **acumulación** es un tipo de asociación,
 en donde participan el componente y el todo. En agregación, el
 componente **no necesariamente corresponde a un solo todo**.

Puede representar una agregación como una jerarquía con la
**clase completa en la parte superior** y los **componentes por
debajo** de ella.

Una línea conectará el todo con un componente mediante un
**rombo sin relleno** que se colocará en la línea más cercana al
todo.

.. uml::

   @startuml

   class Computadora
   class Gabinete
   class Teclado
   class Raton
   class Monitor
   class UnidadCDROM
   class DiscoDuro

   Computadora o-- Gabinete
   Computadora o-- Teclado
   Computadora o-- Raton
   Computadora o-- Monitor
   Computadora o-- UnidadCDROM
   Computadora o-- "1..*" DiscoDuro
   @enduml

En el ejemplo anterior, cada componente corresponde a un todo.
En una agregación éste no será necesariamente el caso.

Por ejemplo: en un sistema casero de entretenimiento, un control
remoto podría ser un componente de una televisión, aunque
también podría ser un componente de una reproductora de casetes
de vídeo.

Restricciones en las agregaciones
---------------------------------

El conjunto de componentes posibles en una agregación se
establece dentro de una **relación O**: el componente *u otro*
es parte del todo.

Por ejemplo: una comida consta de **sopa o ensalada**, el plato
fuerte y el postre. Para modelar esto, utilizaría **una
restricción**: la palabra ``O`` dentro de llaves ``{O}`` con una
línea discontinua que conecte las dos líneas que conforman al
todo.

.. uml::

   @startuml

   class Comida
   class Sopa
   class Ensalada
   class PlatoFuerte
   class Postre

   Comida o-- Sopa
   Comida o-- Ensalada
   Comida o-- PlatoFuerte
   Comida o-- Postre

   Sopa ..> Ensalada : <<{O}>>
   @enduml
