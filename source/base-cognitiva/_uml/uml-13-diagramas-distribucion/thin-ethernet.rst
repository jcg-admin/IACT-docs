Thin ethernet
-------------

Los equipos se conectan a un cable de red mediante dispositivos
conocidos como **conectores T**. Un segmento de red puede unirse
a otro mediante un **repetidor**, dispositivo que amplifica una
señal antes de transmitirla.

.. uml::

   @startuml

   node "PC 1" <<procesador>> as P1
   node "PC 2" <<procesador>> as P2
   node "PC 3" <<procesador>> as P3
   node "PC 4" <<procesador>> as P4
   node "Repetidor" <<dispositivo>> as R
   node "PC 5" <<procesador>> as P5
   node "PC 6" <<procesador>> as P6

   P1 -- P2 : <<conector T>>
   P2 -- P3 : <<conector T>>
   P3 -- P4 : <<conector T>>
   P4 -- R  : <<coaxial>>
   R  -- P5 : <<coaxial>>
   P5 -- P6 : <<conector T>>
   @enduml
