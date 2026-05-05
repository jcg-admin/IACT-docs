8.2 Diagrama de secuencia (vista PERM)
======================================

.. uml::
 :caption: UC_PERM_01 — secuencia desde
           catalogo

 @startuml

 actor Invoker as Invoker
 participant "UI Catalogo PERM" as UiCatalogoPerm
 participant "API ACG" as ApiAcg
 participant "Backend\n(UC_ACC_04)" as Backend
 database "Repo" as Repo

 Invoker -> UiCatalogoPerm: Abre catalogo de AGRs
 UiCatalogoPerm -> ApiAcg: GET /api/access-groups/
 ApiAcg --> UiCatalogoPerm: lista AGRs + counts

 Invoker -> UiCatalogoPerm: Selecciona AGR + User
 UiCatalogoPerm -> ApiAcg: GET preview-assign?
 ApiAcg -> Repo: dry-run validations
 ApiAcg --> UiCatalogoPerm: preview con composicion + impact

 UiCatalogoPerm -> UiCatalogoPerm: Modal con composicion
 Invoker -> UiCatalogoPerm: Confirma

 UiCatalogoPerm -> ApiAcg: POST /api/users/{id}/access-groups/
 ApiAcg -> Backend: delega flujo UC_ACC_04
 Backend -> Repo: registrar Assignment + audit + cache
 Backend --> ApiAcg: 201 Created
 ApiAcg --> UiCatalogoPerm: result
 UiCatalogoPerm -> UiCatalogoPerm: refresh catalogo (counts +1)
 UiCatalogoPerm --> Invoker: Toast confirmacion

 @enduml

