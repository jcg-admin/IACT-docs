11.3 Artifact dentro de execution environment
---------------------------------------------

.. uml::

   @startuml

   node "vm-iact" {
     node "Apache + mod_wsgi" {
       artifact "iact.wsgi"
     }
   }
   @enduml
