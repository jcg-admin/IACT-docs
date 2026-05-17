Cambios de estado
=================

Puede mostrar los cambios de estado en un objeto en un diagrama
de colaboraciones.

En el rectángulo del objeto indique su estado. Agregue otro
rectángulo al diagrama que **haga las veces del objeto e indique
el estado modificado**. Conecte a los dos con*una línea
discontinua* y etiquétela con un estereotipo ``«se toma»`` (o
``«becomes»``).

.. uml::

   @startuml
   allowmixing

   object "GUI [Inicialización]" as GUI1
   object "GUI [Operación]"      as GUI2
   GUI1 ..> GUI2 : <<se toma>>
   @enduml
