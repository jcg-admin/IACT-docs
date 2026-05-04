11.8 Puertos en frontera
------------------------

.. uml::

   @startuml

   node "vm-iact" as VmIact {
     port p_https
     port p_ldap
   }
   node "puesto-supervisor" as PuestoSupervisor
   node "ldap-corporativo" as LDAP

   PuestoSupervisor -- p_https
   p_ldap -- LDAP
   @enduml
