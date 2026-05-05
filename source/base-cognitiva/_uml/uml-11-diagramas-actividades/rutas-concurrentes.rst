Rutas concurrentes
==================

Puede separar una transición en dos rutas que se ejecuten al
mismo tiempo (concurrentemente) y luego se reúnan.

Para representar esta división, utiliza una **línea gruesa
perpendicular** a la transición y las rutas parten de ella. Para
representar la reincorporación, ambas rutas apuntarán a otra
línea gruesa.

.. uml::

   @startuml

   start
   fork
     :Ruta A — Actividad 1;
     :Ruta A — Actividad 2;
   fork again
     :Ruta B — Actividad 1;
     :Ruta B — Actividad 2;
   end fork
   :Reunión;
   stop
   @enduml
