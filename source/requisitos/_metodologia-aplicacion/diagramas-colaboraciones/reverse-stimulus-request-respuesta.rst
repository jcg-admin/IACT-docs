14.5 Reverse stimulus (request + respuesta)
-------------------------------------------

.. uml::

   @startuml
   allowmixing

   object ":auth_app" as Auth
   object ":ldap-corporativo" as LDAP_CORPORATIVO

   Auth -> LDAP_CORPORATIVO : "1: authenticate(user, pass)"
   LDAP_CORPORATIVO --> Auth : "2: ok + atributos"
   @enduml
