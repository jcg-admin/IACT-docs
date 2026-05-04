11.6 Asociación dirigida
------------------------

.. uml::

   @startuml

   node "vm-iact" as VmIact
   node "ldap-corporativo" as LDAP

   VmIact --> LDAP : LDAPS\n(autenticacion)
   @enduml
