8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_05 — gestion catalogo AGR

 @startuml
 left to right direction

 actor "create_function_group" as create_function_group
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_05\nCreate AGR" as CREAR_AGRUPADOR
   usecase "UC_PERM_05\nModify AGR" as MODIFICAR_AGRUPADOR
   usecase "UC_PERM_05\nRetire AGR" as RETIRAR_AGRUPADOR
   usecase "AuditEvent" as AuditEmitter
 }

 create_function_group --> CREAR_AGRUPADOR
 create_function_group --> MODIFICAR_AGRUPADOR
 create_function_group --> RETIRAR_AGRUPADOR
 CREAR_AGRUPADOR ..> EMI : <<include>>
 MODIFICAR_AGRUPADOR ..> EMI : <<include>>
 RETIRAR_AGRUPADOR ..> EMI : <<include>>
 EMI --> view_audit_log

 @enduml

