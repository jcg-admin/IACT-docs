17.20 Destrucción de objeto
---------------------------

.. uml::

   @startuml
   participant "auth_app" as Auth
   participant ":Sesion" as Sesion

   Auth -> Sesion : caducar()
   destroy Sesion
   @enduml
