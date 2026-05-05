.. meta::
 :artefacto: AT_UC_PERM_10_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_perm_10_consultar_auditoria_de_permisos:

==================================================
UC_PERM_10 — Consultar Auditoria RBAC (scope)
==================================================

Vista timeline de ``AuditEvent`` con scope **RBAC/auth** (subset de
UC_AUD_01 que cubre TODOS los modulos). ``view_audit_log`` distinta
de la funcion homonima de UC_AUD_01 — granularidad P-15.
Meta-audit P-44: toda consulta a la bitacora genera AuditEvent.

.. uml::
 :caption: UC_PERM_10 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_audit_log" as view_audit_log
 actor "view_audit_log" as view_audit_log_meta <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_10\nConsultar Auditoria\nRBAC (scope)" as UC_PERM_10
   usecase "Verificar\nview_audit_log" as VERIFICAR_AGR
   usecase "Validar period\n(default last_7d)" as VALIDAR_PERIOD
   usecase "Forzar scope=RBAC\n(filtros event_type)" as FORZAR_SCOPE
   usecase "Filtrar por actor_id\n+ event_type + target" as FILTROS
   usecase "Cursor-based pagination" as PAGINACION
   usecase "Construir timeline" as TIMELINE
   usecase "Meta-audit\nRBAC_AUDIT_QUERIED\n(P-44)" as METAAUDIT
 }

 view_audit_log --> UC_PERM_10

 UC_PERM_10 ..> VERIFICAR_AGR : <<include>>
 UC_PERM_10 ..> VALIDAR_PERIOD : <<include>>
 UC_PERM_10 ..> FORZAR_SCOPE : <<include>>
 UC_PERM_10 ..> FILTROS : <<include>>
 UC_PERM_10 ..> PAGINACION : <<include>>
 UC_PERM_10 ..> TIMELINE : <<include>>
 UC_PERM_10 ..> METAAUDIT : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTROS --> AuditQueryService
 AuditQueryService --> AuditRepo
 PAGINACION --> CursorEncoder
 METAAUDIT --> AuditService
 AuditService --> view_audit_log_meta

 note bottom of FORZAR_SCOPE
   Scope RBAC: filter event_type ∈
   {AGR_*, FUNCTION_*, EXCEPTIONAL_*,
   SOD_RULE_*, USER_*, AUTH_*}.
   UC_AUD_01 cubre TODO scope.
 end note

 note bottom of METAAUDIT
   P-44 audit del audit. CNST-008/
   009/013/025/026.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   eventos consultados (CNST-025 inmutable).
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo append-only con read-replica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   ejecuta filtros + pagination.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor del meta-audit (P-44).
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   codifica cursor de paginacion.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_audit_log.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` —
   UC con scope ALL modules.
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-10/index` —
   spec textual.
