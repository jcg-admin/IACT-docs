.. meta::
 :artefacto: AT_UC_AUTH_01_USECASE
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

.. _at_uc_auth_01_iniciar_sesion:

==============================
UC_AUTH_01 — Iniciar Sesion
==============================

User no autenticado proporciona credenciales (username + password).
Sistema verifica password_hash, registra intento, emite token JWT
firmado y crea ``Session`` activa. UC publico (sin RBAC pre-login).
Throttling por usuario (lockout despues de N intentos fallidos).

.. uml::
 :caption: UC_AUTH_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "User no autenticado" as User_anonimo <<externo>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "Session" as Session <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion\n.. extension points ..\nLockout" as UC_AUTH_01
   usecase "Validar credenciales\n(password_hash)" as VALIDAR_CRED
   usecase "Verificar User state\n(ACTIVE, no BLOCKED)" as VERIFICAR_STATE
   usecase "Verificar refresh\nno blacklisted" as VERIFICAR_BLACKLIST
   usecase "Registrar intento\n(success/fail)" as REGISTRAR_INTENTO
   usecase "Emitir token JWT\nfirmado" as EMITIR_JWT
   usecase "Crear Session activa" as CREAR_SESSION
   usecase "Emitir AuditEvent\nLOGIN_*" as AUDITAR
   usecase "Lockout tras N\nfallidos" as LOCKOUT
 }

 User_anonimo --> UC_AUTH_01

 UC_AUTH_01 ..> VALIDAR_CRED : <<include>>
 UC_AUTH_01 ..> VERIFICAR_STATE : <<include>>
 UC_AUTH_01 ..> VERIFICAR_BLACKLIST : <<include>>
 UC_AUTH_01 ..> REGISTRAR_INTENTO : <<include>>
 UC_AUTH_01 ..> EMITIR_JWT : <<include>>
 UC_AUTH_01 ..> CREAR_SESSION : <<include>>
 UC_AUTH_01 ..> AUDITAR : <<include>>
 LOCKOUT ..> UC_AUTH_01 : <<extend>> (Lockout)

 VALIDAR_CRED --> UserRepo
 VERIFICAR_STATE --> UserRepo
 VERIFICAR_BLACKLIST --> BlacklistedToken
 REGISTRAR_INTENTO --> UserRepo
 CREAR_SESSION --> Session
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_AUTH_01
   UC publico — endpoint sin RBAC
   pre-login. Post-login establece
   view_own_sessions implicita.
 end note

 note bottom of LOCKOUT
   N intentos fallidos disparan
   state=BLOCKED + audit
   ACCOUNT_LOCKED. Recovery via
   UC_AUTH_03.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   credenciales + state.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   record_login_attempt + increment_failed_attempts.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   nueva sesion creada.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   verificar refresh no revocado.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   ValidJWTSpec aplicada.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor LOGIN_SUCCESS / LOGIN_FAILED / ACCOUNT_LOCKED.
 - :doc:`/requisitos/casos-uso/auth/uc-auth-01/index` —
   spec textual.
