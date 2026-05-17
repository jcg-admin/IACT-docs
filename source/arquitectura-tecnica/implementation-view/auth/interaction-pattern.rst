.. meta::
 :artefacto: AT_IMPL_SEQ_AUTH
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_auth:

============================================================
Implementation View — MOD_Auth: Patron de Interaccion
============================================================

Secuencia de llamadas reales entre las capas Django/DRF para
el flujo de login: validacion de credenciales, emision de
JWT (access + refresh) y registro en ``Session``.

.. uml::
 :caption: MOD_Auth impl seq — login → JWT issuance → session record.

 @startuml

 actor Client
 participant "LoginView\n(APIView)" as View <<api>>
 participant "LoginSerializer" as Serializer <<serializer>>
 participant "AuthService" as Service <<service>>
 participant "UserRepository" as URepo <<repository>>
 participant "JWTService" as JWT <<service>>
 participant "SessionRepository" as SRepo <<repository>>
 participant "AuditService" as Audit <<service>>
 database PostgreSQL

 Client -> View : POST /api/v1/auth/login/\n{username, password}
 activate View

 View -> Serializer : .is_valid(raise_exception=True)
 activate Serializer
 Serializer --> View : validated_data
 deactivate Serializer

 View -> Service : authenticate(username, password)
 activate Service

 Service -> URepo : by_username(username)
 activate URepo
 URepo -> PostgreSQL : SELECT * FROM auth_user ...
 PostgreSQL --> URepo
 URepo --> Service : User | None
 deactivate URepo

 alt user not found or password mismatch
   Service -> Audit : record(LOGIN_FAILED, username)
   Service --> View : raise InvalidCredentials
   View --> Client : HTTP 401 + error_code=INVALID_CREDENTIALS
 else valid
   Service -> JWT : issue_pair(user)
   activate JWT
   note right of JWT
     access_token: jti, sub=user.id, exp=15min.
     refresh_token: jti distinto, exp=7d,
     persistido en RefreshTokenORM.
   end note
   JWT --> Service : (access, refresh, jti_access, jti_refresh)
   deactivate JWT

   Service -> SRepo : create(user, jti_access, jti_refresh, ip, ua)
   activate SRepo
   SRepo -> PostgreSQL : INSERT INTO auth_session ...
   SRepo --> Service : Session
   deactivate SRepo

   Service -> Audit : record(LOGIN_SUCCESS, user.id)

   Service --> View : LoginResult(access, refresh)
 end
 deactivate Service

 View --> Client : HTTP 200 + {access, refresh}
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
   - ``apps/auth/api/views.py: LoginView, LogoutView, RefreshView``
 * - Serializer
   - ``apps/auth/api/serializers.py: LoginSerializer``
 * - Service
   - ``apps/auth/services/auth_service.py: AuthService``
 * - JWT
   - ``apps/auth/services/jwt_service.py: JWTService``
     (issue / decode / revoke)
 * - Repositories
   - ``apps/auth/repositories/user_repo.py``
     ``apps/auth/repositories/session_repo.py``
     ``apps/auth/repositories/refresh_token_repo.py``

Invariantes de implementacion
==============================

- **I-IMPL-AUTH-01:** ``AuthService.authenticate`` ejecuta
  comparacion de password con ``django.contrib.auth.hashers
  .check_password`` — no compara strings directamente.
- **I-IMPL-AUTH-02:** ``Session.create`` y la respuesta al
  cliente forman parte de la misma transaccion DRF; un fallo
  en SessionRepo aborta la respuesta y el JWT no se devuelve.
- **I-IMPL-AUTH-03:** los tokens se firman con clave RS256
  cargada desde ``settings.JWT_PRIVATE_KEY`` (env var). Sin
  fallback a HS256 en runtime.

----

.. seealso::

 - :doc:`layer-structure` — vista de paquetes del modulo.
 - :doc:`jwt-token-lifecycle` — patron transversal de JWT.
 - :doc:`/arquitectura-tecnica/design-view/auth/jwt-authentication-flow` —
   secuencia equivalente en DesignView (dominio).
 - :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
   capa de enforcement que consume el JWT.
