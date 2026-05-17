.. meta::
 :artefacto: AT_DM_CLASS_USER_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_user_repo:

========
UserRepo
========

Repositorio CRUD de ``User``. Es el punto unico de escritura para
crear, modificar, desactivar y consultar usuarios del sistema. BR-009
(bajas logicas): no permite DELETE — la desactivacion transita
``state`` a ``INACTIVE`` o ``BLOCKED`` preservando historial.

Consume ``PasswordGenerator`` al crear users (UC_USR_01) y emite
``AuditEvent`` por cada operacion (USER_CREATED, USER_UPDATED,
USER_DEACTIVATED, USER_BLOCKED).

.. uml::
 :caption: Clase UserRepo — CRUD de User con bajas logicas.

 @startuml

 class UserRepo {
   - storage_backend : StorageBackend
   --
   + create(user : User) : UUID
   + get_by_id(user_id : UUID) : User
   + get_by_username(username : String) : User
   + get_by_email(email : String) : User
   + find_by_segment(segment_code : String) : List<User>
   + find_active() : List<User>
   + update(user_id : UUID, changes : Map) : User
   + deactivate(user_id : UUID, actor_id : UUID, reason : String) : User
   + block(user_id : UUID, actor_id : UUID, reason : String) : User
   + record_login_attempt(user_id : UUID, success : Boolean) : void
   + increment_failed_attempts(user_id : UUID) : Integer
   + count_active() : Integer
 }

 class User

 UserRepo "1" --> "*" User : gestiona

 note bottom of UserRepo
   BR-009 bajas logicas — no DELETE.
   CNST-008 isolation por segmento.
   CNST-026 sin PII en logs.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben:

- :doc:`/requisitos/casos-uso/users/uc-usr-01/index` —
  crear usuario: create + emit USER_CREATED.
- :doc:`/requisitos/casos-uso/users/uc-usr-02/index` —
  modificar usuario: update.
- :doc:`/requisitos/casos-uso/users/uc-usr-03/index` —
  desactivar usuario: deactivate (state=INACTIVE).
- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index` —
  iniciar sesion: record_login_attempt(success=True).

UCs que leen:

- :doc:`/requisitos/casos-uso/users/uc-usr-04/index` —
  consultar usuarios: find_by_segment, find_active.

Relaciones
==========

- :doc:`user` — entity gestionada.
- :doc:`password-generator` — invocado en create.
- :doc:`assignment-repo` — verifica que User no tenga assignments antes
  de delete logical (no aplica DELETE en este repo, pero coherencia
  cross-repo).
- :doc:`audit-service` — emite USER_*.
