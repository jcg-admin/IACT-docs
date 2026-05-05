.. meta::
 :artefacto: AT_DM_CLASS_BLACKLISTED_TOKEN
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_blacklisted_token:

================
BlacklistedToken
================

Registro de tokens JWT revocados. Permite invalidar sesiones antes de que
expire el ``exp`` del token original (logout explicito, deteccion de
compromiso, cambio de password). Cada entry tiene TTL hasta el ``exp``
del token original — pasada esa fecha el registro se purga porque el
token ya esta naturalmente expirado.

Consultado por ``AuthorizationGuard`` y por ``Session.validate()`` antes
de aceptar cualquier token. Si el ``token_jti`` esta en la lista, el
request se rechaza con 401.

.. uml::
 :caption: Clase BlacklistedToken — JWT revocados con TTL.

 @startuml

 class BlacklistedToken {
   + token_jti : String
   + user_id : UUID
   + reason : RevocationReason
   + revoked_at : DateTime
   + expires_at : DateTime
   --
   + add(token_jti : String, user_id : UUID, reason : RevocationReason, expires_at : DateTime) : void
   + is_blacklisted(token_jti : String) : Boolean
   + purge_expired() : Integer
 }

 enum RevocationReason {
   LOGOUT
   PASSWORD_CHANGED
   COMPROMISED
   ADMIN_REVOKED
   SESSION_REVOKED
 }

 BlacklistedToken -- RevocationReason

 note bottom of BlacklistedToken
   TTL = exp del token original.
   Purga periodica via cron. CNST-008
   isolation por user_id.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben en BlacklistedToken (revocan):

- :doc:`/requisitos/casos-uso/auth/uc-auth-02/index` —
  cierre de sesion: agrega ``token_jti`` con reason=LOGOUT.
- :doc:`/requisitos/casos-uso/auth/uc-auth-03/index` —
  cambio de contraseña: agrega tokens activos con reason=PASSWORD_CHANGED.
- :doc:`/requisitos/casos-uso/auth/uc-auth-04/index` —
  cambio de contraseña: invalida sesiones activas.

UCs que leen (consultan):

- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index` —
  inicio de sesion: verifica que el refresh token no este blacklisted.
- :doc:`/requisitos/casos-uso/auth/uc-auth-05/index` —
  renovar token: rechaza si ``token_jti`` esta blacklisted.

Relaciones
==========

- :doc:`session` — toda Session emite token_jti que puede entrar a esta lista.
- :doc:`user` — User cuyos tokens se revocan.
- :doc:`audit-service` — emite ``TOKEN_BLACKLISTED`` por cada add.
