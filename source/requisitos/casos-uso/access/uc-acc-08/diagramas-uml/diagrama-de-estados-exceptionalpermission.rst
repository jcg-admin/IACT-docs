8.4 Diagrama de estados — ExceptionalPermission
===============================================

.. uml::
 :caption: Estados de ExceptionalPermission

 @startuml

 [*] --> ACTIVE : UC_ACC_08\n(grant)

 ACTIVE --> EXPIRED : cron job\n(marca_tiempo_actual > expires_at)
 ACTIVE --> REVOKED : revocacion\nexplicita
 EXPIRED --> [*]
 REVOKED --> [*]

 note right of EXPIRED
   AuditEvent
   EXCEPTIONAL_PERMISSION_EXPIRED
   automatico
 end note

 @enduml
