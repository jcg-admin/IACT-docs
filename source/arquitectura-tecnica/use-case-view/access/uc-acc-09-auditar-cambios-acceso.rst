.. meta::
 :artefacto: AT_UC_ACC_09_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_acc_09_auditar_cambios_acceso:

==================================================
UC_ACC_09 — Auditar Cambios de Acceso (vista MOD_Access)
==================================================

Vista de AuditEvent con scope **MOD_Access** (subset de UC_AUD_01).
Muestra cambios de Assignments, ExceptionalPermissions, AGR vencidos.
``view_audit_log`` filtrado a event_types ACC_*. P-44 meta-audit.

.. uml::
 :caption: UC_ACC_09 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_audit_log" as view_audit_log_invoker
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as UC_ACC_09
   usecase "Verificar\nview_audit_log" as VERIFICAR_AGR
   usecase "Forzar scope=MOD_Access\n(filter event_type)" as FORZAR_SCOPE
   usecase "Filtrar por actor_id\n+ event_type + period" as FILTROS
   usecase "Cursor pagination" as PAGINACION
   usecase "Construir timeline" as TIMELINE
   usecase "Meta-audit\nACC_AUDIT_QUERIED (P-44)" as METAAUDIT
 }

 view_audit_log_invoker --> UC_ACC_09

 UC_ACC_09 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_09 ..> FORZAR_SCOPE : <<include>>
 UC_ACC_09 ..> FILTROS : <<include>>
 UC_ACC_09 ..> PAGINACION : <<include>>
 UC_ACC_09 ..> TIMELINE : <<include>>
 UC_ACC_09 ..> METAAUDIT : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTROS --> AuditQueryService
 AuditQueryService --> AuditRepo
 PAGINACION --> CursorEncoder
 METAAUDIT --> AuditService
 AuditService --> view_audit_log

 note bottom of FORZAR_SCOPE
   Scope MOD_Access: filter event_type ∈
   {FUNCTIONS_*, AGR_*, EXCEPTIONAL_*}.
   UC_AUD_01 cubre TODO scope.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   eventos consultados.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo append-only.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   ejecuta filtros.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor del meta-audit.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_audit_log.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` —
   UC con scope ALL.
 - :doc:`/requisitos/casos-uso/access/uc-acc-09/index` —
   spec textual.
