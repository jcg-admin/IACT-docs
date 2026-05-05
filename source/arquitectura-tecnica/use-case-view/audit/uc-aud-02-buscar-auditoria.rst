.. meta::
 :artefacto: AT_UC_AUD_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_aud_02_buscar_auditoria:

==============================
UC_AUD_02 — Buscar Auditoria
==============================

FTS bounded sobre payload indexado (Elasticsearch / Postgres FTS).
``search_audit_log`` distinta de ``view_audit_log`` (P-15).
``date_range`` obligatorio (max 90 dias) para evitar full table scans.

.. uml::
 :caption: UC_AUD_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "search_audit_log" as search_audit_log
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditValidator" as AuditValidator <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar Auditoria\n(FTS bounded)" as UC_AUD_02
   usecase "Verificar\nsearch_audit_log" as VERIFICAR_AGR
   usecase "Validar query\nno vacia" as VALIDAR_QUERY
   usecase "Validar date_range\nobligatorio (max 90d)" as VALIDAR_RANGE
   usecase "Aplicar filtros\nestructurados" as FILTROS
   usecase "Ejecutar FTS bounded" as FTS_QUERY
   usecase "Cursor pagination" as PAGINACION
   usecase "Meta-audit\nAUDIT_SEARCHED" as METAAUDIT
 }

 search_audit_log --> UC_AUD_02

 UC_AUD_02 ..> VERIFICAR_AGR : <<include>>
 UC_AUD_02 ..> VALIDAR_QUERY : <<include>>
 UC_AUD_02 ..> VALIDAR_RANGE : <<include>>
 UC_AUD_02 ..> FILTROS : <<include>>
 UC_AUD_02 ..> FTS_QUERY : <<include>>
 UC_AUD_02 ..> PAGINACION : <<include>>
 UC_AUD_02 ..> METAAUDIT : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_QUERY --> AuditValidator
 VALIDAR_RANGE --> AuditValidator
 FTS_QUERY --> AuditQueryService
 AuditQueryService --> AuditRepo
 PAGINACION --> CursorEncoder
 METAAUDIT --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_RANGE
   BoundedDateRangeSpec: range max
   90 dias. Para periodos mayores
   usar export (UC_AUD_03).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura indexada para FTS.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   AuditRepo con FTS bounded.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   orquesta FTS.
 - :doc:`/arquitectura-tecnica/domain-model/audit-validator` —
   validacion query/range.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   BoundedDateRangeSpec.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   meta-audit.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica search_audit_log.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-02/index` —
   spec textual.
