17.11 Autonumber con offset
---------------------------

.. uml::

   @startuml
   autonumber

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth

   Supervisor -> Browser : envia credenciales
   Browser -> Auth : POST /login
   Auth --> Browser : 302 Redirect
   @enduml
