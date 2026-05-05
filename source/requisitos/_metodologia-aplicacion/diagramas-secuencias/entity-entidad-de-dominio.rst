17.6 Entity (entidad de dominio)
--------------------------------

.. uml::

   @startuml
   participant "alr_app" as Alr
   entity "Alerta" as Alerta
   Alr -> Alerta : reconocer(supervisor)
   Alerta --> Alr : nuevo estado
   @enduml
