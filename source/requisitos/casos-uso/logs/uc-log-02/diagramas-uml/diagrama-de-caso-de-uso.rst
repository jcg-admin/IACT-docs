8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_02 — actores y casos asociados

 @startuml

 left to right direction

 ' TODO (use-case-view-uml07-rebuild Nivel A): completar
 ' actores (INVOKER + beneficiarios + Sistema), sub-usecases
 ' (validaciones, side-effects, audit emit), relaciones
 ' (`<<include>>`, `<<extend>>`) y notas referenciando BRs/CNSTs.
 ' Ver patron canonico en uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst.

 actor "INVOKER" as INVOKER

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs del ETL" as UC_LOG_02
 }

 INVOKER --> UC_LOG_02

 @enduml
