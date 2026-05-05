Representación de los resultados
--------------------------------

Un mensaje podría ser una petición a un objeto para que realice
un cálculo y devuelva un valor. Un objeto ``Cliente`` podría
solicitar a un objeto ``Calculadora`` que calcule el precio total.

Sintaxis: el nombre del valor devuelto a la izquierda, seguido
de ``:=``, luego el nombre de la operación y las cantidades:

::

 precioTotal := calcular(precioElemento, impuesto)

.. uml::

   @startuml
   allowmixing

   object ":Cliente"      as C
   object ":Calculadora"  as Calc
   C -> Calc : "1: precioTotal := calcular(precioElemento, impuesto)"
   @enduml

A la parte que está a la derecha de ``:=`` se le conoce como
**firma del mensaje**.
