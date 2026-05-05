8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_03 — actores y casos asociados

 @startuml

 left to right direction

 ' TODO (use-case-view-uml07-rebuild Nivel A): completar
 ' actores (INVOKER + beneficiarios + Sistema), sub-usecases
 ' (validaciones, side-effects, audit emit), relaciones
 ' (`<<include>>`, `<<extend>>`) y notas referenciando BRs/CNSTs.
 ' Ver patron canonico en uc-acc-01/diagramas-uml/diagrama-de-caso-de-uso.rst.

 actor "INVOKER" as INVOKER

 rectangle "MOD_Admin" {
   usecase "UC_ADM_03\nGestionar Catalogo de Agrupadores del Sistema" as UC_ADM_03
 }

 INVOKER --> UC_ADM_03

 @enduml
