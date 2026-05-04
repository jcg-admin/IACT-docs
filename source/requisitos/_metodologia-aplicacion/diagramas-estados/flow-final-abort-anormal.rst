13.9 Flow final — abort anormal
-------------------------------

.. uml::

   @startuml

   [*] --> Inicializada

   Inicializada --> Procesando : start
   Procesando --> Completada : ok

   state "AbortadaPorError" as ABT #FFAAAA
   Procesando --> ABT : error catastrofico
   ABT : entry / registrar en audit_log
   ABT --> [*]
   @enduml
