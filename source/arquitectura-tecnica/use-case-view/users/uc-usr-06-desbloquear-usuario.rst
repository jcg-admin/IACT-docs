.. meta::
 :artefacto: AT_UC_USR_06_USECASE
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

.. _at_uc_usr_06_desbloquear_usuario:

====================================
UC_USR_06 — Desbloquear Usuario
====================================

Vista arquitectonica del UC_USR_06 — desbloqueo
administrativo. Spec textual completa en
:doc:`/requisitos/casos-uso/users/uc-usr-06/index`.

.. uml::

   @startuml

   left to right direction

   actor "unblock_users" as ADMIN
   actor "AuthorizationGuard" as GUARD
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_06" {
     usecase "Desbloquear Usuario" as UC
     usecase "Validar funcion\nunblock_users" as INC1 <<include>>
     usecase "Lookup AuditEvent\nde bloqueo previo" as INC2 <<include>>
     usecase "Emitir AuditEvent\nUSER_UNBLOCKED" as INC3 <<include>>
     usecase "Emitir warning si\nestado inconsistente" as EXT1 <<extend>>
   }

   ADMIN --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC2 --> AUDIT
   INC3 --> AUDIT
   EXT1 --> AUDIT

   note right of UC
     Pre: User.state = BLOCKED
     Post: User.state = ACTIVE
     Inversa de UC_USR_05
     Tambien desbloquea ACCOUNT_LOCKED (BR-015)
   end note

   @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-06/index` —
   spec textual completa.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   transicion state BLOCKED → ACTIVE.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   lookup del bloqueo previo + insert USER_UNBLOCKED.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor USER_UNBLOCKED.
 - :doc:`/arquitectura-tecnica/use-case-view/users/uc-usr-05-bloquear-usuario` —
   operacion inversa.
