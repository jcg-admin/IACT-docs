8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_10 — actores y casos asociados

 @startuml

 left to right direction

 actor "manage_own_views" as INVOKER
 actor "SavedViewRepo" as REPO <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_10\nGuardar Vista" as UC_RPT_10
   usecase "Validar limite\n< 30 vistas por User" as LIMIT
   usecase "Validar payload\n(filtros + columnas + orden\n+ group_by + chart)" as VALIDAR
   usecase "Persistir SavedView" as PERSIST
 }

 INVOKER --> UC_RPT_10
 UC_RPT_10 ..> LIMIT : <<include>>
 UC_RPT_10 ..> VALIDAR : <<include>>
 UC_RPT_10 ..> PERSIST : <<include>>

 PERSIST --> REPO

 note bottom of UC_RPT_10
   SavedView encapsula toda la
   configuracion (filtros, period
   relativo, columnas, orden,
   group_by, chart). Diferencia con
   UC_RPT_09: incluye presentacion.
 end note

 note bottom of LIMIT
   Hard limit: 30 vistas por User.
   Forza al User a curar su set
   activo.
 end note

 @enduml
