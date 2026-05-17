8.4 Diagrama de clases — vistas compartidas
===========================================

.. uml::
 :caption: ACC y PERM vistas — backing comun

 @startuml

 class "View_ACC" as ViewAcc
 class "View_PERM" as ViewPerm
 class "AccessService" as Accessservice {
   +assign_access_group(...)
 }
 class Assignment
 class AccessGroup
 class AuditEvent

 ViewAcc --> Accessservice : invoca
 ViewPerm --> Accessservice : invoca
 Accessservice --> Assignment : crea
 Accessservice --> AuditEvent : emite
 Assignment --> AccessGroup : referencia

 note right of Accessservice
   UC_ACC_04 backing
   compartido por ambas vistas
 end note

 @enduml
