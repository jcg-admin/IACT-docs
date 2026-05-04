11.5 Asociación bidireccional entre nodos
-----------------------------------------

.. uml::

   @startuml

   node "puesto-supervisor" as PuestoSupervisor
   node "vm-iact" as VmIact

   PuestoSupervisor -- VmIact : HTTPS (intranet)
   @enduml
