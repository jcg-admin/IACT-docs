.. meta::
 :artefacto: AT_UC_USR_07_USECASE
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

.. _at_uc_usr_07_editar_perfil_propio:

====================================
UC_USR_07 — Editar Perfil Propio
====================================

Vista arquitectonica del UC_USR_07 — self-service edit
del propio perfil. Spec textual completa en
:doc:`/requisitos/casos-uso/users/uc-usr-07/index`.

.. uml::

   @startuml

   left to right direction

   actor "edit_own_profile" as USER
   actor "AuthorizationGuard" as GUARD
   actor "EmailValidator" as EMAIL
   actor "AuditService" as AUDIT

   rectangle "Sistema IACT — UC_USR_07" {
     usecase "Editar Perfil Propio" as UC
     usecase "Validar funcion\nedit_own_profile" as INC1 <<include>>
     usecase "Validar formato\ny unicidad email" as INC2 <<include>>
     usecase "Emitir AuditEvent\nPROFILE_UPDATED" as INC3 <<include>>
     usecase "Sin diff →\nno emit AuditEvent" as EXT1 <<extend>>
   }

   USER --> UC

   UC ..> INC1 : <<include>>
   UC ..> INC2 : <<include>>
   UC ..> INC3 : <<include>>
   UC <.. EXT1 : <<extend>>

   INC1 --> GUARD
   INC2 --> EMAIL
   INC3 --> AUDIT

   note right of UC
     Self-service: actor = target.
     target_user_id = jwt.user_id
     (no en URL — defensa contra
     impersonation).
     Whitelist EDITABLE_FIELDS_SELF
     = {full_name, email}.
   end note

   @enduml

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-07/index` —
   spec textual completa.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   escritura de full_name / email.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor PROFILE_UPDATED (sin PII en payload).
 - :doc:`/requisitos/casos-uso/users/uc-usr-03/index` —
   modificacion administrativa (campos sensibles).
 - :doc:`/requisitos/casos-uso/auth/uc-auth-04/index` —
   cambiar password (credencial — fuera de UC_USR_07).
