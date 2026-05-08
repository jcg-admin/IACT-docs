.. meta::
 :artefacto: AT_UC_USR_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_usr_02_consultar_usuarios:

================================
UC_USR_02 — Consultar Usuarios
================================

List paginado de Users con filtros (segmento, state, AGR asignado).
Dos funciones separadas P-15: ``list_users`` (lista basica) y
``view_users`` (detalle por ID con auditoria P-44 reforzada). CNST-008
isolation por segmento — out-of-segment retorna vacio.

.. uml::
 :caption: UC_USR_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "list_users" as list_users
 actor "view_users" as view_users <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_02\nConsultar Usuarios\n.. extension points ..\nVistaDetalle" as UC_USR_02
   usecase "Verificar\nlist_users" as VERIFICAR_AGR
   usecase "Resolver segmento\n(CNST-008)" as RESOLVER_SEG
   usecase "Filtrar por state\n+ AGR + segmento" as FILTROS
   usecase "Cursor pagination" as PAGINACION
   usecase "Sanitizar PII output\n(CNST-026)" as SANITIZAR
   usecase "Vista detalle por ID\n(view_users + audit P-44)" as VISTA_DETALLE
 }

 list_users --> UC_USR_02
 view_users --> VISTA_DETALLE

 UC_USR_02 ..> VERIFICAR_AGR : <<include>>
 UC_USR_02 ..> RESOLVER_SEG : <<include>>
 UC_USR_02 ..> FILTROS : <<include>>
 UC_USR_02 ..> PAGINACION : <<include>>
 UC_USR_02 ..> SANITIZAR : <<include>>
 VISTA_DETALLE ..> UC_USR_02 : <<extend>> (VistaDetalle)

 VERIFICAR_AGR --> AuthorizationGuard
 RESOLVER_SEG --> SegmentResolver
 FILTROS --> UserRepo
 PAGINACION --> CursorEncoder
 SANITIZAR --> Sanitizer
 VISTA_DETALLE --> AuditService
 AuditService --> view_audit_log

 note bottom of VISTA_DETALLE
   GET /api/users/{id}/ requiere
   view_users + emite USER_DETAIL_VIEWED
   (P-44 audit reforzado).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   entity consultada.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio queries.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation por segmento.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder` —
   pagination.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   PII output.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica list_users / view_users.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor en modo detalle.
 - :doc:`/requisitos/casos-uso/users/uc-usr-02/index` —
   spec textual.
