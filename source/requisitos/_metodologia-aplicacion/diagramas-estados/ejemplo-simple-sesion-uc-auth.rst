2.2 Ejemplo simple — Sesion (UC_AUTH)
-------------------------------------

.. uml::

   @startuml

   [*] --> Inactiva
   Inactiva --> Activa : login()
   Activa --> Inactiva : logout()
   Activa --> [*]
   @enduml

----
