Estereotipos
------------

De vez en cuando se diseña un sistema que requiere algunos
elementos hechos a la medida. Los **estereotipos** o *clics* le
permiten tomar elementos propios del UML y convertirlos en otros.

Imagine a un estereotipo como una alteración. Se representa como
un nombre entre dos pares de paréntesis angulares (``«…»``) y
después se aplica al elemento.

El concepto de una **interfaz** provee un buen ejemplo. Una
interfaz es una clase que realiza operaciones y que no tiene
atributos; es un conjunto de acciones que tal vez quiera utilizar
una y otra vez en su modelo. En lugar de inventar un nuevo
elemento, podrá utilizar el símbolo de una clase con
``«Interfaz»`` situada justo sobre el nombre de la clase.

.. uml::

   @startuml

   class Lavable <<Interfaz>> {
     + iniciarCiclo()
     + detenerCiclo()
     + obtenerEstado()
   }
   class Lavadora
   Lavadora ..|> Lavable
   @enduml

----
