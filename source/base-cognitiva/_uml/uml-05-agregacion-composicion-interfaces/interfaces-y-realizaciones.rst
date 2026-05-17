Interfaces y realizaciones
==========================

Cuando haya creado varias clases y se dé cuenta de que no todas
pertenecen a una clase principal, pero su comportamiento debe
incluir algunas de las **mismas operaciones con las mismas
firmas**, querrá:

- codificar las operaciones en una de las clases y reutilizarlas
  en otras;
- desarrollar un conjunto de operaciones que puedan ser
  utilizadas en diferentes clases dentro de un sistema;
- y que también se puedan reutilizar en las clases de otro
  sistema.

Esto implica encontrar un método para capturar un **conjunto
reutilizable de operaciones**. Una forma de lograrlo es a través
de una **interfaz**: un conjunto de operaciones que especifica
cierto aspecto de la funcionalidad de una clase — un **conjunto
de operaciones que una clase presenta a otras clases**.

La interfaz puede establecer un **subconjunto** de las
operaciones de una clase y no necesariamente todas ellas.

Como un conjunto de operaciones, una interfaz **no tiene
atributos**. Para modelar una interfaz en UML se utiliza un
símbolo rectangular con el nombre de la interfaz escrito en
cursiva y precedido por el estereotipo ``<<interface>>``.

.. note::

 Para poder distinguir una clase que no muestra sus atributos de
 una interfaz, puede utilizar la estructura "estereotipo" y
 especificar la palabra ``<<interface>>``. Otra opción es
 colocar la letra ``I`` al principio del nombre de una interfaz.

Por ejemplo: si el teclado de la computadora garantizara que
parte de su funcionalidad *"haría las veces"* del teclado de una
máquina de escribir, bajo este esquema, la relación entre una
clase y una interfaz se conoce como **realización**, y se modela
como una línea discontinua con una **punta de flecha en forma de
triángulo sin rellenar** que adjunte y apunte a la interfaz.

Una **interfaz es un conjunto de operaciones que realiza una
clase**. Esta última se relaciona con una interfaz mediante la
**realización**, indicada por una línea discontinua con una
punta de flecha en forma de triángulo sin rellenar que apunta a
la interfaz.

Una **realización** se refiere a la relación entre una interfaz
y una clase que implementa esa interfaz. Es cuando una clase
dice: *"Voy a seguir las reglas de esta interfaz"*.

Una clase puede realizar más de una interfaz, y una interfaz
puede ser realizada por más de una clase.

.. uml::

   @startuml

   interface "ITypewriterKeyboard" as ITK {
     + pressKey(t)
     + getCharacter() : Char
     + toggleUppercase()
   }

   class ComputerKeyboard {
     - layout : String
     + pressKey(t)
     + getCharacter() : Char
     + toggleUppercase()
     + sendOSCommand()
   }

   ComputerKeyboard ..|> ITK
   @enduml

Otra forma (omitida en muchas convenciones modernas) de
representar una clase y su interfaz es con un **pequeño círculo**
(*lollipop*) que se conecte mediante una línea a la clase:

.. uml::

   @startuml

   class ComputerKeyboard
   () "ITypewriterKeyboard" as ITK
   ComputerKeyboard -- ITK
   @enduml
