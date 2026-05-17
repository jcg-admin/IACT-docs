11.9 Vista combinada — IACT minimalista
---------------------------------------

.. uml::

   @startuml
   title IACT — Deployment minimalista

   actor Supervisor

   node "puesto-supervisor" as PuestoSupervisor {
     artifact "Browser"
   }

   node "vm-iact" as VmIact {
     node "Apache + mod_wsgi" {
       artifact "iact.wsgi"
     }
     database "Redis" as Redis
     database "bd_analytics" as BD_ANALYTICS
     database "audit_log" as Audit
   }

   node "ldap-corporativo" as LDAP_CORPORATIVO
   database "bd-operativa\n(read-only)" as BD_OPERATIVA

   Supervisor -- PuestoSupervisor
   PuestoSupervisor --> VmIact : HTTPS (intranet)
   VmIact --> LDAP_CORPORATIVO : LDAPS
   VmIact ..> BD_OPERATIVA : SQL read-only\n(CNST_007)
   @enduml
