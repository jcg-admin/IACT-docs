Mejor situación
---------------

Iniciemos con la mejor situación del caso de uso *"Comprar
gaseosa"*:

1. El cliente inserta el dinero en la alcancía de la fachada.
2. El cliente hace su elección.
3. El dinero viaja hacia el registrador.
4. El registrador verifica si la gaseosa elegida está en el
   dispensador.
5. Asumimos que sí hay gaseosas, y el registrador actualiza su
   reserva de efectivo.
6. El registrador hace que el dispensador entregue la gaseosa
   en la fachada.

.. uml::

   @startuml
   allowmixing

   actor Cliente
   object ":Fachada"     as F
   object ":Registrador" as R
   object ":Dispensador" as D

   Cliente -> F : "insertar(alimentacion, seleccion)"
   F -> R       : "1: agregar(alimentacion, seleccion)"
   R -> D       : "2: despachar(seleccion)"
   D -> F       : "3: despachar(seleccion)"
   @enduml
