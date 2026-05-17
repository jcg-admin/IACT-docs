17.19 Creación de objeto
------------------------

.. uml::

   @startuml
   participant "auth_app" as Auth

   create participant ":Sesion" as Sesion
   Auth -> Sesion : <<create>> nueva(user_id)
   @enduml
