2.1 Símbolos básicos
--------------------

Cuatro elementos canónicos: **punto inicial** (círculo
relleno), **estado** (rectángulo redondeado),**transición**
(flecha etiquetada) y **punto final** (diana).

.. uml::

   @startuml

   [*] --> Estado1
   Estado1 --> Estado2 : transición
   Estado2 --> [*]
   @enduml
