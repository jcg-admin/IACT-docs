8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_09 — auditar acceso

 @startuml
 left to right direction

 actor "write_audit_event" as CALLER
 actor "AlertEngine" as Alertengine
 actor "AuditTable\n(append-only)" as Audittable

 rectangle "MOD_Permissions / Audit" {
   usecase "UC_PERM_09\nAuditar Acceso" as UC09
   usecase "PII Scan" as PII
   usecase "Sanitizar" as SAN
   usecase "registrar en tx caller" as INS
   usecase "Push alert post-COMMIT" as ALT
 }

 CALLER --> UC09
 UC09 ..> PII : <<include>>
 UC09 ..> SAN : <<include>>
 UC09 ..> INS : <<include>>
 UC09 ..> ALT : <<extend>>
 INS --> Audittable
 ALT --> Alertengine

 note bottom of UC09
   P-09 audit-or-abort:
   si emit falla, caller hace rollback.
 end note

 @enduml

