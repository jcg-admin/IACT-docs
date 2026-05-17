17.7 Activación inline
----------------------

.. uml::

   @startuml
   actor S as Supervisor
   participant "auth_app" as Auth
   database "Redis" as Redis

   S -> Auth ++ : POST /login
   Auth -> Redis : crear sesion (CNST_002)
   Redis --> Auth : ok
   Auth --> S -- : 302 panel
   @enduml
