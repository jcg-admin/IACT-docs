16.7 Realización de interfaz
----------------------------

.. uml::

   @startuml

   interface ISecurity
   component "perm_app" as Perm

   Perm ..|> ISecurity : implementa
   @enduml
