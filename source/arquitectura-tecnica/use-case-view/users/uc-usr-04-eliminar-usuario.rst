.. meta::
 :artefacto: AT_UC_USR_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_usr_04_eliminar_usuario:

==============================
UC_USR_04 — Eliminar Usuario
==============================

Desactiva un User (BR-009 baja logica — NO DELETE). ``state`` transita
a ``INACTIVE`` o ``BLOCKED``. Revoca todas las sesiones activas via
``BlacklistedToken``, revoca todos los Assignment del User y limpia
PermissionCache. Audit reforzado.

.. uml::
 :caption: UC_USR_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "deactivate_users" as deactivate_users
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as UC_USR_04
   usecase "Verificar\ndeactivate_users" as VERIFICAR_AGR
   usecase "Validar reason ≥ 20" as VALIDAR_REASON
   usecase "Transicionar\nstate=INACTIVE" as PERSISTIR
   usecase "Revocar Assignments\n(state=REVOKED)" as REVOCAR_ASSIGN
   usecase "Blacklist tokens\nactivos" as BLACKLIST
   usecase "Invalidar PermissionCache" as INVALIDAR
   usecase "Emitir AuditEvent\nUSER_DEACTIVATED" as AUDITAR
 }

 deactivate_users --> UC_USR_04

 UC_USR_04 ..> VERIFICAR_AGR : <<include>>
 UC_USR_04 ..> VALIDAR_REASON : <<include>>
 UC_USR_04 ..> PERSISTIR : <<include>>
 UC_USR_04 ..> REVOCAR_ASSIGN : <<include>>
 UC_USR_04 ..> BLACKLIST : <<include>>
 UC_USR_04 ..> INVALIDAR : <<include>>
 UC_USR_04 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 PERSISTIR --> UserRepo
 REVOCAR_ASSIGN --> AssignmentRepo
 BLACKLIST --> BlacklistedToken
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 PERSISTIR --> User_destino
 AuditService --> view_audit_log

 note bottom of UC_USR_04
   BR-009 baja logica — no DELETE.
   Historial preservado para
   auditoria (CNST-025 inmutable).
 end note

 note bottom of REVOCAR_ASSIGN
   Cascade revoke de Assignments
   activos. Si hay critico unique
   holder (LastHolderSpec), error 409.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   state INACTIVE.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   cascade revoke.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   tokens revocados.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   LastHolderSpec evita orfandad de funciones criticas.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica deactivate_users.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor USER_DEACTIVATED.
 - :doc:`/requisitos/casos-uso/users/uc-usr-04/index` —
   spec textual.
