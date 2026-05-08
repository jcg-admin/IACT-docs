4.2 Búsqueda de Reporte por nombre programado
---------------------------------------------

.. uml::

   @startuml

   class User
   class Report
   User "1" -[#black]- "(name)" Report : recovers_scheduled
   note right of Report
     UC_RPT_08 — el usuario
     recupera el reporte programado
     por su nombre (único en
     su contexto de usuario).
   end note
   @enduml
