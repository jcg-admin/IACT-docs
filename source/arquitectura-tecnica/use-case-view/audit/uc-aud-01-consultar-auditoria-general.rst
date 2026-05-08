.. meta::
 :artefacto: AT_UC_AUD_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_aud_01_consultar_auditoria_general:

==================================================
UC_AUD_01 — Consultar Auditoria General
==================================================

List paginado timeline-style de TODOS los AuditEvents (todos los
modulos), con filtros (period, module, event_type, actor_id, target).
P-44 meta-audit ``GENERAL_AUDIT_QUERIED``. Diferente de UC_PERM_10
(scope=RBAC subset) — UC_AUD_01 cubre operacionales tambien.

.. uml::
 :caption: UC_AUD_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_audit_log" as view_audit_log_invoker
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nConsultar Auditoria\nGeneral" as UC_AUD_01
   usecase "Verificar\nview_audit_log" as VERIFICAR_AGR
   usecase "Validar period\n(default last_7d)" as VALIDAR_PERIOD
   usecase "Aplicar filtros\n(module, event_type,\nactor_id, target)" as FILTROS
   usecase "Cursor pagination" as PAGINACION
   usecase "Construir timeline\n+ summary" as TIMELINE
   usecase "Meta-audit\nGENERAL_AUDIT_QUERIED\n(P-44)" as METAAUDIT
 }

 view_audit_log_invoker --> UC_AUD_01

 UC_AUD_01 ..> VERIFICAR_AGR : <<include>>
 UC_AUD_01 ..> VALIDAR_PERIOD : <<include>>
 UC_AUD_01 ..> FILTROS : <<include>>
 UC_AUD_01 ..> PAGINACION : <<include>>
 UC_AUD_01 ..> TIMELINE : <<include>>
 UC_AUD_01 ..> METAAUDIT : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 FILTROS --> AuditQueryService
 AuditQueryService --> AuditRepo
 PAGINACION --> CursorEncoder
 METAAUDIT --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_AUD_01
   Scope: TODOS los modulos.
   UC_PERM_10 cubre subset RBAC,
   UC_ACC_09 subset Access.
   Funciones RBAC granular P-15.
 end note

 note bottom of METAAUDIT
   P-44 audit del audit:
   toda consulta a la bitacora
   genera AuditEvent.
   CNST-008/009/013/025/026.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura inmutable.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo append-only con read-replica.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   ejecuta filtros + pagination.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor del meta-audit.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination cursor.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_audit_log.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` —
   spec textual.
