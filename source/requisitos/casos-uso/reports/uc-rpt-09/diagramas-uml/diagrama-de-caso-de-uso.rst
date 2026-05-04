8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_09 — filtros

 @startuml
 left to right direction
 actor "User autenticado" as UserAutenticado
 rectangle "MOD_Reports" {
   usecase "UC_RPT_09\nGestionar filtros" as UC09
   usecase "Aplicar filtro" as AplicacionFrontend
 }
 UserAutenticado --> UC09
 UserAutenticado --> APP
 @enduml

