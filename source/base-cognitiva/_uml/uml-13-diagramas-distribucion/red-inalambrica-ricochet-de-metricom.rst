Red inalámbrica Ricochet de Metricom
------------------------------------

**Metricom** ofrece una solución inalámbrica por módem para
acceso móvil a Internet. Su **módem inalámbrico** se conecta al
puerto serial de un equipo y se comunica con la red Ricochet.

La red Ricochet consta de transmisores y receptores de radio del
tamaño de una caja de zapatos. Estos **radios de microceldilla**
se montan en la parte superior de los postes de luz a distancias
de 400 a 800 metros, en patrón de tablero de ajedrez. Cada radio
obtiene una pequeña cantidad de energía del poste si se equipa
con un adaptador especial.

Los radios de microceldilla difunden señales a **Puntos de
acceso cableados** que llevan la información a un **NIF**
(*Network Interconnection Facility*).

El NIF consta de un **servidor de nombres** (BD que valida las
conexiones), un **enrutador** (enlaza redes entre sí) y una
**puerta de enlace** (traduce la información de un protocolo a
otro). La información se lleva del NIF a Internet.

.. uml::

   @startuml

   node "Laptop" <<procesador>> as L
   node "Modem inalambrico" <<dispositivo>> as M
   node "Radio microceldilla 1" <<dispositivo>> as R1
   node "Radio microceldilla 2" <<dispositivo>> as R2
   node "Punto de acceso cableado" <<dispositivo>> as PA

   node "NIF" {
     component "Servidor de nombres" as SN
     component "Enrutador"           as RT
     component "Puerta de enlace"    as GW
   }

   cloud "Internet" as NET

   L  -- M  : <<serial>>
   M  -- R1 : <<RF>>
   M  -- R2 : <<RF>>
   R1 -- PA : <<RF>>
   R2 -- PA : <<RF>>
   PA -- SN : <<cable>>
   SN -- RT
   RT -- GW
   GW -- NET
   @enduml
