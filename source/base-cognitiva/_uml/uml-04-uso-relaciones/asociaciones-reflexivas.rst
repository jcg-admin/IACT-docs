Asociaciones reflexivas
=======================

En ocasiones, una clase tiene una asociación **consigo misma**.
Esto puede ocurrir cuando una clase tiene objetos que pueden
jugar diversos papeles.

Por ejemplo: un ``OcupanteDeAutomovil`` puede ser un
``Conductor`` o un ``Pasajero``. En el papel del conductor, el
``OcupanteDeAutomovil`` puede llevar a ninguno o más
``OcupanteDeAutomovil`` que jugarán el papel de pasajeros. Esto
se representa mediante el trazado de una línea de asociación a
partir del rectángulo de la clase hacia el mismo rectángulo, e
indicando los papeles, el nombre de la asociación, la dirección
y la multiplicidad.

.. uml::

   @startuml

   class OcupanteDeAutomovil
   OcupanteDeAutomovil "1\nconductor" -- "0..*\npasajero" OcupanteDeAutomovil : transporta
   @enduml

Una **asociación reflexiva** es una asociación binaria en la que
los objetos que participan en la relación pertenecen a la misma
clase: los objetos origen y destino son de la misma clase.

**Otro ejemplo — El jefe y sus subordinados:**

Piensa en cualquier trabajo: siempre hay un empleado que es jefe
de otros. Tanto el jefe como los trabajadores a su cargo son
empleados. Cada empleado existe independientemente del resto y
un empleado no está formado o compuesto por otros empleados. Las
etiquetas ``<<boss>>`` y ``<<subordinate>>`` se llaman **roles**
y se escriben en los extremos de la asociación para identificar
correcta y semánticamente qué papel juega cada objeto dentro de
la relación.

.. uml::

   @startuml

   class Empleado
   Empleado "1\n<<boss>>" -- "0..*\n<<subordinate>>" Empleado : supervisa
   @enduml
