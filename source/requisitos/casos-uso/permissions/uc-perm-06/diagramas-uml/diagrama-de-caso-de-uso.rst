8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_06 — composicion AGR

 @startuml
 left to right direction

 actor "assign_functions_to_group" as assign_functions_to_group
 actor "Users con AGR" as REPOSITORIO_USUARIOS
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_06\nComposicion AGR" as UC_PERM_06
   usecase "Validar separacion\ncascade" as VALIDAR_SEPARATION_RULES
   usecase "registrar add" as RegistrarDatos
   usecase "DELETE remove" as EliminarRegistro
   usecase "Audit COMPOSITION_CHANGED" as AuditEmitter
 }

 assign_functions_to_group --> UC_PERM_06
 UC_PERM_06 ..> VALIDAR_SEPARATION_RULES : <<include>>
 UC_PERM_06 ..> INS : <<include>>
 UC_PERM_06 ..> DEL : <<include>>
 UC_PERM_06 ..> EMI : <<include>>
 UC_PERM_06 ..> REPOSITORIO_USUARIOS : cascade
 EMI --> view_audit_log

 note bottom of UC_PERM_06
   Cambios en composicion afectan
   a todos los Users con el AGR
 end note

 @enduml

