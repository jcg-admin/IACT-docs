El diagrama de secuencias
-------------------------

Los mensajes son **asincrónicos**: ninguno de los componentes
aguarda nada antes de continuar.

Cuando teclea en un procesador de textos, en ocasiones no ve
aparecer en la pantalla el carácter correspondiente a la tecla
que haya oprimido sino hasta después de haber oprimido algunas
más.

.. uml::

   @startuml

   actor Usuario
   participant ":GUI"          as GUI
   participant ":SistemaOp"    as SO
   participant ":CPU"          as CPU
   participant ":TarjetaVideo" as TV
   participant ":Monitor"      as MON

   Usuario ->> GUI : oprimirTecla
   GUI     ->> SO  : notificarTecla
   SO      ->> CPU : notificarTecla
   SO      ->> GUI : actualizar
   CPU     ->> TV  : enviarCaracter
   TV      ->> MON : presentarCaracter
   @enduml

Es muy instructivo mostrar los **estados** de uno o varios de los
objetos en el diagrama de secuencias. Se puede combinar con
diagrama de estados (híbrido). La secuencia se origina y
finaliza en el estado *Operativo* de la GUI.

.. uml::

   @startuml

   actor Usuario
   participant ":GUI" as GUI
   participant ":SistemaOp" as SO
   participant ":CPU" as CPU

   Usuario ->> GUI : oprimirTecla
   note over GUI : estado: Operativo → Registrando
   GUI ->> SO : notificarTecla
   SO  ->> CPU : notificarTecla
   SO  ->> GUI : actualizar
   note over GUI : estado: Registrando → Operativo
   @enduml

Otra forma de mostrar el cambio de estado de un objeto es
**incluir al objeto más de una vez** en el diagrama.
