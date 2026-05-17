Multiplicidad
=============

La **multiplicidad** es la cantidad de objetos de una clase que
se relacionan con un objeto de la clase asociada. Dicha relación
se colocará sobre la línea de asociación junto a la clase
correspondiente.

.. uml::

   @startuml

   class Equipo
   class Jugador
   Equipo "1" -- "5..*" Jugador : tiene
   @enduml

Hay varios tipos de multiplicidades: uno a uno, uno a muchos, uno
a uno o más, uno a ninguno o uno, uno a un intervalo definido
(por ejemplo: uno a cinco hasta diez), uno a exactamente n, o uno
a un conjunto de opciones (por ejemplo, uno a nueve o diez).

Se utiliza un **asterisco** (``*``) para representar*muchos*.

En un contexto OR se representa por dos puntos, como en
``"1..*"`` (*uno o más*); en otro contexto, OR se representa por
una coma (``,``), como en ``"5, 10"`` (*5 o 10*).

.. tip::

 Cuando la clase ``A`` tiene una multiplicidad de uno a ninguno
 o uno con la clase ``B``, la clase ``B`` se dice que es
 **opcional** para la clase ``A``.

.. list-table:: Tipos de multiplicidad
 :widths: 30 70
 :header-rows: 1

 * - Multiplicidad
   - Significado
 * - ``1 → 1``
   - uno a uno
 * - ``1 →*``
   - uno a muchos
 * - ``1 → 1..*``
   - uno a uno o más (muchos)
 * - ``1 → 0,1``
   - uno a ninguno o uno
 * - ``1 → 12..18``
   - uno a 12 hasta 18
 * - ``1 → 3``
   - uno a tres
 * - ``1 → 12,24``
   - uno a 12 o 24
