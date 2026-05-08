2.2 Roles en asociación — relación empleador-empleado
-----------------------------------------------------

Un caso de roles aplicado a IACT: la relación entre
``Supervisor`` (rol *aprobador*) y ``Operador`` (rol
*ejecutor*) en la asignación de funciones (UC_ACC_01):

.. uml::

   @startuml

   class User
   User "1\n<<approver>>" -- "0..*\n<<executor>>" User : assigns_functions
   note right of User
     Roles en la asignación
     de funciones:
       - approver  (supervisor)
       - executor  (operator or
                    access admin)
   end note
   @enduml
