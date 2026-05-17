11.7 Dependencia entre nodos
----------------------------

.. uml::

   @startuml

   node "vm-iact" as VmIact
   database "bd-operativa\n(read-only)" as BD_OPERATIVA

   VmIact ..> BD_OPERATIVA : depende de\n(CNST_007)
   @enduml
