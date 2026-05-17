.. meta::
 :artefacto: AT_DM_CLASS_SESSION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_session:

=======
Session
=======

Sesion activa de un usuario. Tiene caducidad controlada por
CNST-002 (timeout) y CNST-003 (una sola sesion activa por usuario).
El cierre puede ser por el propio usuario, por un administrador
o por timeout.

.. uml::
 :caption: Clase Session — sesion autenticada con ciclo de vida.

 @startuml

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

 enum SessionState {
   ACTIVE
   CLOSED
   EXPIRED
 }

 Session -- SessionState

 note bottom of Session
   CNST-002: timeout de sesion.
   CNST-003: una sola sesion activa por usuario.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/user`
