.. meta::
 :artefacto: AT_DM_CLASS_MENU_ITEM
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_menu_item:

========
MenuItem
========

**v5.6.x extension.** Wrapper UX persistido 1:1 sobre
``Function``. Materializa el catalogo de items del menu con
metadata visual (label, icono, ruta, orden) y lifecycle propio
(DRAFT/ACTIVE/DEPRECATED/ARCHIVED). NO es fuente de capability:
la regla de acceso vive siempre en ``Function``.

Documentado en
:doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
Constraint: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
(v2.0.0).

.. uml::
 :caption: Clase MenuItem v1.0.0 — wrapper UX 1:1 sobre Function
           con lifecycle DRAFT/ACTIVE/DEPRECATED/ARCHIVED.

 @startuml

 class MenuItem {
   + id : UUID
   + function : Function          <<OneToOne, PROTECT>>
   + display_label : String
   + icon : String
   + display_order : Integer
   + route_path : String
   + parent : MenuItem             <<self FK, nullable>>
   + status : MenuItemStatus
   + deprecated_at : DateTime      <<nullable>>
   + archived_at : DateTime        <<nullable>>
   + block_auto_archive : Boolean  <<default False>>
   + block_reason : String         <<>= 20 chars si block=True>>
   + block_set_by : User           <<nullable>>
   + block_set_at : DateTime       <<nullable>>
   + created_at : DateTime
   + updated_at : DateTime
   + created_by : User
   --
   + transition_to(status: MenuItemStatus, actor: User)
   + set_block_flag(reason: String, actor: User)
   + clear_block_flag(actor: User)
   + is_visible_to(user: User) : Boolean
   + days_in_deprecated() : Integer
   + clean()                       <<validate I-1..I-4>>
 }

 enum MenuItemStatus {
   DRAFT
   ACTIVE
   DEPRECATED
   ARCHIVED
 }

 class Function

 MenuItem "1" -- "1" Function : function\n(OneToOne, PROTECT)
 MenuItem "0..*" -- "0..1" MenuItem : parent\n(self, SET_NULL)
 MenuItem "*" -- "1" MenuItemStatus : status

 note right of MenuItem
   campo function:
   I-1: OneToOneField, on_delete=PROTECT.
   Borrar Function bloqueado si tiene
   MenuItem (auditable).
   --
   campo parent:
   Override visual UX, NO jerarquia
   de permisos (CNST-029 modelo plano).
   Frontend reconstruye arbol opcional.
 end note

 note bottom of MenuItem
   Invariantes (CNST-032 v2.0.0):
   - I-1: 1 Function = 0..1 MenuItem
   - I-2: PROTECT on Function delete
   - I-3: Function puede existir sin MenuItem
   - I-4: Function.is_active=False oculta
          (filter en queryset, no signal)
 end note

 @enduml

**Indices DB (3):**

- ``status``
- ``(status, display_order)``
- ``deprecated_at``

**Reglas de transicion** (state machine — UC_ADM_05):

::

   DRAFT      -> ACTIVE      (publicar)
   ACTIVE     -> DEPRECATED  (deprecar)
   DEPRECATED -> ACTIVE      (reactivar — limpia campos)
   DEPRECATED -> ARCHIVED    (archivar manual o auto 90d)
   ARCHIVED   -> ACTIVE      (reactivar — limpia archived_at)

Cualquier otra combinacion responde 409 Conflict.

**Politica de campos derivados:**

.. list-table::
 :widths: 25 25 25 25
 :header-rows: 1

 * - Transicion
   - deprecated_at
   - archived_at
   - block_*
 * - DRAFT → ACTIVE
   - NULL
   - NULL
   - reset
 * - ACTIVE → DEPRECATED
   - now()
   - sin cambio
   - sin cambio
 * - DEPRECATED → ACTIVE
   - NULL (limpia)
   - sin cambio
   - reset
 * - DEPRECATED → ARCHIVED
   - sin cambio
   - now()
   - reset
 * - ARCHIVED → ACTIVE
   - NULL
   - NULL
   - reset

.. seealso::

 :doc:`function`
 :doc:`menu-item-repo`
 :doc:`menu-lifecycle-service`
 :doc:`user-capability-resolver`
 :doc:`audit-event`
 :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
 :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
 :doc:`/requisitos/casos-uso/admin/uc-adm-04/index`
 :doc:`/requisitos/casos-uso/admin/uc-adm-05/index`
