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
 Backend -> Repo: actualizar Assignment REVOKED
 Backend -> Repo: registrar AuditEvent AGR_REVOKED
 Backend -> Repo: PermissionCache.invalidate
 Backend --> API: 200 OK con resumen
 API --> UiPerm: result
 UiPerm -> UiPerm: refresh catalogo (count -1)
 UiPerm --> Invoker: Toast confirmacion

 @enduml

