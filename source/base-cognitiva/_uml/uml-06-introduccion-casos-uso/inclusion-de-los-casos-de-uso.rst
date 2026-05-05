Inclusión de los casos de uso
=============================

Tal vez distinguió ciertos pasos en común. ¿Podríamos eliminar la
duplicación de pasos de un caso de uso al otro? Tomar cada
secuencia de pasos en común y conformar un **caso de uso
adicional** a partir de ellos.

Combinemos los pasos necesarios para *"quitar el seguro"* y
*"abrir la máquina"* y llamémoslos **"Exhibir el interior"**, y
los pasos *"cerrar la máquina"* y *"asegurarla"* en otro caso de
uso llamado **"Cubrir el interior"**.

- El caso de uso **"Reabastecer"** iniciaría con el caso de uso
  *"Exhibir el interior"*, luego el representante del proveedor
  seguiría los pasos ya indicados, y concluiría con el caso de
  uso *"Cubrir el interior"*.
- De forma similar, el caso de uso **"Recolectar dinero"**
  iniciaría con *"Exhibir el interior"*, procedería como se
  indicó, y finalizaría con el caso de uso *"Cubrir el
  interior"*.

De tal manera que *"Reabastecer"* y *"Recolectar dinero"*
**incluyen** los nuevos casos de uso. Esta técnica de
**aprovechamiento de un caso de uso** se le conoce como
**inclusión de un caso de uso**.

.. uml::

   @startuml

   left to right direction
   actor Proveedor
   actor Recolector

   rectangle "Máquina de Gaseosas" {
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
     usecase "Exhibir el interior"  as UCIN
     usecase "Cubrir el interior"   as UCOUT
   }
   Proveedor  --> UC2
   Recolector --> UC3
   UC2 ..> UCIN  : <<include>>
   UC2 ..> UCOUT : <<include>>
   UC3 ..> UCIN  : <<include>>
   UC3 ..> UCOUT : <<include>>
   @enduml

La inclusión de un caso de uso también se conoce como **"usar"
un caso de uso**. El término *incluir* tiene dos ventajas:

1. Es más claro: los pasos en un caso de uso **incluyen** los
   de otro.
2. Se evita la confusión potencial de las palabras *"usar"* y
   *"uso"* en un contexto tan estrecho. Así, no tendremos que
   decir *"promover el uso mediante el uso reiterativo de un
   caso de uso"*.

Promover el uso, mediante la **inclusión** reiterativa de un
caso de uso.
