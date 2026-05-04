Estereotipos — extender UML
---------------------------

Notación: nombre entre ``«…»`` (paréntesis angulares dobles).

.. uml::

   @startuml

   interface IAuthenticable <<interface>> {
     + login()
     + logout()
   }
   @enduml

----
