17.2 Participante (servicio Django)
-----------------------------------

.. uml::

   @startuml
   participant "rpt_app" as Rpt
   participant "perm_app" as Perm
   Rpt -> Perm : verificar(user, "exportar")
   Perm --> Rpt : ok
   @enduml
