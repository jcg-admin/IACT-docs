.. meta::
 :artefacto: AT_IMPL_SEQ_USERS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_users:

============================================================
Implementation View — MOD_Users: Patron de Interaccion
============================================================

Secuencia para "crear usuario" (UC_USR_01) — el flow CRUD
canonico. La asignacion inicial de grupos se delega a
MOD_Access (cross-modulo) dentro de la misma transaccion.

.. uml::
 :caption: MOD_Users impl seq — create user + initial group assignment.

 @startuml

 actor PipelineAdmin
 participant "UserView\n(APIView)" as View <<api>>
 participant "UserSerializer" as Serializer <<serializer>>
 participant "UserService" as Svc <<service>>
 participant "UserRepository" as URepo <<repository>>
 participant "AccessService\n(MOD_Access)" as Access <<service>>
 participant "AuditService" as Audit <<service>>
 database PostgreSQL

 PipelineAdmin -> View : POST /api/v1/users/\n{email, name, initial_groups[]}
 activate View

 View -> View : permission_classes\n[function_perm("create_user")]

 View -> Serializer : .is_valid(...)
 Serializer --> View : validated_data

 View -> Svc : create(validated_data, actor)
 activate Svc

 Svc -> Svc : transaction.atomic block

 Svc -> URepo : create(email, name, password_hash,\nstate=ACTIVE)
 activate URepo
 URepo -> PostgreSQL : INSERT INTO auth_user ...
 URepo --> Svc : User
 deactivate URepo

 loop por cada group_ref
   Svc -> Access : assign(user.id, group_ref, actor)
   activate Access
   note right
     cross-modulo. Esta llamada
     internamente verifica SoD,
     emite audit propio y
     invalida el cache de
     permissions.
   end note
   Access --> Svc : Assignment
   deactivate Access
 end

 Svc -> Audit : record(USER_CREATED, actor, user.id)

 Svc --> View : User
 deactivate Svc

 View -> Serializer : .to_representation(...)
 View --> PipelineAdmin : HTTP 201 + body
 deactivate View

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/users/api/views.py: UserView, UserDetailView,
     BlockUserView``
 * - Serializer
   - ``apps/users/api/serializers.py: UserSerializer,
     CreateUserSerializer``
 * - Service
   - ``apps/users/services/user_service.py``
 * - Repository
   - ``apps/users/repositories/user_repo.py``
 * - ORM
   - ``apps/users/models.py: UserORM``
     (extiende ``django.contrib.auth.models.AbstractUser``)

Invariantes de implementacion
==============================

- **I-IMPL-USR-01:** ``UserService.create`` ejecuta dentro
  de ``transaction.atomic()``. Si cualquier
  ``Access.assign`` falla (e.g. SoD violation), todo se
  revierte: el ``User`` no se persiste.
- **I-IMPL-USR-02:** ``BlockUserView`` revoca tokens JWT
  via ``JWTService.revoke_user_tokens(user.id)`` en la misma
  transaccion (cross-modulo a MOD_Auth).
- **I-IMPL-USR-03:** ``DELETE /api/v1/users/{id}/`` NO
  ejecuta ``DELETE FROM`` en BD — invoca ``UserService.purge``
  que **soft-delete** (``state=DELETED, purged_at=now()``)
  y, despues de retencion, hace el delete fisico via job de
  housekeeping. Cumple GDPR sin perder integridad referencial
  hasta la purga formal.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/users/user-lifecycle` —
   FSM del usuario en DesignView.
 - :doc:`/arquitectura-tecnica/implementation-view/access/interaction-pattern` —
   patron de asignacion invocado.
 - :doc:`/arquitectura-tecnica/implementation-view/auth/jwt-token-lifecycle` —
   patron de revoke al bloquear.
