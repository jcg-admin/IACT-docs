.. meta::
 :artefacto: AT_DM_CLASS_MENU_ITEM_REPO
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

.. _dm_class_menu_item_repo:

============
MenuItemRepo
============

**v5.6.x extension.** Repositorio + queryset para ``MenuItem``.
Encapsula las consultas canonicas: items visibles para un user,
preview admin, listados filtrados y operaciones bulk. Garantiza
el invariante I-4 (visibilidad cascade desde
``Function.is_active``) via ``filter`` en queryset, no via signal.

.. uml::
 :caption: Clase MenuItemRepo v1.0.0 — repositorio + queryset
           con metodos de visibilidad para UC_PERM_08 y admin.

 @startuml

 class MenuItemRepo {
   - queryset
   --
   + visible()
   + for_user(user)
   + with_status_for_admin(statuses)
   + by_function(function)
   + descendants(parent)
   + ancestors(item)
   + has_cycle(item, candidate_parent)
   + bulk_reorder(items, orders)
   + count_by_status()
 }

 class MenuItemQuerySet {
   + visible() : QuerySet
   + for_user(user) : QuerySet
   + with_status_for_admin(statuses) : QuerySet
   + due_for_auto_archive(threshold_days) : QuerySet
   + due_for_pre_archive_warning(start, end) : QuerySet
   + select_with_function() : QuerySet
 }

 class MenuItem
 class Function
 class User

 MenuItemRepo "1" -- "1" MenuItemQuerySet : queryset
 MenuItemRepo --> MenuItem : queries
 MenuItemRepo ..> Function : reads is_active
 MenuItemRepo ..> User : reads capabilities

 note bottom of MenuItemRepo
   for_user(user) filtra:
     status='ACTIVE'
     AND function.is_active=True
     AND function.codename
         IN UserCapabilityResolver
            .resolve(user)
   Garantiza I-4 (visibilidad cascade).
 end note

 note bottom of MenuItemQuerySet
   due_for_auto_archive(N) returns:
     SELECT * WHERE
       status='DEPRECATED'
       AND deprecated_at < now() - N days
       AND block_auto_archive=False
   Soporte del job
   auto_archive_menu_items
   (UC_ADM_05 FA-04).
 end note

 @enduml

**Metodos canonicos** (consumo desde otros componentes):

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Metodo
   - Consumidor principal
   - Garantia
 * - ``visible()``
   - cualquier endpoint que lista items
   - Solo ACTIVE + Function activa (I-4)
 * - ``for_user(user)``
   - ``UserMenuEndpoint`` (UC_PERM_08 ext)
   - visible() + filtro por
     ``UserCapabilityResolver.resolve(user)``
 * - ``with_status_for_admin(statuses)``
   - admin UI (UC_ADM_04 listado)
   - Acceso a DRAFT y DEPRECATED para preview
 * - ``due_for_auto_archive(90)``
   - job ``auto_archive_menu_items``
   - DEPRECATED >90d sin block
 * - ``due_for_pre_archive_warning(80, 90)``
   - job de notificacion 80d
   - Ventana 80-90d sin block
 * - ``has_cycle(item, candidate)``
   - UC_ADM_04 FA-03 (reorganizar parent)
   - DAG validation antes de UPDATE
 * - ``bulk_reorder(items, orders)``
   - UC_ADM_04 FA-05 bulk reorder
   - 1 UPDATE multi-row + 1 audit event
 * - ``count_by_status()``
   - dashboards / metrics
   - Counts por estado para observabilidad

**Patron implementado:** Repository + Custom QuerySet Manager.
``MenuItemRepo`` delega a ``MenuItemQuerySet`` que extiende
``Q.objects``. Encapsulamiento del ORM detras de la interfaz
de dominio.

.. seealso::

 :doc:`menu-item`
 :doc:`function`
 :doc:`user-capability-resolver`
 :doc:`menu-lifecycle-service`
 :doc:`/backend/rbac-implementation-guide`
 :doc:`/requisitos/casos-uso/admin/uc-adm-04/index`
