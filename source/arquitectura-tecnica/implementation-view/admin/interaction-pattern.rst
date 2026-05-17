.. meta::
 :artefacto: AT_IMPL_SEQ_ADMIN
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_admin:

============================================================
Implementation View — MOD_Admin: Patron de Interaccion
============================================================

Secuencia canonica del modulo: transicion de un ``MenuItem``
en su FSM (``DRAFT → ACTIVE``, etc., UC_ADM_05). El service
implementa un guard de transicion + side-effects sobre
campos derivados.

.. uml::
 :caption: MOD_Admin impl seq — MenuItem state transition.

 @startuml

 actor PipelineAdmin
 participant "MenuItemView\n(APIView)" as View <<api>>
 participant "MenuItemSerializer" as Serializer <<serializer>>
 participant "MenuLifecycleService" as Svc <<service>>
 participant "MenuItemRepository" as Repo <<repository>>
 participant "AuditService" as Audit <<service>>
 database PostgreSQL

 PipelineAdmin -> View : POST /api/v1/admin/menu-items/{id}/transition/\n{action: "publish"}
 activate View

 View -> View : permission_classes\n[function_perm("manage_menu_items")]

 View -> Serializer : .is_valid(...)
 Serializer --> View : action

 View -> Svc : transition(item_id, action, actor)
 activate Svc

 Svc -> Repo : by_id(item_id)
 activate Repo
 Repo -> PostgreSQL : SELECT * FROM menu_item WHERE id = ?
 Repo --> Svc : MenuItem
 deactivate Repo

 Svc -> Svc : guard:\nis_valid_transition(\nitem.status, action)
 alt invalid transition
   Svc --> View : raise InvalidTransition
   View --> PipelineAdmin : HTTP 409 Conflict + error_code=\nINVALID_STATE_TRANSITION
 else valid
   Svc -> Svc : derive next_status,\ncampos derivados\n(deprecated_at, archived_at,\nblock_*)

   Svc -> Repo : update(item_id, **derived)
   activate Repo
   Repo -> PostgreSQL : UPDATE menu_item SET ... WHERE id = ?
   Repo --> Svc : MenuItem
   deactivate Repo

   Svc -> Audit : record(MENU_ITEM_TRANSITION,\nactor, item_id, transition)

   Svc --> View : MenuItem
 end
 deactivate Svc

 View -> Serializer : .to_representation(...)
 View --> PipelineAdmin : HTTP 200 + body
 deactivate View

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/admin_panel/api/views.py: MenuItemView,
     FunctionCatalogView, AgrupadorView``
 * - Service
   - ``apps/admin_panel/services/menu_lifecycle_service.py``
     (logica de transicion + derivacion de campos)
 * - Repository
   - ``apps/admin_panel/repositories/menu_item_repo.py``
 * - Transition table
   - ``apps/admin_panel/services/_transitions.py:
     VALID_TRANSITIONS`` (dict de
     ``(from_state, action) -> (to_state, derive_fields)``)

Invariantes de implementacion
==============================

- **I-IMPL-ADM-01:** la tabla de transiciones es**dato**,
  no codigo: ``VALID_TRANSITIONS = {("DRAFT", "publish"):
  ("ACTIVE", _on_publish), ...}``. Permite agregar
  transiciones nuevas sin reescribir el service.
- **I-IMPL-ADM-02:** el guard ``is_valid_transition`` se
  ejecuta ANTES del UPDATE — sin transition valida no hay
  query a BD. Cualquier combinacion no en
  ``VALID_TRANSITIONS`` responde 409.
- **I-IMPL-ADM-03:** los campos derivados (``deprecated_at``,
  ``archived_at``, ``block_*``) se computan en helpers
  ``_on_publish``, ``_on_deprecate``, etc. — separados del
  service principal. Test unitario por helper.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/admin/menu-item-lifecycle` —
   FSM del MenuItem (DesignView).
 - :doc:`/arquitectura-tecnica/domain-model/menu-lifecycle-service` —
   service en domain-model.
