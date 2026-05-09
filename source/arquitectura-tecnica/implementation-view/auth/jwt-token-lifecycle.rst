.. meta::
 :artefacto: AT_IMPL_PATTERN_JWT_LIFECYCLE
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_jwt_lifecycle:

============================================================
Implementation View — JWT Token Lifecycle (jti blacklist)
============================================================

Patron transversal de gestion de tokens JWT: emision,
verificacion en cada request, refresh, y revocacion via
``jti`` blacklist. Documenta restricciones de implementacion
no obvias que ningun developer puede deducir del DesignView
solo.

Estructura del token
=====================

.. code-block:: text

   header (RS256)
   payload:
     sub: user.id            (subject)
     jti: <uuid4>             (JWT ID — clave del blacklist)
     iat: <timestamp>         (issued at)
     exp: <timestamp>         (expiration)
     type: "access"|"refresh"
     session_id: <uuid>       (link a Session ORM)
   signature

Issue + verify (hot path)
==========================

.. uml::
 :caption: JWT verify — hot path en cada request.

 @startuml

 participant "DRF View" as View
 participant "JWTAuthentication\n(custom backend)" as JWTAuth <<auth>>
 participant "JWTService" as JWT <<service>>
 participant "JtiBlacklistCache" as Cache <<cache>>
 participant "RefreshTokenORM" as ORM <<orm>>

 View -> JWTAuth : authenticate(request)
 activate JWTAuth

 JWTAuth -> JWT : decode(token, RS256)
 activate JWT
 alt firma invalida o exp vencido
   JWT --> JWTAuth : raise InvalidToken
   JWTAuth --> View : None (DRF responde 401)
 else firma OK
   JWT --> JWTAuth : payload (sub, jti, ...)
 end
 deactivate JWT

 JWTAuth -> Cache : is_revoked(jti)
 activate Cache
 note right of Cache
   Cache en memoria (LRU + TTL).
   Refrescado via Django signal
   cuando RefreshTokenRepo.revoke
   se ejecuta. ADR-BACK-012:
   sin Redis, in-process per worker.
 end note
 alt jti en blacklist
   Cache --> JWTAuth : True
   JWTAuth --> View : None (401)
 else
   Cache --> JWTAuth : False
   JWTAuth --> View : (User, payload)
 end
 deactivate Cache
 deactivate JWTAuth

 @enduml

Refresh + revoke
=================

.. uml::
 :caption: refresh + logout — agrega jti al blacklist.

 @startuml

 actor Client
 participant "RefreshView\nLogoutView" as View <<api>>
 participant "JWTService" as JWT <<service>>
 participant "RefreshTokenRepository" as RTRepo <<repository>>
 participant "JtiBlacklistCache" as Cache <<cache>>

 == Refresh ==
 Client -> View : POST /api/v1/auth/refresh/\n{refresh}
 View -> JWT : decode(refresh)
 alt invalido / revocado
   View --> Client : HTTP 401
 else OK
   View -> RTRepo : rotate(old_jti, new_pair)
   note right of RTRepo
     rotate atomico:
     1) marca old_jti = revoked
     2) emite nuevo refresh con jti distinto
   end note
   RTRepo -> Cache : invalidate(old_jti)
   View --> Client : HTTP 200 + {access, refresh nuevo}
 end

 == Logout ==
 Client -> View : POST /api/v1/auth/logout/
 View -> RTRepo : revoke_all_for_session(session_id)
 RTRepo -> Cache : invalidate_many(jtis)
 View --> Client : HTTP 204

 @enduml

Restricciones de implementacion
================================

- **R-JWT-01:** ``access_token`` NO se persiste — solo el
  ``refresh_token`` con su ``jti`` y ``revoked_at``. La
  blacklist es para ``jti`` de refresh tokens y de access
  tokens revocados explicitamente (e.g. por bloqueo de
  usuario en :doc:`/arquitectura-tecnica/design-view/users/user-lifecycle`).
- **R-JWT-02:** la blacklist cache tiene **TTL = JWT.exp**.
  Una vez expira, el jti se purga automaticamente (no hay
  garbage collection separado).
- **R-JWT-03:** sin Redis (ADR-BACK-012). El cache es
  per-process. Multi-worker invalida via ``django.dispatch
  .Signal`` capturada por todos los workers del host.
  Cross-host no aplica (single-host deploy actual).
- **R-JWT-04:** RS256 obligatorio. La privada se carga desde
  ``settings.JWT_PRIVATE_KEY``. La publica se sirve via
  ``GET /api/v1/auth/.well-known/jwks.json`` para clientes
  externos.
- **R-JWT-05:** ``jti`` es ``uuid4`` — colision practicamente
  imposible. NO usar contadores monotonicos.

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - JWTService
   - ``apps/auth/services/jwt_service.py``
 * - JWTAuthentication backend
   - ``apps/auth/authentication.py: JWTAuthentication``
 * - JtiBlacklistCache
   - ``apps/auth/services/jti_blacklist.py``
 * - RefreshTokenRepository
   - ``apps/auth/repositories/refresh_token_repo.py``
 * - Signals
   - ``apps/auth/signals.py: jti_revoked``

----

.. seealso::

 - :doc:`interaction-pattern` — login flow que emite los
   tokens.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/auth/session-lifecycle` —
   ciclo de vida de sesion en DesignView.
 - :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
   patron de RBAC que consume los tokens.
