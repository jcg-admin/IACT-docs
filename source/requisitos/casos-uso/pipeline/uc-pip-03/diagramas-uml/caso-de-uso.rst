8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_data_availability" as view_data_availability
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_03\nDisponibilidad\nde Datos" as UC03
 }
 view_data_availability --> UC03
 @enduml

