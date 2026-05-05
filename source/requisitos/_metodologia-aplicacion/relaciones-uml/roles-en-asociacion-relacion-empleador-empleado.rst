2.2 Roles en asociación — relación empleador-empleado
-----------------------------------------------------

Un caso de roles aplicado a IACT: la relación entre
``Supervisor`` (rol *aprobador*) y ``Operador`` (rol
*ejecutor*) en la asignación de funciones (UC_ACC_01):

.. uml::

   @startuml

   class Usuario
   Usuario "1\n<<aprobador>>" -- "0..*\n<<ejecutor>>" Usuario : asigna_funciones
   note right of Usuario
     Roles en la asignación
     de funciones:
       - aprobador  (supervisor)
       - ejecutor   (operador o
                    admin de acceso)
   end note
   @enduml
