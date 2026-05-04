Diagramas híbridos
==================

Un diagrama híbrido contiene símbolos de diferentes tipos.

En el diagrama de creación de documento, se podría depurar la
actividad de impresión: en lugar de sólo mostrar *"Imprimir
documento"*, se transmite una señal a un objeto ``Impresora``
que la recibe y la imprime.

.. uml::

   @startuml

   start
   :Guardar archivo;
   ->Enviar a impresora>
   stop

   note right
     La impresora recibe la señal
     y ejecuta la impresión.
   end note
   @enduml

Otra posibilidad: mostrar un diagrama de actividades para una
operación **dentro de un símbolo de objeto**, y el objeto que
recibe una petición para ejecutar la operación:

.. uml::

   @startuml

   allowmixing
   actor Usuario
   object Calculadora
   Usuario -> Calculadora : calcularFib(n)
   note right of Calculadora
     (interior)
     start \n Respuesta1 := 1 \n
     Contador := 1 \n ... \n
     mostrar(Respuesta, Contador) \n stop
   end note
   @enduml

----
