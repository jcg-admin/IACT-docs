.. meta::
 :artefacto: AT_DM_CLASS_MENU_LIFECYCLE_SERVICE
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

.. _dm_class_menu_lifecycle_service:

=====================
MenuLifecycleService
=====================

**v5.6.x extension.** State machine + politicas del lifecycle de
``MenuItem``. Centraliza:

- Transiciones validas (DRAFT → ACTIVE → DEPRECATED → ARCHIVED).
- Activacion/desactivacion del flag ``block_auto_archive`` con
  validacion de ``block_reason``.
- Logica del job ``auto_archive_menu_items`` ejecutado por el
  Planificador de Tareas (UC_ADM_05 FA-04).
- Gestion de campos derivados (``deprecated_at``,
  ``archived_at``, cuarteto ``block_*``).

.. uml::
 :caption: Clase MenuLifecycleService v1.0.0 — state machine
           + politica de auto-archive a 90d con block opt-out.

 @startuml

 class MenuLifecycleService {
   + VALID_TRANSITIONS
   + DEPRECATED_WARNING_DAYS = 30
   + DEPRECATED_PRE_ARCHIVE_DAYS = 80
   + DEPRECATED_ARCHIVE_DAYS = 90
   + BLOCK_REASON_MIN_LENGTH = 20
   --
   + transition(item, target, actor)
   + set_block_flag(item, reason, actor)
   + clear_block_flag(item, actor)
   + auto_archive_due_items() : ArchiveJobResult
   - _validate_transition(current, target)
   - _apply_derived_fields(item, target)
   - _emit_audit(item, before, after)
 }

 class ArchiveJobResult {
   + archived_count : Integer
   + warned_count : Integer
   + critical_alert_count : Integer
   + failures : list of MenuItem
 }

 class InvalidTransitionError {
   + current : MenuItemStatus
   + requested : MenuItemStatus
 }

 class FunctionInactiveError {
   + function_codename : String
 }

 class BlockOnlyInDeprecatedError

 class MenuItem
 class MenuItemRepo
 class AuditService
 class PermissionCache
 class InternalMailbox

 MenuLifecycleService --> MenuItem : transitions
 MenuLifecycleService --> MenuItemRepo : reads / writes
 MenuLifecycleService --> AuditService : emits LIFECYCLE_*
 MenuLifecycleService --> PermissionCache : invalidates
 MenuLifecycleService --> InternalMailbox : warns / alerts
 MenuLifecycleService ..> InvalidTransitionError : throws
 MenuLifecycleService ..> FunctionInactiveError : throws
 MenuLifecycleService ..> BlockOnlyInDeprecatedError : throws
 MenuLifecycleService --> ArchiveJobResult : returns

 note right of MenuLifecycleService
   VALID_TRANSITIONS:
     DRAFT -> ACTIVE
     ACTIVE -> DEPRECATED
     DEPRECATED -> ACTIVE
     DEPRECATED -> ARCHIVED
     ARCHIVED -> ACTIVE
 end note

 note bottom of MenuLifecycleService
   auto_archive_due_items() es
   idempotente:
   1. Auto-archive items DEPRECATED >90d
      sin block_auto_archive.
   2. Critical alerts items >=90d con block.
   3. Pre-archive notifications 80-90d.
   4. Warning early items >30d.
   Ejecutado por Planificador
   diariamente a 02:00 UTC.
 end note

 @enduml

**Diagrama de estado del MenuItem:**

.. uml::
 :caption: State machine del MenuItem manejado por
           MenuLifecycleService.

 @startuml

 [*] --> DRAFT : crear (UC_ADM_04)

 DRAFT --> ACTIVE : transition(ACTIVE)\npublicar
 DRAFT --> DRAFT : update metadata UX\n(UC_ADM_04, no es transicion)

 ACTIVE --> DEPRECATED : transition(DEPRECATED)\ndeprecar
 ACTIVE --> ACTIVE : update metadata UX

 DEPRECATED --> ACTIVE : transition(ACTIVE)\nreactivar (limpia campos)
 DEPRECATED --> ARCHIVED : transition(ARCHIVED)\narchivar manual
 DEPRECATED --> ARCHIVED : auto_archive_due_items()\n(>=90d, !block)

 ARCHIVED --> ACTIVE : transition(ACTIVE)\nreactivar (limpia archived_at)
 ARCHIVED --> [*] : (sin terminal real)

 note right of DEPRECATED
   deprecated_at = now() en entrada.
   block_auto_archive previene
   auto-archive a 90d.
 end note

 note right of ARCHIVED
   archived_at = now() en entrada.
   Invisible en endpoint.
   Capability sigue accesible
   via URL directa.
 end note

 @enduml

**Politica de campos derivados en cada transicion:**

.. list-table::
 :widths: 30 25 25 20
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

**Politica del flag ``block_auto_archive``** (gap #3 resuelto):

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Aspecto
   - Politica
 * - Default
   - ``False`` — sistema archiva al exceder 90d en DEPRECATED
 * - Activacion
   - Solo en ``status=DEPRECATED``; requiere ``block_reason``
     ≥ 20 caracteres + ``block_set_by`` + ``block_set_at``
 * - Audit
   - Eventos ``MENU_ITEM_BLOCK_FLAG_SET`` /
     ``MENU_ITEM_BLOCK_FLAG_CLEARED``
 * - Reset automatico
   - En cualquier transicion a ACTIVE (campos block_* limpiados)

**Job auto-archive — comportamiento por dia** desde
``deprecated_at``:

::

   Day  0..29: silencioso
   Day 30..79: warning a system_admin (early)
   Day 80..89: pre-archive notification "auto-archive en N dias"
   Day 90+:    si !block: AUTO ARCHIVE
              si  block: critical alert (>= 90d con block activo)

.. seealso::

 :doc:`menu-item`
 :doc:`menu-item-repo`
 :doc:`audit-service`
 :doc:`permission-cache`
 :doc:`internal-mailbox`
 :doc:`/arquitectura-tecnica/scheduled-tasks`
 :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
 :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
 :doc:`/requisitos/casos-uso/admin/uc-adm-05/index`
