Asociación binaria
==================

Relación que existe entre instancias/objetos de dos clases, donde
los objetos de una clase **existen de forma independiente** a la
existencia de los objetos de la otra clase.

La creación o destrucción de una instancia de la ``Clase A``
implica únicamente la creación o destrucción de la **relación**
que existe entre esa instancia y otra instancia de la ``Clase
B``, pero **nunca** significa la creación o destrucción de la
instancia de la ``Clase B``.

No hay una relación fuerte entre ambas instancias. El objeto de
la ``Clase A`` usa un objeto de la ``Clase B`` y puede que
viceversa también.

En UML esta asociación se representa con una **línea que une
ambas clases**.

**Ejemplo — Las obras de arte y las salas de un museo:**

Imagina un museo que alberga obras de arte. Cada obra de arte
(instancia de la clase ``Artwork``) está expuesta en una sala
del museo (instancia de la clase ``Room``).

Si se destruye una obra de arte (por ejemplo, se quema o se
deteriora), esto **no significa** que destruyamos la sala del
museo, ya que puede haber más obras de arte expuestas en ella.
Lo mismo pasa al revés: si destruimos una sala porque la vamos a
fusionar con otra o vamos a usar su espacio para otra cosa
(``Office``), las obras de arte que alberga no las tenemos que
destruir; en todo caso, las tendremos que reubicar en otras
salas.

.. uml::

   @startuml

   class Artwork {
     titulo : String
     autor : String
     anio : Integer
   }
   class Room {
     numero : Integer
     planta : Integer
   }
   Artwork "0..*" -- "1" Room : se exhibe en
   @enduml

----
