Herencia y generalización
=========================

Si usted conoce algo de una categoría de cosas, automáticamente
sabrá algunas cosas que podrá transferir a otras categorías. A
esto se le conoce como **herencia**; UML también lo denomina
**generalización**.

Una clase (la **clase secundaria** o **subclase**) puede heredar
los atributos y operaciones de otra (la **clase principal** o
**superclase**).

La clase principal (o madre) es más genérica que la secundaria
(o hija). La hija es **sustituible** por la madre: donde quiera
que se haga referencia a la clase madre, también se hace
referencia a la clase hija (en el caso contrario no es
aplicable).

Una clase secundaria puede ser principal para otra clase
secundaria. En UML se coloca un **triángulo sin rellenar** que
apunte a la clase principal — esto se interpreta con la frase
*"es un tipo de"*.

Ejemplo: un ``Mamifero`` es una clase secundaria de ``Animal``,
y ``Caballo`` es una clase secundaria de ``Mamifero``. Un
``Mamifero`` *es un tipo de* ``Animal``, y un ``Caballo`` *es un
tipo de* ``Mamifero``.

.. uml::

   @startuml

   class Animal
   class Mamifero
   class Reptil
   class Ave
   class Caballo
   class Perro
   class Vaca

   Animal <|-- Mamifero
   Animal <|-- Reptil
   Animal <|-- Ave
   Mamifero <|-- Caballo
   Mamifero <|-- Perro
   Mamifero <|-- Vaca
   @enduml

Observe la apariencia del triángulo y las líneas cuando varias
clases secundarias son herencia de una clase principal. También
observe que no se colocaron los atributos y operaciones en las
subclases — esto trae por resultado un diagrama más ordenado.

.. tip::

 Al modelar, se tiene que satisfacer la relación *"es un tipo
 de"* con la clase principal. Si no se cumple, tal vez una
 asociación de otro tipo sea más adecuada.

Las clases secundarias agregan otras operaciones y atributos a
los que han heredado. En el ejemplo anterior, un ``Mamifero``
tiene pelo y da leche — dos atributos que no se encuentran en la
clase ``Animal``.

Una clase puede no provenir de una clase principal, en cuyo caso
será una **clase base** o **clase raíz**. En caso contrario,
una clase podría no tener clases secundarias, en cuyo caso será
una **clase final** o **clase hoja**.

Si una clase tiene exactamente una clase principal, tendrá
**herencia simple**. Si proviene de varias clases principales,
tendrá **herencia múltiple**.

Descubrimiento de la herencia
-----------------------------

El analista deberá darse cuenta de que los atributos y
operaciones de una clase son generales y que se aplicarán a,
quizá, varias clases (mismas que agregarán sus propios atributos
y operaciones).

En el ejemplo del baloncesto de la hora 3
(:doc:`uml-03-uso-orientacion-objetos`):

- El ``Jugador`` tiene atributos como ``nombre``, ``estatura``,
  ``peso``, ``velocidadAlCorrer`` y ``saltoVertical``. Tiene
  operaciones como ``driblar()``, ``pasar()``, ``rebotar()`` y
  ``tirar()``.
- Las clases ``Defensa``, ``Delantero`` y ``Central`` heredarán
  tales atributos y operaciones, y agregarán los suyos:

  - La clase ``Defensa`` podría tener las operaciones
    ``correrAlFrente()`` y ``quitarBalon()``.
  - El ``Central`` podría tener ``retacarBalon()``.

- De acuerdo con los comentarios del entrenador respecto a las
  estaturas, el analista tal vez quisiera colocar
  **restricciones** en las estaturas para cada posición.

- El modelo del baloncesto tiene un ``CronometroDeJuego`` (que
  controla el tiempo restante en un periodo de juego) y un
  ``LapsoDeTiro`` (que controla el tiempo restante desde el
  instante que un equipo tomó posesión del balón). Si nos damos
  cuenta de que **ambos controlan el tiempo**, el analista
  podría formular una clase ``Reloj`` con una operación
  ``controlarTiempo()`` que podrían heredar tanto
  ``CronometroDeJuego`` como ``LapsoDeTiro``.

- Dado que ``LapsoDeTiro`` controla 24 segundos (profesional) o
  35 segundos (colegial) y el ``CronometroDeJuego`` controla 12
  minutos (profesional) o 20 minutos (colegial),
  ``controlarTiempo()`` será **polimórfico**.

----
