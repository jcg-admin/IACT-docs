8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_08 — actores y casos asociados

 @startuml

 left to right direction

 ' TODO (use-case-view-uml07-rebuild Nivel A): completar
 ' actores (INVOKER + beneficiarios + Sistema), sub-usecases
 ' (validaciones, side-effects, audit emit), relaciones
 ' (`<<include>>`, `<<extend>>`) y notas referenciando BRs/CNSTs.
 ' Ver patron canonico en uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst.

 actor "INVOKER" as INVOKER

 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nVer Propio Dashboard" as UC_OPR_08
 }

 INVOKER --> UC_OPR_08

 @enduml
