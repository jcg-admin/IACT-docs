Responsabilidades y restricciones
=================================

En un área bajo la lista de operaciones, podrá mostrar la
**responsabilidad** de la clase. La responsabilidad es una
descripción de **lo que hará la clase** — es decir, lo que sus
atributos y operaciones intentan realizar en conjunto.

Una lavadora, por ejemplo, tiene la responsabilidad de recibir
ropa sucia y dar por resultado ropa limpia.

Indicará las responsabilidades en un área inferior a la que
contiene las operaciones.

.. uml::

   @startuml

   class Lavadora {
     marca : String
     capacidad : Float
     --
     agregarRopa()
     activarse()
     sacarRopa()
     --
     responsabilidades:
     -- Recibir ropa sucia
     -- Lavar y enjuagar
     -- Entregar ropa limpia
   }
   @enduml

La idea es incluir información suficiente para describir una
clase de forma inequívoca.

Una manera más formal es agregar una **restricción**, un
**texto libre bordeado por llaves**: este texto especifica una o
varias reglas que sigue la clase. Para "restringir" el atributo
``capacidad`` de la clase ``Lavadora``, escribirá
``{capacidad = 7, 8 o 9 Kg}`` junto al símbolo de la clase.

.. uml::

   @startuml

   class Lavadora {
     marca : String
     capacidad : Float
     --
     agregarRopa()
     activarse()
   }
   note right of Lavadora
     {capacidad = 7, 8 o 9 Kg}
   end note
   @enduml

UML proporciona otra forma — aún más formal — de agregar
restricciones, con todo un lenguaje conocido como **OCL** (Object
Constraint Language). OCL cuenta con su propio conjunto de
reglas, términos y operadores, lo que lo convierte en una
herramienta avanzada y, en ocasiones, útil.

----
