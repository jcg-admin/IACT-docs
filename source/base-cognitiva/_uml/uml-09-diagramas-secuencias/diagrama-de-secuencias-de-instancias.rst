Diagrama de secuencias de instancias
------------------------------------

En el caso de uso *"Comprar gaseosa"*, el actor es un cliente
que desea adquirir una lata de gaseosa.

El cliente inicia el escenario mediante la inserción de dinero
en la máquina y luego hace una selección. Asumamos que en la
máquina hay tres objetos: la **fachada** (interfaz al usuario),
el **registrador de dinero** y el **dispensador**.

Daremos por hecho que el registrador controla al dispensador.
Secuencia:

1. El cliente inserta el dinero en la alcancía de la fachada.
2. El cliente hace su elección.
3. El dinero viaja hacia el registrador.
4. El registrador verifica si la gaseosa elegida está en el
   dispensador.
5. Dado que es el mejor escenario, asumimos que sí hay
   gaseosas, y el registrador actualiza su reserva de efectivo.
6. El registrador hace que el dispensador entregue la gaseosa
   en la fachada.

.. warning:: Diagrama de secuencias de instancias

 Es un diagrama de secuencias que sólo se centra en **un
 escenario** (una instancia).

Cada mensaje mueve el flujo de control de un objeto a otro
(mensajes simples).

.. uml::

   @startuml

   actor Cliente
   participant ":Fachada"      as F
   participant ":Registrador"  as R
   participant ":Dispensador"  as D

   Cliente -> F : insertarDinero
   Cliente -> F : seleccionarMarca
   F -> R       : enviarDinero
   R -> D       : verificarMarca
   D --> R      : disponible
   R -> R       : actualizarReserva
   R -> D       : entregarGaseosa
   D -> F       : depositarGaseosa
   F --> Cliente : tomarGaseosa
   @enduml
