.. meta::
 :artefacto: ARQ_MOD_002_DIAG_CLASES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/user-identity/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_002_clases_modulo_identidad:

=====================================
Diagrama de clases — modulo identidad
=====================================

.. uml::
 :caption: Clases de identidad de usuario con atributos clave.

 @startuml

 class User {
   +user_id: UUID
   +username: String
   +email: String
   +state: UserState
   +created_at: DateTime
   +last_login_at: DateTime
   +create()
   +deactivate()     <<BR-009 v2.0.0>>
   +modify()
 }
 enum UserState {
  ACTIVE
  INACTIVE
  BLOCKED
 }
 User -- UserState

 class Session {
   +session_id: UUID
   +user_id: UUID
   +started_at: DateTime
   +expires_at: DateTime
   +state: SessionState
   +open()
   +close()
 }
 enum SessionState {
  ACTIVE
  CLOSED
  EXPIRED
 }
 Session -- SessionState

 class AuditEvent {
   +event_id: UUID
   +event_type: EventType
   +details: JSON
   +occurred_at: DateTime
   +record()
   +search()
 }

 User "1" *-- "0..*" Session
 User "1" --> "0..*" AuditEvent : genera

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/user-identity/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
