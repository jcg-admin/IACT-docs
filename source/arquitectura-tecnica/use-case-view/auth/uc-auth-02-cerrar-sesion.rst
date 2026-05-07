.. meta::
 :artefacto: AT_UC_AUTH_02_USECASE
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

.. _at_uc_auth_02_cerrar_sesion:

==============================
UC_AUTH_02 — Cerrar Sesion
==============================

User cierra sesion explicitamente. Sistema agrega ``token_jti`` actual
a ``BlacklistedToken`` con ``reason=LOGOUT`` (TTL hasta ``exp`` del
token original), termina ``Session`` activa. Sin RBAC adicional —
sesion propia.

.. uml::
 :caption: UC_AUTH_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "User autenticado" as User_autenticado
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Session" as Session <<sistema>>
 actor "BlacklistedToken" as BlacklistedToken <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_02\nCerrar Sesion" as UC_AUTH_02
   usecase "Validar JWT actual" as VALIDAR_JWT
   usecase "Blacklist token_jti\n(reason=LOGOUT)" as BLACKLIST
   usecase "Terminar Session\n(state=CLOSED)" as TERMINAR
   usecase "Emitir AuditEvent\nLOGOUT" as AUDITAR
 }

 User_autenticado --> UC_AUTH_02

 UC_AUTH_02 ..> VALIDAR_JWT : <<include>>
 UC_AUTH_02 ..> BLACKLIST : <<include>>
 UC_AUTH_02 ..> TERMINAR : <<include>>
 UC_AUTH_02 ..> AUDITAR : <<include>>

 BLACKLIST --> BlacklistedToken
 TERMINAR --> Session
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of BLACKLIST
   TTL hasta exp del token original.
   Planificador de Tareas purga
   BlacklistedToken expirados.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session terminada.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   token revocado con reason=LOGOUT.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor LOGOUT.
 - :doc:`/requisitos/casos-uso/auth/uc-auth-02/index` —
   spec textual.
