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
     database "bd_analytics" as BDA
     database "audit_log" as Audit
   }

   node "ldap-corporativo" as LDAP
   database "bd-operativa\n(read-only)" as BDO

   Supervisor -- PuestoSupervisor
   PuestoSupervisor --> VmIact : HTTPS (intranet)
   VmIact --> LDAP : LDAPS
   VmIact ..> BDO : SQL read-only\n(CNST_007)
   @enduml
