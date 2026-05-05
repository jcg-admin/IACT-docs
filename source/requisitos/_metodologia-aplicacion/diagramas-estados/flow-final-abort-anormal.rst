13.9 Flow final — abort anormal
-------------------------------

.. uml::

   @startuml

   [*] --> Inicializada

   Inicializada --> Procesando : start
   Procesando --> Completada : ok

   state "AbortadaPorError" as ETL_ABORTADO #FFAAAA
   Procesando --> ETL_ABORTADO : error catastrofico
   ETL_ABORTADO : entry / registrar en audit_log
   ETL_ABORTADO --> [*]
   @enduml
