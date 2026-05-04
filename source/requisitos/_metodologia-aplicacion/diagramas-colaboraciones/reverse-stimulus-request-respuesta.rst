14.5 Reverse stimulus (request + respuesta)
-------------------------------------------

.. uml::

   @startuml
   allowmixing

   object ":auth_app" as Auth
   object ":ldap-corporativo" as LDAP

   Auth -> LDAP : "1: authenticate(user, pass)"
   LDAP --> Auth : "2: ok + atributos"
   @enduml
