8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_audit_log" as view_audit_log
 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nConsultar Auditoria" as UC_AUD_01
   usecase "UC_PERM_09\nMeta-audit" as UcPerm09
 }
 view_audit_log --> UC_AUD_01
 UC_AUD_01 ..> UcPerm09 : <<include>>
 @enduml

