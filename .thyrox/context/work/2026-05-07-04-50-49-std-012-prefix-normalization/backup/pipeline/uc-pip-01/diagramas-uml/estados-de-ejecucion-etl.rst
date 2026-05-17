8.3 Estados de ejecucion ETL
=============================

.. uml::

 @startuml
 [*] --> en_ejecucion : Disparador ETL invoca SP
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*]
 @enduml

