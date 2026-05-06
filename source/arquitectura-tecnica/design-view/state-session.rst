.. meta::
 :artefacto: AT_DESIGN_STATE_SESSION
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: Session
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_state_session:

============================================================
Design View — Ciclo de Vida: Session
============================================================

Maquina de estados de la entidad ``Session``. Cubre el ciclo
de una sesion JWT desde el login hasta la expiracion natural,
revocacion explicita (logout) o blacklist.

.. uml::
 :caption: Session FSM — active -> expired | revoked | blacklisted.

 @startuml

 [*] --> active : login()

 active --> active : User.refresh()\n(extiende ttl)

 active --> expired : ExpirationPolicy.ttl_reached
 active --> revoked : User.logout()
 active --> blacklisted : Admin.revoke_user_sessions()

 expired --> [*]
 revoked --> [*]
 blacklisted --> [*]

 note right of active
   Cada request de la session
   pasa por AuthorizationGuard:
   - verifica jwt firmado
   - verifica no en BlacklistedToken
   - verifica exp no rebasado
 end note

 note right of revoked
   logout() agrega el JWT a
   BlacklistedToken hasta que
   exp natural lo elimine.
 end note

 note right of blacklisted
   admin puede revocar TODAS
   las sessions de un usuario
   (e.g. al desactivarlo).
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-auth`
 - :doc:`/arquitectura-tecnica/design-view/act-jwt-auth`
 - :doc:`/arquitectura-tecnica/design-view/class-auth`
 - :doc:`/arquitectura-tecnica/use-case-view/auth/index`
 - :doc:`/arquitectura-tecnica/domain-model/session`
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token`
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy`
