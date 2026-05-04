Una red token-ring
------------------

En una red **token-ring**, las computadoras equipadas con una
**NIC** (tarjeta de interfaz de red) se conectan a una **MSAU**
(unidad central de acceso a multi estaciones). Se conectan
varias MSAU en serie que forma un anillo.

El anillo de MSAU se combina para fungir como un policía de
tránsito mediante una señal conocida como **token** que permite
a cada equipo saber cuándo puede transmitir información. El
token va de equipo en equipo hasta que uno de ellos contenga
información por enviar. Cuando se obtiene el token, sólo esa
información puede ir por la red.

.. uml::

   @startuml

   node "MSAU 1" as M1
   node "MSAU 2" as M2
   node "MSAU 3" as M3

   node "PC 1" <<procesador>> as P1
   node "PC 2" <<procesador>> as P2
   node "PC 3" <<procesador>> as P3
   node "PC 4" <<procesador>> as P4
   node "PC 5" <<procesador>> as P5

   M1 -- M2 : <<token>>
   M2 -- M3 : <<token>>
   M3 -- M1 : <<token>>

   M1 -- P1 : <<NIC>>
   M1 -- P2 : <<NIC>>
   M2 -- P3 : <<NIC>>
   M3 -- P4 : <<NIC>>
   M3 -- P5 : <<NIC>>
   @enduml
