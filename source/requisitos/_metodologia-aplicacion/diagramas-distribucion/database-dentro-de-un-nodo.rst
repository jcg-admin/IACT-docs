11.4 Database dentro de un nodo
-------------------------------

.. uml::

   @startuml

   node "vm-iact" {
     database "bd_analytics" as BDA
     database "audit_log" as Audit
     database "Redis" as Redis
   }
   @enduml
