8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_09 — actores y casos asociados

 @startuml
 left to right direction

 actor "view_audit_log" as INVOKER
 actor "Sistema" as Sistema

 rectangle "MOD_Access" {
   usecase "UC_ACC_09\nAuditar Cambios" as UC_ACC_09
   usecase "Listar eventos\npaginado" as VistaListado
   usecase "Ver detalle" as VistaDetalle
   usecase "Agregar (count\npor categoria)" as AgregadorConteo
   usecase "Audit P-16\nselectivo" as AUDITORIA_SELECTIVA
 }

 INVOKER --> UC_ACC_09
 UC_ACC_09 ..> LST : <<extend>>
 UC_ACC_09 ..> DET : <<extend>>
 UC_ACC_09 ..> AGG : <<extend>>
 LST ..> AUDITORIA_SELECTIVA : <<extend (filter\ntarget_user_id)>>
 DET ..> AUDITORIA_SELECTIVA : <<include>>
 Sistema --> AUDITORIA_SELECTIVA

 note bottom of UC_ACC_09
   Subset de UC_AUD_*
   filtrado por
   ACCESS_EVENT_TYPES
 end note

 @enduml

