4. Diagrama de estados
----------------------

**Propósito:** los estados en los que un objeto puede estar y
cómo transiciona entre ellos. Estado + transición + evento.

**Cuándo usarlo:** cuando necesitas mostrar cómo algo cambia de
estado a lo largo del tiempo (ej.: orden pasando de *pendiente*
→ *confirmada* → *enviada* → *entregada*).

**Lección completa:** :doc:`/base-cognitiva/_uml/uml-08-diagramas-estados/index`.

.. uml::

   @startuml

   [*] --> Apagada
   Apagada --> Remojo : encender()
   Remojo --> Lavado
   Lavado --> Enjuague
   Enjuague --> Centrifugado
   Centrifugado --> Apagada
   Apagada --> [*]
   @enduml

----
