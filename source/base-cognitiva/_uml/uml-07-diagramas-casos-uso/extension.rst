Extensión
---------

En lugar de sólo reabastecer la máquina de gaseosas para que
todas las marcas tengan la misma cantidad de latas, el
representante podría anotar aquellas que se venden mejor y
reabastecer acorde con ello. Podemos decir que el nuevo caso de
uso **extiende** al original dado que*agrega otros pasos* a la
secuencia del caso de uso original, que se conoce como **el caso
de uso base**.

La extensión sólo se puede realizar en puntos indicados de manera
específica dentro de la secuencia del caso de uso base. A estos
puntos se les conoce como **puntos de extensión**.

En el caso de uso *"Reabastecer"*, los nuevos pasos (*anotar las
ventas* y*abastecer de manera acorde*) se darían luego que el
representante haya abierto la máquina y esté listo para llenar
los compartimientos de las marcas. En este ejemplo, *el punto de
extensión es* **"Llenar los compartimientos"**.

Podrá concebir la extensión con una línea de dependencia (línea
discontinua con punta de flecha), junto con un estereotipo que
muestra ``<<extender>>`` (o ``<<extend>>``) entre paréntesis
angulares; el punto de extensión aparecerá debajo del nombre del
caso de uso.

.. uml::

   @startuml

   left to right direction
   actor Proveedor
   actor Recolector

   rectangle "Máquina de Gaseosas" {
     usecase "Reabastecer\n.. extension points ..\nLlenar los compartimientos"  as UC2
     usecase "Reabastecer de\nacuerdo a las ventas"                             as UC2X
     usecase "Recolectar el dinero"                                             as UC3
     usecase "Exhibir el interior"                                              as UCIN
     usecase "Cubrir el interior"                                               as UCOUT
   }
   Proveedor  --> UC2
   Recolector --> UC3
   UC2X ..> UC2 : <<extend>>\n(Llenar compartimientos)
   UC2 ..> UCIN  : <<include>>
   UC2 ..> UCOUT : <<include>>
   UC3 ..> UCIN  : <<include>>
   UC3 ..> UCOUT : <<include>>
   @enduml
