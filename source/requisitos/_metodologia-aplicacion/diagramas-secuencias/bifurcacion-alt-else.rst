17.12 Bifurcación ``alt`` / ``else``
------------------------------------

.. uml::

   @startuml
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "audit_log" as Audit

   Auth -> Auth : validar formato

   alt [credenciales validas]
     Auth -> LDAP : authenticate
     LDAP --> Auth : OK
   else [credenciales invalidas]
     Auth ->> Audit : registrar intento (CNST_011)
   end
   @enduml
