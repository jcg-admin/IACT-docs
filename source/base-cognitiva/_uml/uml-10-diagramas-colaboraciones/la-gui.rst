La GUI
======

Un actor inicia la secuencia al oprimir una tecla. Tal secuencia
(de la lección anterior):

1. La GUI notifica al sistema operativo que se oprimió una tecla.
2. El sistema operativo le notifica a la CPU.
3. El sistema operativo actualiza la GUI.
4. La CPU notifica a la tarjeta de vídeo.
5. La tarjeta de vídeo envía un mensaje al monitor.
6. El monitor presenta el carácter alfanumérico en la pantalla.

.. uml::

   @startuml
   allowmixing

   actor Usuario
   object ":GUI"          as GUI
   object ":SistemaOp"    as SO
   object ":CPU"          as CPU
   object ":TarjetaVideo" as TV
   object ":Monitor"      as MON

   Usuario -> GUI : oprimirTecla
   GUI -> SO   : "1: notificarTecla()"
   SO -> CPU   : "2: notificarTecla()"
   SO -> GUI   : "3: actualizar()"
   CPU -> TV   : "4: enviarCaracter()"
   TV -> MON   : "5: presentarCaracter()"
   @enduml

----
