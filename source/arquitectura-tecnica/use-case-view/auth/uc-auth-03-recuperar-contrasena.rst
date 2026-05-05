.. meta::
 :artefacto: AT_UC_AUTH_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_auth_03_recuperar_contrasena:

==============================
UC_AUTH_03 — Recuperar Contrasena
==============================

User olvida password. Admin con ``reset_password`` genera password
temporal via ``PasswordGenerator`` (TTL corto), lo entrega al destino
via ``InternalMessage``, blackliste tokens activos del User. User
debe cambiar la temporal en su primer uso (UC_AUTH_04).

.. uml::
 :caption: UC_AUTH_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "reset_password" as reset_password
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "PasswordGenerator" as PasswordGenerator <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_03\nRecuperar Contrasena" as UC_AUTH_03
   usecase "Verificar\nreset_password" as VERIFICAR_AGR
   usecase "Generar password\ntemporal (TTL corto)" as GENERAR_TEMP
   usecase "Persistir hash\n+ flag must_change" as PERSISTIR
   usecase "Blacklist tokens\nactivos del User\n(reason=PASSWORD_CHANGED)" as BLACKLIST
   usecase "Enviar via\nInternalMessage" as ENVIAR
   usecase "Sanitizar logs\n(no plain pwd)" as SANITIZAR
   usecase "Emitir AuditEvent\nPASSWORD_RESET" as AUDITAR
 }

 reset_password --> UC_AUTH_03

 UC_AUTH_03 ..> VERIFICAR_AGR : <<include>>
 UC_AUTH_03 ..> GENERAR_TEMP : <<include>>
 UC_AUTH_03 ..> PERSISTIR : <<include>>
 UC_AUTH_03 ..> BLACKLIST : <<include>>
 UC_AUTH_03 ..> ENVIAR : <<include>>
 UC_AUTH_03 ..> SANITIZAR : <<include>>
 UC_AUTH_03 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 GENERAR_TEMP --> PasswordGenerator
 PERSISTIR --> UserRepo
 BLACKLIST --> BlacklistedToken
 ENVIAR --> InternalMailbox
 InternalMailbox --> User_destino
 SANITIZAR --> Sanitizer
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of GENERAR_TEMP
   PasswordGenerator.generate_temporary
   con TTL corto (e.g. 24h). Plain
   text via mailbox UNA sola vez.
 end note

 note bottom of BLACKLIST
   Reset invalida sesiones activas
   por seguridad (tokens del User
   blacklisted con reason=
   PASSWORD_CHANGED).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   password_hash actualizado.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/password-generator` —
   genera temporal con TTL.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   revoca sesiones activas.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon del destino.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item con password temporal.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   evita plain en logs.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica reset_password.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor PASSWORD_RESET.
 - :doc:`/requisitos/casos-uso/auth/uc-auth-03/index` —
   spec textual.
