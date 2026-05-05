14.9 Cambio de estado anotado
-----------------------------

.. uml::

   @startuml
   allowmixing

   object ":auth_app" as Auth
   object ":Sesion" as Sesion

   Auth -> Sesion : "1: caducar()"
   note right of Sesion
     estado: activa → caducada
     CNST_002
   end note
   @enduml
