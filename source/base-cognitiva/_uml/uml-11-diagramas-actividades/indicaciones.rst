Indicaciones
============

Durante una secuencia es posible enviar una **indicación**
(*signal*). Cuando se reciba, provocará que se ejecute una
actividad.

- El **pentágono convexo** simboliza el**envío** de un evento.
- El **pentágono cóncavo** simboliza la**recepción** del evento.

.. uml::

   @startuml

   start
   :Preparar mensaje;
   ->Enviar señal>
   :Esperar...;
   ->Recibir señal<
   :Procesar respuesta;
   stop
   @enduml
