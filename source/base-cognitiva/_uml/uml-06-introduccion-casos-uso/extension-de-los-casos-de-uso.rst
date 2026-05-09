Extensión de los casos de uso
=============================

Es posible volver a utilizar un caso de uso de una forma distinta
a una inclusión. En ocasiones crearemos un caso de uso
**agregándole algunos pasos a un caso de uso existente**.

Volviendo al caso de uso *"Reabastecer"*: antes de colocar nuevas
latas de gaseosas en la máquina, suponga que el representante del
proveedor nota las marcas que se han vendido bien, así como las
que no se han vendido tan bien. En lugar de sólo reabastecer
todas las marcas, el representante podría sacar aquellas que no
se han vendido bien y reemplazarlas por latas de las marcas que
han probado ser más populares.

Si agregamos estos pasos a *"Reabastecer"*, tendremos un nuevo
caso de uso que llamaríamos **"Reabastecer de acuerdo a las
ventas"**. Este nuevo caso de uso es una*extensión del
original*, acción a la que se le conoce como**extensión de un
caso de uso**.

.. uml::

   @startuml

   left to right direction
   actor Proveedor

   rectangle "Máquina de Gaseosas" {
     usecase "Reabastecer"                       as UC2
     usecase "Reabastecer de acuerdo a ventas"   as UC2X
   }
   Proveedor --> UC2X
   UC2X ..> UC2 : <<extend>>
   @enduml
