8.4 Diagrama de estados Assignment AGR
======================================

.. uml::
 :caption: Estados Assignment(target=AGR)

 @startuml

 [*] --> ACTIVE : UC_PERM_01 / UC_ACC_04
 ACTIVE --> REVOKED : UC_PERM_02 / UC_ACC_02
 ACTIVE --> EXPIRED : cron (expires_at)
 REVOKED --> [*]
 EXPIRED --> [*]

 note right of REVOKED
   revoked_by_admin_id,
   revoke_reason
   Historial preservado (BR-009)
 end note

 @enduml
