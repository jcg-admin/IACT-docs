.. _uc-perm-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_02 vista del flujo
           UC_ACC_02 sobre AGR

 @startuml
 left to right direction

 actor "revoke_function_group" as revoke_function_group
 actor "revoke_function_group" as revoke_function_group

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_02\nRevocar\n(generico)" as ACC02
 }
 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar AGR\n(catalogo)" as PERM02
 }
 cloud "Backend compartido" {
   usecase "DELETE /api/users/{id}/\naccess-groups/{agr_id}/" as BE
 }

 revoke_function_group --> ACC02
 revoke_function_group --> PERM02
 ACC02 --> BE : delega
 PERM02 --> BE : delega

 note right of BE
   Funcion: revoke_function_group
   AuditEvent: AGR_REVOKED
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_02 — flujo

 @startuml

 actor Invoker as Invoker
 participant "UI PERM" as UiPerm
 participant "API" as API
 participant "Backend\n(UC_ACC_02 sobre AGR)" as Backend
 database "Repo" as Repo

 Invoker -> UiPerm: Identifica User + AGR
 UiPerm -> API: GET preview-revoke
 API -> Repo: dry-run validations
 API --> UiPerm: preview con warnings

 UiPerm -> UiPerm: Modal expandido
 alt warnings criticos
   UiPerm -> UiPerm: Doble confirmacion (escribir)
 end
 Invoker -> UiPerm: Confirma

 UiPerm -> API: DELETE /api/users/{id}/\n  access-groups/{agr_id}/
 API -> Backend: delega flujo UC_ACC_02
 Backend -> Repo: UPDATE Assignment REVOKED
 Backend -> Repo: INSERT AuditEvent AGR_REVOKED
 Backend -> Repo: PermissionCache.invalidate
 Backend --> API: 200 OK con resumen
 API --> UiPerm: result
 UiPerm -> UiPerm: refresh catalogo (count -1)
 UiPerm --> Invoker: Toast confirmacion

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_02 — actividad

 @startuml

 start

 :Identifica User + AGR a revocar;
 :GET preview-revoke;
 :Modal con composicion + warnings;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 if (Warnings criticos?) then (si)
   :Doble confirmacion (escribir);
   if (Confirma literal?) then (no)
     :Cancela; stop
   else (si)
   endif
 else (no)
 endif

 :DELETE backend;
 note right
   Flujo identico a UC_ACC_02
   sobre target_type=AGR
 end note

 if (Backend OK?) then (no)
   :Mostrar error; stop
 else (si)
 endif

 :Refresh catalogo (count -1);
 :Toast confirmacion;

 stop

 @enduml

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
