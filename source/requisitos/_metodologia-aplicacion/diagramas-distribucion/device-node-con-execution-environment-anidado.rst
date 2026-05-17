11.2 Device node con execution environment anidado
--------------------------------------------------

.. uml::

   @startuml

   node "vm-iact" as VmIact {
     node "Apache + mod_wsgi" as Apache
   }
   @enduml
