13.1 Ciclo simple — Sesion
--------------------------

.. uml::

   @startuml

   [*] --> Activa : login (CNST_002)
   Activa --> Caducada : timeout
   Activa --> Cerrada : logout
   Caducada --> [*]
   Cerrada --> [*]
   @enduml
