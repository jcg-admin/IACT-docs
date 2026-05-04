ARCnet
------

Una red **ARCnet** (*Attached Resource Computer Network*)
implica pasar un *token* o señal de un equipo a otro. La
diferencia es que en ARCnet **cada equipo tiene asignado un
número** y el orden numérico determina cuál equipo obtendrá el
token.

Cada equipo se conecta a un **concentrador** (*hub*) que puede
ser **activo** (amplifica la información) o **pasivo**
(transmite sin amplificar). A diferencia de los MSAU, los
concentradores ARCnet **no mueven el token en un anillo**; los
equipos se lo pasan entre sí.

.. uml::

   @startuml

   node "Hub Activo"  <<dispositivo>> as HA
   node "Hub Pasivo"  <<dispositivo>> as HP

   node "PC 1 (id=1)" <<procesador>> as P1
   node "PC 2 (id=2)" <<procesador>> as P2
   node "PC 3 (id=3)" <<procesador>> as P3
   node "PC 4 (id=4)" <<procesador>> as P4

   HA -- HP : <<cable>>
   HA -- P1
   HA -- P2
   HP -- P3
   HP -- P4

   note bottom of HA
     El token se pasa entre
     equipos en orden numérico
     (1 → 2 → 3 → 4 → 1).
   end note
   @enduml
