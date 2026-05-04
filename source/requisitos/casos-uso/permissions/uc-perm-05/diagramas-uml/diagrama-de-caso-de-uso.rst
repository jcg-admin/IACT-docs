8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_05 — gestion catalogo AGR

 @startuml
 left to right direction

 actor "create_function_group" as create_function_group
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_05\nCreate AGR" as UCCRE
   usecase "UC_PERM_05\nModify AGR" as UCMOD
   usecase "UC_PERM_05\nRetire AGR" as UCRET
   usecase "AuditEvent" as AuditEmitter
 }

 create_function_group --> UCCRE
 create_function_group --> UCMOD
 create_function_group --> UCRET
 UCCRE ..> EMI : <<include>>
 UCMOD ..> EMI : <<include>>
 UCRET ..> EMI : <<include>>
 EMI --> view_audit_log

 @enduml

