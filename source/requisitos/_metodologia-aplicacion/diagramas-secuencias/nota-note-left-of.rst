17.17 Nota ``note left of``
---------------------------

.. uml::

   @startuml
   participant "auth_app" as Auth
   database "Redis" as Redis

   Auth -> Redis : crear sesion
   note left of Redis
     CNST_002:
     una sola sesion activa
     por usuario
   end note
   @enduml
