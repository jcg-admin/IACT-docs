5.1 Cadena de mando — Usuario supervisa Usuario
-----------------------------------------------

.. uml::

   @startuml

   class User
   User "1\n<<supervisor>>" -- "0..*\n<<supervised>>" User : supervises
   note right of User
     Reflexiva:
       - un Supervisor supervisa
         0..* Operadores;
       - un Operador es supervisado
         por 1 User.
     Roles distintos en la misma
     clase User.
   end note
   @enduml
