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

Diagrama de clases — modulo identidad
=======================================

.. uml::
 :caption: Clases de identidad de usuario con atributos clave.

 @startuml

 class User {
   +id: int
   +username: str
   +email: str
   +is_active: bool
   +date_joined: datetime
   +last_login: datetime
   +create(): User
   +deactivate(): void
 }

 class Session {
   +user: User
   +jwt_token: str
   +ip_origen: str
   +created_at: datetime
   +expires_at: datetime
   +invalidate(): void
 }

 class AuditEvent {
   +user_id: int
   +accion: str
   +entidad: str
   +timestamp: datetime
   +ip_origen: str
 }

 User "1" *-- "0..*" Session
 User "1" --> "0..*" AuditEvent : genera

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/user-identity/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
