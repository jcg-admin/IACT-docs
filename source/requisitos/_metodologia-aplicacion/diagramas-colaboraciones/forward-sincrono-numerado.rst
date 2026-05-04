14.3 Forward síncrono numerado
------------------------------

.. uml::

   @startuml
   allowmixing

   object ":Browser" as Browser
   object ":auth_app" as Auth

   Browser -> Auth : "1: POST /login"
   @enduml
