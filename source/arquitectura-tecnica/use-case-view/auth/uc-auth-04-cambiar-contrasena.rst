.. meta::
 :artefacto: AT_UC_AUTH_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_auth_04_cambiar_contrasena:

============================================================
UC_AUTH_04 — Cambiar Contrasena
============================================================

User cambia su propio password. Requiere proporcionar password actual
para verificacion + nuevo password (PasswordPolicy aplicada). Sesion
propia — sin RBAC adicional. Blacklisted tokens activos para forzar
re-login con nuevo password.

.. uml::
 :caption: UC_AUTH_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "User autenticado" as User_autenticado
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "PasswordGenerator" as PasswordGenerator <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_04\nCambiar Contrasena" as UC_AUTH_04
   usecase "Validar password\nactual" as VALIDAR_ACTUAL
   usecase "Validar nuevo cumple\nPasswordPolicy" as VALIDAR_NUEVO
   usecase "Verificar nuevo ≠ actual\n+ ≠ ultimas N" as VALIDAR_HISTORIA
   usecase "Persistir nuevo hash\n+ clear must_change" as PERSISTIR
   usecase "Blacklist tokens\nactivos (forzar re-login)" as BLACKLIST
   usecase "Sanitizar logs" as SANITIZAR
   usecase "Emitir AuditEvent\nPASSWORD_CHANGED" as AUDITAR
 }

 User_autenticado --> UC_AUTH_04

 UC_AUTH_04 ..> VALIDAR_ACTUAL : <<include>>
 UC_AUTH_04 ..> VALIDAR_NUEVO : <<include>>
 UC_AUTH_04 ..> VALIDAR_HISTORIA : <<include>>
 UC_AUTH_04 ..> PERSISTIR : <<include>>
 UC_AUTH_04 ..> BLACKLIST : <<include>>
 UC_AUTH_04 ..> SANITIZAR : <<include>>
 UC_AUTH_04 ..> AUDITAR : <<include>>

 VALIDAR_ACTUAL --> UserRepo
 VALIDAR_NUEVO --> PasswordGenerator
 PERSISTIR --> UserRepo
 BLACKLIST --> BlacklistedToken
 SANITIZAR --> Sanitizer
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_NUEVO
   PasswordGenerator.meets_policy
   verifica complejidad. Politica
   default: 12 chars + upper + lower
   + digit + symbol.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   password_hash actualizado.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/password-generator` —
   meets_policy + PasswordPolicy.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   revoca tokens activos.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   evita plain en logs.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor PASSWORD_CHANGED.
 - :doc:`/requisitos/casos-uso/auth/uc-auth-04/index` —
   spec textual.
