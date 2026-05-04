.. _uc-perm-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_03 vs UC_ACC_08

 @startuml
 left to right direction

 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "grant_exceptional_permission" as grant_exceptional_permission
 actor "view_audit_log" as view_audit_log

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_08\nGrant excepcional" as ACC08
 }
 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_03\nGrant excepcional" as PERM03
 }
 rectangle "Backend compartido" {
   usecase "POST exceptional-permissions" as BE
 }

 grant_exceptional_permission --> ACC08
 grant_exceptional_permission --> PERM03
 ACC08 --> BE : delega
 PERM03 --> BE : delega
 BE --> view_audit_log : AuditEvent\nhigh-priority

 note bottom of BE
   Funcion: grant_exceptional_permission
   Mailbox HARD, justification + expires_at
   obligatorios, audit reforzado.
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_03 — flujo

 @startuml

 actor Invoker as Invoker
 participant "UI PERM" as UiPerm
 participant "API" as API
 participant "Backend\n(UC_ACC_08)" as Backend
 database "Repo" as Repo

 Invoker -> UiPerm: Selecciona functions + User +\n  expires_at + justification + TKT
 UiPerm -> API: GET preview-exceptional
 API --> UiPerm: preview con SoD
 UiPerm -> UiPerm: Modal con preview + warning\n  "high-priority audit"
 Invoker -> UiPerm: Confirma

 UiPerm -> API: POST exceptional-permissions/
 API -> Backend: delega flujo UC_ACC_08
 Backend -> Repo: INSERT ExceptionalPermission
 Backend -> Repo: INSERT InternalMessage (HARD)
 Backend -> Repo: INSERT AuditEvent\nEXCEPTIONAL_PERMISSION_GRANTED
 Backend -> Repo: PermissionCache.invalidate
 Backend --> API: 201 Created
 API --> UiPerm: result
 UiPerm -> UiPerm: Refresh catalogo
 UiPerm --> Invoker: Toast

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_03 — actividad

 @startuml

 start

 :Selecciona functions + User +
  expires_at + justification + TKT;
 :GET preview-exceptional;
 :Modal con preview SoD + warning
  high-priority audit;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 :POST exceptional-permissions/;
 note right
   Backend identico a UC_ACC_08
 end note

 if (Backend OK?) then (no)
   :Mostrar error segun status; stop
 else (si)
 endif

 :Refresh catalogo;
 :Toast confirmacion;

 stop

 @enduml

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
