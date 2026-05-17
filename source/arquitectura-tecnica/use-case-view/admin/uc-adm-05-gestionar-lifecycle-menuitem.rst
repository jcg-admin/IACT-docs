.. meta::
 :artefacto: AT_UC_ADM_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_adm_05_gestionar_lifecycle_menuitem:

==============================================
UC_ADM_05 — Gestionar Lifecycle de MenuItem
==============================================

UC v5.6.x extension. Implementa la state machine de
transiciones del ``MenuItem`` (5 transiciones validas) +
gestion del flag ``block_auto_archive``. El Planificador de
Tareas ejecuta auto-archive a 90d con identidad ``actor=system``.
Capability ``manage_menu_lifecycle`` con ``is_critical=True``.

.. uml::
 :caption: UC_ADM_05 — actores, transiciones, job de auto-archive.

 @startuml

 left to right direction

 actor "manage_menu_lifecycle" as manage_menu_lifecycle
 actor "Planificador\nde Tareas" as PlanificadorTareas <<sistema>>
 actor "view_menu_lifecycle" as view_menu_lifecycle <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "MenuItemRepo" as MenuItemRepo <<sistema>>
 actor "MenuLifecycleService" as MenuLifecycleService <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_05\nGestionar Lifecycle\nde MenuItem" as UC_ADM_05
   usecase "Verificar AGR-010\n(bypass cache AP-2b)" as VERIFICAR_AGR
   usecase "Validar transicion\nvalida (state machine)" as VALIDAR_TRANS
   usecase "Validar Function\nactiva (en publish)" as VALIDAR_FN
   usecase "Aplicar transicion\n(deprecated_at /\narchived_at)" as APLICAR
   usecase "Invalidar cache\nmenu:user:{id}" as INVALIDAR
   usecase "Emitir AuditEvent\nLIFECYCLE_TRANSITION" as AUDITAR
   usecase "Set/Clear flag\nblock_auto_archive" as BLOCK_FLAG
   usecase "auto_archive_menu_items()\n(diario a 02:00 UTC)" as AUTO_ARCHIVE
   usecase "Notificar warning\n(30d / 80d)" as NOTIF_WARN
   usecase "Notificar critical\n(>=90d con block)" as NOTIF_CRIT
 }

 manage_menu_lifecycle --> UC_ADM_05
 view_menu_lifecycle --> UC_ADM_05
 PlanificadorTareas --> AUTO_ARCHIVE : actor=system

 UC_ADM_05 ..> VERIFICAR_AGR : <<include>>
 UC_ADM_05 ..> VALIDAR_TRANS : <<include>>
 UC_ADM_05 ..> VALIDAR_FN : <<extend>>\n(solo en publish)
 UC_ADM_05 ..> APLICAR : <<include>>
 UC_ADM_05 ..> INVALIDAR : <<include>>
 UC_ADM_05 ..> AUDITAR : <<include>>
 UC_ADM_05 ..> BLOCK_FLAG : <<extend>>

 AUTO_ARCHIVE ..> APLICAR : <<include>>
 AUTO_ARCHIVE ..> AUDITAR : <<include>>
 AUTO_ARCHIVE ..> INVALIDAR : <<include>>
 AUTO_ARCHIVE ..> NOTIF_WARN : <<extend>>
 AUTO_ARCHIVE ..> NOTIF_CRIT : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_TRANS --> MenuLifecycleService
 APLICAR --> MenuItemRepo
 APLICAR --> MenuLifecycleService
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 BLOCK_FLAG --> MenuLifecycleService
 NOTIF_WARN --> InternalMailbox
 NOTIF_CRIT --> InternalMailbox
 AuditService --> view_audit_log

 note bottom of VALIDAR_TRANS
   5 transiciones validas:
     DRAFT -> ACTIVE
     ACTIVE -> DEPRECATED
     DEPRECATED -> ACTIVE
     DEPRECATED -> ARCHIVED
     ARCHIVED -> ACTIVE
   Otra cualquier combinacion
   responde 409.
 end note

 note bottom of BLOCK_FLAG
   block_auto_archive=True
   requiere block_reason >= 20
   chars + block_set_by +
   block_set_at + audit log.
   Solo aplica en DEPRECATED.
 end note

 note bottom of AUTO_ARCHIVE
   Idempotente. Re-ejecucion
   no duplica archives ni
   notificaciones.
   Day 30: warning early.
   Day 80: pre-archive notif.
   Day 90: archive si !block;
           critical alert si block.
 end note

 @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/admin/uc-adm-05/index` — spec
   completa (12 partes).
 - :doc:`/arquitectura-tecnica/domain-model/menu-item` — entidad
   afectada.
 - :doc:`/arquitectura-tecnica/domain-model/menu-lifecycle-service`
   — state machine.
 - :doc:`/arquitectura-tecnica/domain-model/menu-item-repo` —
   queryset.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   destinatario de warnings y critical alerts.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de LIFECYCLE_TRANSITION.
 - :doc:`/arquitectura-tecnica/scheduled-tasks` — motor concreto
   del Planificador de Tareas.
 - :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
   (estados DRAFT/ACTIVE/DEPRECATED/ARCHIVED).
