8.4 Diagrama de estados ExceptionalPermission
=============================================

.. uml::
 :caption: Estados ExceptionalPermission

 @startuml

 [*] --> ACTIVE : UC_PERM_03 / UC_ACC_08
 ACTIVE --> EXPIRED : cron (NOW > expires_at)
 ACTIVE --> REVOKED : UC_PERM_04
 EXPIRED --> [*]
 REVOKED --> [*]

 note right of EXPIRED
   AuditEvent
   EXCEPTIONAL_PERMISSION_EXPIRED
 end note

 @enduml
