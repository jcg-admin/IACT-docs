8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_03 — flujo

 @startuml

 actor Invoker as Invoker
 participant "UI PERM" as UiPerm
 participant "API" as EndpointAPI
 participant "Backend\n(UC_ACC_08)" as Backend
 database "Repo" as Repo

 Invoker -> UiPerm: Selecciona functions + User +\n  expires_at + justification + TKT
 UiPerm -> API: GET preview-exceptional
 API --> UiPerm: preview con separacion
 UiPerm -> UiPerm: Modal con preview + warning\n  "high-priority audit"
 Invoker -> UiPerm: Confirma

 UiPerm -> API: POST exceptional-permissions/
 API -> Backend: delega flujo UC_ACC_08
 Backend -> Repo: registrar ExceptionalPermission
 Backend -> Repo: registrar InternalMessage (HARD)
 Backend -> Repo: registrar AuditEvent\nEXCEPTIONAL_PERMISSION_GRANTED
 Backend -> Repo: PermissionCache.invalidate
 Backend --> API: 201 Created
 API --> UiPerm: result
 UiPerm -> UiPerm: Refresh catalogo
 UiPerm --> Invoker: Toast

 @enduml

