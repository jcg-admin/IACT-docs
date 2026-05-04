8.3 Estado de frescura de datos
================================

.. uml::

 @startuml
 [*] --> fresco : ETL exitoso (< 12 hs)
 fresco --> degradado : > 12 hs sin actualizacion
 degradado --> vencido : > 24 hs sin actualizacion
 vencido --> fresco : ETL exitoso
 degradado --> fresco : ETL exitoso
 @enduml

