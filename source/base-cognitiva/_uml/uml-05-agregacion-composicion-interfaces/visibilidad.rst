Visibilidad
===========

La **visibilidad** se aplica a atributos u operaciones, y
establece la proporción en que otras clases podrán utilizar los
atributos y operaciones de una clase dada (o las operaciones de
una interfaz).

- **Nivel público** — la funcionalidad se extiende a otras
  clases. Antecede el atributo u operación con un signo de suma
  (``+``).
- **Nivel protegido** — la funcionalidad se otorga sólo a las
  clases que se heredan de la clase original. Antecede con un
  símbolo de número (``#``).
- **Nivel privado** — sólo la clase original puede utilizar el
  atributo u operación. Antecede con un guion (``-``).

Por ejemplo, en una **televisión**: ``modificarVolumen()`` y
``cambiarCanal()`` son operaciones públicas;
``dibujarImagenEnPantalla()`` es privada.

En un **automóvil**: ``acelerar()`` y ``frenar()`` son
operaciones públicas, pero ``actualizarKilometraje()`` es
protegida.

.. tip::

 La realización implica que el nivel **público** se aplique a
 cualquier operación en una interfaz. La protección de
 operaciones mediante cualquiera de los otros niveles tal vez no
 tendría sentido, dado que una interfaz se orienta a ser
 realizada por diversas clases.

.. uml::

   @startuml

   class Television {
     - circuitos
     - decodificador
     + modificarVolumen()
     + cambiarCanal()
     - dibujarImagenEnPantalla()
   }

   class Automovil {
     - chasis
     # kilometraje : Integer
     + acelerar()
     + frenar()
     # actualizarKilometraje()
   }
   @enduml

----
