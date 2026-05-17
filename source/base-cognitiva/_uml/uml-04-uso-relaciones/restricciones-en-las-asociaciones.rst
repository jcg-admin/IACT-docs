Restricciones en las asociaciones
=================================

En ocasiones una asociación debe seguir cierta regla: esta regla
se indica al establecer una **restricción** junto a la línea de
asociación.

Por ejemplo, un ``Cajero`` atiende a un ``Cliente``, pero cada
``Cliente`` es atendido en el orden en que se encuentre en la
formación. Dicha restricción se puede realizar colocando la
palabra ``ordenado`` entre llaves ``{}`` junto a la clase
``Cliente``.

.. uml::

   @startuml

   class Cashier
   class Customer
   Cashier "1" -- "0..*" Customer : serves
   note bottom of Customer
     {ordered}
   end note
   @enduml

Otro tipo de restricción es la relación **OR** (distinguida como
``{Or}``) en una **línea discontinua** que conecte a dos líneas
de asociación. El siguiente diagrama modela a un estudiante de
educación media superior que elegirá entre un curso académico o
uno comercial.

.. uml::

   @startuml

   class Student
   class AcademicCourse
   class BusinessCourse

   Student --> AcademicCourse : enrolls in
   Student --> BusinessCourse : enrolls in
   AcademicCourse ..> BusinessCourse : <<{Or}>>
   @enduml
