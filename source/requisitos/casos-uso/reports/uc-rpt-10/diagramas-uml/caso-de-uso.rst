8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User autenticado" as UserAutenticado
 rectangle "MOD_Reports" {
   usecase "UC_RPT_10\nGuardar Vista" as UC10
   usecase "Aplicar vista" as AplicacionFrontend
   usecase "Clone" as Clone
 }
 UserAutenticado --> UC10
 UserAutenticado --> APP
 UserAutenticado --> Clone
 @enduml

