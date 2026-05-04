8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_06 — composicion AGR

 @startuml
 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "Users con AGR" as USERS
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_06\nComposicion AGR" as UC06
   usecase "Validar SoD\ncascade" as VSOD
   usecase "registrar add" as RegistrarDatos
   usecase "DELETE remove" as EliminarRegistro
   usecase "Audit COMPOSITION_CHANGED" as AuditEmitter
 }

 assign_functions_to_group --> UC06
 UC06 ..> VSOD : <<include>>
 UC06 ..> INS : <<include>>
 UC06 ..> DEL : <<include>>
 UC06 ..> EMI : <<include>>
 UC06 ..> USERS : cascade
 EMI --> view_audit_log

 note bottom of UC06
   Cambios en composicion afectan
   a todos los Users con el AGR
 end note

 @enduml

