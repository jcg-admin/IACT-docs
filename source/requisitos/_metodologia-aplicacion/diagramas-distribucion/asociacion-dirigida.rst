11.6 Asociación dirigida
------------------------

.. uml::

   @startuml

   node "vm-iact" as VmIact
   node "ldap-corporativo" as LDAP_CORPORATIVO

   VmIact --> LDAP_CORPORATIVO : LDAPS\n(autenticacion)
   @enduml
