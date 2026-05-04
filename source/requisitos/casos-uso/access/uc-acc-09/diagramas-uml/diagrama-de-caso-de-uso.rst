8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_09 — actores y casos asociados

 @startuml
 left to right direction

 actor "view_audit_log" as INVOKER
 actor "Sistema" as Sistema

 rectangle "MOD_Access" {
   usecase "UC_ACC_09\nAuditar Cambios" as UC09
   usecase "Listar eventos\npaginado" as LST
   usecase "Ver detalle" as DET
   usecase "Agregar (count\npor categoria)" as AGG
   usecase "Audit P-16\nselectivo" as AUDS
 }

 INVOKER --> UC09
 UC09 ..> LST : <<extend>>
 UC09 ..> DET : <<extend>>
 UC09 ..> AGG : <<extend>>
 LST ..> AUDS : <<extend (filter\ntarget_user_id)>>
 DET ..> AUDS : <<include>>
 Sistema --> AUDS

 note bottom of UC09
   Subset de UC_AUD_*
   filtrado por
   ACCESS_EVENT_TYPES
 end note

 @enduml

