17.18 Nota sobre dos participantes
----------------------------------

.. uml::

   @startuml
   participant "Browser" as Browser
   participant "auth_app" as Auth

   Browser -> Auth : POST /login

   note over Browser, Auth
     CNST_011 throttling:
     max 5 intentos / 5 min
   end note
   @enduml
