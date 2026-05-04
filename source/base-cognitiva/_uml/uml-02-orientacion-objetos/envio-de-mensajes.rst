Envío de mensajes
=================

Los objetos trabajan en conjunto. Esto se logra mediante el
**envío de mensajes** entre ellos. Un objeto envía a otro un
mensaje para realizar una operación, y el objeto receptor
ejecutará la operación.

Una televisión y su control remoto pueden ser un ejemplo muy
intuitivo del mundo que nos rodea: al presionar el botón de
encendido, le envía literalmente un mensaje al televisor para
que se encienda. Muchas de las cosas que hace mediante el
control remoto, también las podrá hacer si se levanta de la
silla, va a la televisión y presiona los botones correspondientes.

La interfaz que la televisión le presenta (el conjunto de botones
y perillas) no es, obviamente, la misma que le muestra al control
remoto (un receptor de rayos infrarrojos).

  El envío de mensajes se puede hacer por diferentes interfaces.

.. uml::

   @startuml

   actor Persona
   participant ControlRemoto
   participant Television

   Persona        -> ControlRemoto : presionar botón
   ControlRemoto  -> Television    : señal IR (encender)
   Persona        -> Television    : presionar perilla\n(interfaz física)
   @enduml

----
