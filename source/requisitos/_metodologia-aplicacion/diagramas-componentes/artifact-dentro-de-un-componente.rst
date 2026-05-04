16.5 Artifact dentro de un componente
-------------------------------------

.. uml::

   @startuml

   component "iact.wsgi" {
     artifact "auth_app" as Auth
     artifact "perm_app" as Perm
     artifact "rpt_app" as Rpt
   }
   @enduml
