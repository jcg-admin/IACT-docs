8.4 Diagrama de estado del trend
================================

.. uml::
 :caption: Estado de carga del trend

 @startuml
 [*] --> Empty
 Empty --> Loading : query
 Loading --> Loaded : rows OK
 Loading --> Stale : ETL atrasado
 Loading --> Error : timeout
 Loaded --> Empty : period change
 Stale --> Loaded : ETL recuperado
 Error --> Loading : retry
 @enduml
