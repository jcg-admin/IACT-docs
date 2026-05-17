14.6 Numeración anidada
-----------------------

.. uml::

   @startuml
   allowmixing

   object ":Browser" as Browser
   object ":auth_app" as Auth
   object ":Redis" as Redis

   Browser -> Auth : "1: POST /login"
   Auth -> Redis : "1.1: crear_sesion()"
   Redis --> Auth : "1.2: session_id"
   Auth --> Browser : "1.3: 302 panel"
   @enduml
