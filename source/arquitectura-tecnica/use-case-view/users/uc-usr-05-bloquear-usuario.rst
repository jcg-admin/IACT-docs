.. meta::
 :artefacto: AT_UC_USR_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_usr_05_bloquear_usuario:

==================================
UC_USR_05 — Bloquear Usuario
==================================

Vista arquitectonica del UC_USR_05 — bloqueo administrativo
manual de un User. Spec textual completa en
:doc:`/requisitos/casos-uso/users/uc-usr-05/index`.

.. uml::

   @startuml

   left to right direction

   actor "block_users" as ADMIN
   actor "AuthorizationGuard" as GUARD
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_05" {
     usecase "Bloquear Usuario" as UC
     usecase "Validar funcion\nblock_users" as INC1 <<include>>
     usecase "Cerrar sesiones\nactivas" as INC2 <<include>>
     usecase "Blacklistear\ntokens vivos" as INC3 <<include>>
     usecase "Emitir AuditEvent\nUSER_BLOCKED" as INC4 <<include>>
     usecase "Override razon\nsi bloqueo automatico\nprevio" as EXT1 <<extend>>
   }

   ADMIN --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC ..> INC4 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC4 --> AUDIT

   note right of UC
     Pre: User.state = ACTIVE
     Post: User.state = BLOCKED
     Reversible: UC_USR_06
     Distinto de BR-015 (automatico)
   end note

   @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-05/index` —
   spec textual completa.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   transicion state ACTIVE → BLOCKED.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   cierre masivo de sesiones.
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token` —
   blacklisting de refresh tokens.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor USER_BLOCKED.
 - :doc:`/requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos` —
   bloqueo automatico (BR relacionada, semantica distinta).
 - :doc:`/arquitectura-tecnica/use-case-view/users/uc-usr-06-desbloquear-usuario` —
   operacion inversa.
