17.1 Actor humano
-----------------

.. uml::

   @startuml
   actor "Supervisor" as Supervisor
   participant "auth_app" as Auth
   Supervisor -> Auth : envia credenciales
   @enduml
