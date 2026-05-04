.. _uc-perm-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

.. note::

 Diagramas backend identicos a UC_ACC_04
 Parte 8. Esta parte muestra el flujo desde
 la vista UI PERM y la coexistencia ACC↔PERM.

8.1 Diagrama de coexistencia ACC↔PERM
=====================================

.. uml::
 :caption: UC_PERM_01 vs UC_ACC_04 — vistas
           del mismo flujo

 @startuml
 left to right direction

 actor "assign_function_groups" as assign_function_groups
 actor "assign_function_groups" as assign_function_groups

 rectangle "UI MOD_Access" {
   usecase "UC_ACC_04\nAsignar AGR\n(desde User)" as ACC04
 }

 rectangle "UI MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo\n(desde catalogo AGR)" as PERM01
 }

 cloud "Backend compartido" {
   usecase "POST /api/users/\n{id}/access-groups/" as BE
   note bottom: Funcion: assign_function_groups
 }

 assign_function_groups --> ACC04
 assign_function_groups --> PERM01
 ACC04 --> BE : delega
 PERM01 --> BE : delega

 note right of BE
   Implementacion comun (UC_ACC_04 backing).
   AuditEvent AGR_ASSIGNED no distingue
   origen UI.
 end note

 @enduml

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
 Backend -> Repo: INSERT Assignment + audit + cache
 Backend --> ApiAcg: 201 Created
 ApiAcg --> UiCatalogoPerm: result
 UiCatalogoPerm -> UiCatalogoPerm: refresh catalogo (counts +1)
 UiCatalogoPerm --> Invoker: Toast confirmacion

 @enduml

8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_01 — actividad

 @startuml

 start

 :Invoker abre catalogo de AGRs;
 :Selecciona AGR;
 :Selecciona User destino;

 :GET preview-assign;
 :Modal con composicion + impact;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 :POST /api/users/{id}/access-groups/;

 note right
   Flujo backend identico
   a UC_ACC_04
 end note

 if (Backend OK?) then (no)
   :Mostrar error segun status; stop
 else (si)
 endif

 :Refrescar catalogo
  (counts AGR +1);
 :Toast confirmacion;

 stop

 @enduml

8.4 Diagrama de clases — vistas compartidas
===========================================

.. uml::
 :caption: ACC y PERM vistas — backing comun

 @startuml

 class "View_ACC" as ViewAcc
 class "View_PERM" as ViewPerm
 class "AccessService" as Accessservice {
   +assign_access_group(...)
 }
 class Assignment
 class AccessGroup
 class AuditEvent

 ViewAcc --> Accessservice : invoca
 ViewPerm --> Accessservice : invoca
 Accessservice --> Assignment : crea
 Accessservice --> AuditEvent : emite
 Assignment --> AccessGroup : referencia

 note right of Accessservice
   UC_ACC_04 backing
   compartido por ambas vistas
 end note

 @enduml
