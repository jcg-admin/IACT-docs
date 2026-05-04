Decisiones
==========

Una secuencia de actividades llegará a un punto donde se realice
alguna **decisión**. Las condiciones le llevarán por un camino y
otras por otro (mutuamente exclusivas).

Puede representar un punto de decisión de dos formas:

- mostrar las rutas posibles que parten directamente de una
  actividad;
- llevar la transición hacia un **rombo** y que de allí salgan
  las rutas.

Indica la condición con una instrucción **entre corchetes** junto
a la ruta correspondiente.

.. uml::

   @startuml

   start
   :Verificar valor;
   if ([valor > 0]) then (sí)
     :Procesar positivo;
   else (no)
     :Procesar negativo;
   endif
   stop
   @enduml

----
