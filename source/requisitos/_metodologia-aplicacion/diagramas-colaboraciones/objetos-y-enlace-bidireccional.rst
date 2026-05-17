14.1 Objetos y enlace bidireccional
-----------------------------------

.. uml::

   @startuml
   allowmixing

   object ":Supervisor" as Supervisor
   object ":Browser" as Browser

   Supervisor -- Browser : opera
   @enduml
