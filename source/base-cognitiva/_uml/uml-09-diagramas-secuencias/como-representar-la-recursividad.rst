Cómo representar la recursividad
================================

Un objeto cuenta con una operación que se invoca a sí misma. A
esto se le conoce como **recursividad**.

Por ejemplo: uno de los objetos en su sistema es una calculadora,
y una de sus operaciones es el cálculo de intereses. Para
calcular el interés compuesto para un periodo que incluya varios
periodos, la operación tendrá que invocarse a sí misma varias
veces.

Para representar esto en UML, se dibuja una **flecha de mensaje
fuera de la activación** que signifique la operación, y un
**pequeño rectángulo sobrepuesto** en la activación. La flecha
apunta al pequeño rectángulo, y otra flecha regresa al objeto
que inició la recursividad.

.. uml::

   @startuml

   participant ":Calculadora" as C
   activate C
   C -> C : calcularInteres(periodo)
   activate C
   C -> C : calcularInteres(periodo-1)
   activate C
   C --> C : resultado
   deactivate C
   C --> C : resultado
   deactivate C
   deactivate C
   @enduml

----
