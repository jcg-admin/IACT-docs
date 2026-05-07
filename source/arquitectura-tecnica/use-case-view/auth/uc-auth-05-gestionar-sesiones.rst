.. meta::
 :artefacto: AT_UC_AUTH_05_USECASE
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

.. _at_uc_auth_05_gestionar_sesiones:

============================================================
UC_AUTH_05 — Gestionar Sesiones
============================================================

User consulta sesiones activas propias (web, mobile, API) y puede
revocar sesiones individuales (logout remoto). Tambien soporta renovar
JWT tras expiracion (refresh token flow). Funciones implicitas
``view_own_sessions`` + ``revoke_own_session`` (auto-otorgadas
a usuarios autenticados).

.. uml::
 :caption: UC_AUTH_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_own_sessions" as view_own_sessions
 actor "revoke_own_session" as revoke_own_session <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Session" as Session <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_05\nGestionar Sesiones\n.. extension points ..\nRevocar\nRenovarToken" as UC_AUTH_05
   usecase "Validar JWT actual" as VALIDAR_JWT
   usecase "Listar Sessions\nactivas del User" as LISTAR
   usecase "Revocar Session\nespecifica" as REVOCAR
   usecase "Blacklist token\n(reason=SESSION_REVOKED)" as BLACKLIST
   usecase "Renovar JWT\n(refresh token)" as RENOVAR
   usecase "Verificar refresh\nno blacklisted" as VERIFY_REFRESH
   usecase "Emitir AuditEvent\nSESSION_*" as AUDITAR
 }

 view_own_sessions --> UC_AUTH_05
 revoke_own_session --> REVOCAR
 view_own_sessions --> RENOVAR

 UC_AUTH_05 ..> VALIDAR_JWT : <<include>>
 UC_AUTH_05 ..> LISTAR : <<include>>
 REVOCAR ..> UC_AUTH_05 : <<extend>> (Revocar)
 RENOVAR ..> UC_AUTH_05 : <<extend>> (RenovarToken)
 REVOCAR ..> BLACKLIST : <<include>>
 RENOVAR ..> VERIFY_REFRESH : <<include>>
 REVOCAR ..> AUDITAR : <<include>>
 RENOVAR ..> AUDITAR : <<include>>

 LISTAR --> Session
 REVOCAR --> Session
 BLACKLIST --> BlacklistedToken
 VERIFY_REFRESH --> BlacklistedToken
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_AUTH_05
   3 sub-flujos: list (GET),
   revoke (DELETE), refresh (POST
   con refresh token).
 end note

 note bottom of VERIFY_REFRESH
   Refresh token tambien puede
   estar blacklisted (por logout
   o password change). Si lo esta,
   401.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Sessions del User.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   tokens revocados.
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   ValidJWTSpec aplicada.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor SESSION_LISTED / REVOKED / TOKEN_REFRESHED.
 - :doc:`/requisitos/casos-uso/auth/uc-auth-05/index` —
   spec textual.
