.. meta::
 :artefacto: AT_DOMINIO_01_AUTH
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_auth:

========================================
Modelo de Dominio — Bounded Context Auth
========================================

4.1 Auth
--------

Tres clases: ``User``, ``Session`` y ``InternalMailbox``. La clase
``User`` es la entidad central; ``Session`` representa una sesion
activa con caducidad; ``InternalMailbox`` es el canal de
notificacion interno (sin email externo, CNST-001).

.. uml::
 :caption: Bounded context Auth — usuarios, sesiones y buzon
           interno.

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

 class Session {
   + session_id : UUID
   + user_id : UUID
   + started_at : DateTime
   + last_activity_at : DateTime
   + expires_at : DateTime
   + state : SessionState
   + client_info : String
   --
   + open()
   + close()              <<sesion propia>>
   + close_all()          <<admin: view_all_active_sessions>>
   + view_own_sessions()  <<view_own_sessions>>
 }

 class InternalMailbox {
   + mailbox_id : UUID
   + owner_user_id : UUID
   + last_read_at : DateTime
   --
   + deliver_message()
   + view_messages()
   + mark_read()
 }

 enum UserState {
   ACTIVE
   INACTIVE
   BLOCKED
 }

 enum SessionState {
   ACTIVE
   CLOSED
   EXPIRED
 }

 User "1" -- "0..*" Session            : posee
 User "1" -- "1"    InternalMailbox    : posee
 User -- UserState
 Session -- SessionState

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

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
