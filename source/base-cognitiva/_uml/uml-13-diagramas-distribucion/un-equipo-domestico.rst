Un equipo doméstico
-------------------

Para modelar un equipo de cómputo doméstico, incluimos el
procesador y los dispositivos, y también la conexión telefónica
con el proveedor de servicios de Internet.

  La nube que representa Internet **no es parte** de la
  simbología UML, pero es útil para clarificar el modelo.

.. uml::

   @startuml

   node "PC Hogar"      <<procesador>> as PC
   node "Monitor"       <<dispositivo>> as MON
   node "Teclado"       <<dispositivo>> as TEC
   node "Ratón"         <<dispositivo>> as RAT
   node "Impresora"     <<dispositivo>> as IMP
   node "Modem ADSL"    <<dispositivo>> as MOD
   cloud "Internet"                     as NET
   node "Proveedor ISP" <<procesador>>  as ISP

   PC  -- MON : <<HDMI>>
   PC  -- TEC : <<USB>>
   PC  -- RAT : <<USB>>
   PC  -- IMP : <<USB>>
   PC  -- MOD : <<Ethernet>>
   MOD -- NET : <<ADSL>>
   NET -- ISP
   @enduml
