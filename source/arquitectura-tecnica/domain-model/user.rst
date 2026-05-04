.. meta::
 :artefacto: AT_DM_CLASS_USER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Auth
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_user:

====
User
====

Entidad central del bounded context Auth. Representa a un usuario
del sistema IACT con su ciclo de vida (ACTIVE → INACTIVE → BLOCKED).
La identidad de un usuario nunca se borra, solo se desactiva (BR-009
v2.0.0).

.. uml::
 :caption: Clase User — entidad de identidad del sistema IACT.

 @startuml

 class User {
   + user_id : UUID
   + username : String
   + email : String
   + full_name : String
   + state : UserState
   + created_at : DateTime
   + last_login_at : DateTime
   + primary_access_group_id : String
   --
   + create()
   + deactivate()       <<BR-009 v2.0.0>>
   + modify()
   + view()
   + recover_password()
 }

 enum UserState {
   ACTIVE
   INACTIVE
   BLOCKED
 }

 class Session {
   + session_id : UUID
   + state : SessionState
 }

 class InternalMailbox {
   + mailbox_id : UUID
   + owner_user_id : UUID
 }

 enum SessionState {
   ACTIVE
   CLOSED
   EXPIRED
 }

 User -- UserState
 User "1" -- "0..*" Session            : posee
 User "1" -- "1"    InternalMailbox    : posee
 Session -- SessionState

 note bottom of User
   BR-009 v2.0.0: desactivar, no eliminar.
   primary_access_group_id referencia AGR-001..012.
 end note

 note bottom of Session
   CNST-002: timeout de sesion.
   CNST-003: una sola sesion activa por usuario.
 end note

 note bottom of InternalMailbox
   CNST-001: buzon interno unicamente,
   sin canal de email externo.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/session`
 :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
