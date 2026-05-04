8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "search_audit_log" as search_audit_log
 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar" as UC02
   usecase "UC_PERM_09\nMeta-audit" as UcPerm09
 }
 search_audit_log --> UC02
 UC02 ..> UcPerm09 : <<include>>
 @enduml

