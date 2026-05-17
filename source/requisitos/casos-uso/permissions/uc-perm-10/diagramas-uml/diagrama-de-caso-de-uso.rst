8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_10 — consultar audit

 @startuml
 left to right direction

 actor "view_audit_log" as view_audit_log
 actor "ExportWorker" as Exportworker

 rectangle "MOD_Permissions / Audit" {
   usecase "UC_PERM_10\nList" as UcPerm10
   usecase "Detalle" as Detalle
   usecase "Aggregate" as Aggregate
   usecase "Export" as Export
   usecase "UC_PERM_09\nmeta-audit" as UcPerm09
 }

 view_audit_log --> UcPerm10
 view_audit_log --> Detalle
 view_audit_log --> Aggregate
 view_audit_log --> Export
 UcPerm10 ..> UcPerm09 : <<include>>
 Detalle ..> UcPerm09 : <<include>>
 Aggregate ..> UcPerm09 : <<include>>
 Export ..> UcPerm09 : <<include>>
 Export --> Exportworker
 Exportworker ..> UcPerm09 : <<include>>

 note bottom
   P-44: cada consulta del log
   se audita (audit del audit).
 end note

 @enduml

