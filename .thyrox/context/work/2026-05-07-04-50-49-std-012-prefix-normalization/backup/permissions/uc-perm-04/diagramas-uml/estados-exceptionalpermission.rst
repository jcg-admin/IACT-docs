8.4 Estados ExceptionalPermission
=================================

.. uml::
 :caption: Maquina de estados

 @startuml

 [*] --> ACTIVE : UC_PERM_03 / UC_ACC_08
 ACTIVE --> REVOKED : UC_PERM_04
 ACTIVE --> EXPIRED : cron job
 REVOKED --> [*]
 EXPIRED --> [*]

 note right of REVOKED
   revoked_by_admin_id !=
   NULL distingue de EXPIRED
 end note

 @enduml
