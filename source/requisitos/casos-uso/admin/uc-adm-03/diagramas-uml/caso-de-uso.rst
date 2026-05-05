8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "admin_sistema\n(AGR-009)" as admin
 rectangle "MOD_Admin — UC_ADM_03" {
   usecase "Agregar funcion\na AGR sistema\nassign_functions_to_group" as Add
   usecase "Remover funcion\nde AGR sistema\nassign_functions_to_group" as Remove
   usecase "Ver composicion" as View
   usecase "Ver impacto" as Impact
   usecase "Recalcular\neffective_set" as Recalc
 }
 admin --> Add
 admin --> Remove
 admin --> View
 admin --> Impact
 Add ..> Recalc : <<include>>
 Remove ..> Recalc : <<include>>
 @enduml
