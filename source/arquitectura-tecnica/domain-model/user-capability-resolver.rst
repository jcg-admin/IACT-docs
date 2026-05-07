.. meta::
 :artefacto: AT_DM_CLASS_USER_CAPABILITY_RESOLVER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_user_capability_resolver:

======================
UserCapabilityResolver
======================

**v5.6.x extension.** Resolver canonico de capabilities por
usuario. Unico punto de computo: middlewares, endpoints,
serializers y signals consumen este resolver — NUNCA calculan
capabilities ad-hoc.

Implementa los dos sub-patrones AP-2 documentados en
:doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`:

- **AP-2a (read endpoints):** ``resolve()`` cache-first con TTL
  300s y degraded mode.
- **AP-2b (critical capabilities):** ``resolve_uncached()`` y
  ``has_capability()`` que decide cache vs DB segun
  ``Function.is_critical`` (ADR-BACK-010).

.. uml::
 :caption: Clase UserCapabilityResolver v1.0.0 — resolver
           con dos politicas: cache-first y DB-direct para
           capabilities criticas.

 @startuml

 class UserCapabilityResolver <<service>> {
   {static} CACHE_TTL : Integer = 300
   {static} CRITICAL_TTL : Integer = 60
   --
   {static} + resolve(user: User) : Set<String>
   {static} + resolve_uncached(user: User) : Set<String>
   {static} + has_capability(user: User, codename: String) : Boolean
   {static} - _query_db(user: User) : Set<String>
   {static} - _critical_codenames() : Set<String>
 }

 class PermissionCache <<service>> {
   + get(key: String) : Optional<Set<String>>
   + set(key: String, value: Set<String>, ttl: Integer)
   + delete(key: String)
 }

 class Function {
   + codename : String
   + is_critical : Boolean
   + is_active : Boolean
 }

 class User {
   + id : UUID
   + is_authenticated : Boolean
 }

 class UserAccessGroupAssignment {
   + user : User
   + group : AccessGroup
   + expires_at : DateTime <<nullable>>
 }

 UserCapabilityResolver --> PermissionCache : uses (cache-first)
 UserCapabilityResolver --> Function : queries by is_critical
 UserCapabilityResolver --> User : input
 UserCapabilityResolver ..> UserAccessGroupAssignment : queries

 note right of UserCapabilityResolver
   metodo resolve(user):
     Cache key: caps:user:{id}
     TTL: 300s
     On CacheError: degraded mode,
       log + metric, continua a DB.
   --
   metodo has_capability(user, codename):
     Si codename in critical_set:
       usa resolve_uncached (DB-direct)
     Else:
       usa resolve (cache-first)
 end note

 note bottom of UserCapabilityResolver
   AP-2a: capabilities no criticas usan cache.
   AP-2b: capabilities con is_critical=True
          bypassan el servicio de cache.
   Strong consistency en capabilities sensibles.
 end note

 @enduml

**Query DB canonica** (4 JOINs con indices):

.. code-block:: sql

   SELECT DISTINCT f.codename
     FROM functions f
     JOIN function_group_membership fgm
       ON fgm.function_id = f.id
     JOIN access_groups ag
       ON ag.id = fgm.group_id
     JOIN user_access_group_assignment uaga
       ON uaga.group_id = ag.id
    WHERE uaga.user_id = ?
      AND f.is_active = TRUE
      AND (uaga.expires_at IS NULL OR uaga.expires_at > NOW());

P95 ≤ 20ms en cache MISS, P95 ≤ 5ms en cache HIT (ADR-BACK-009).

**13 indices que sostienen P95** (Phase 5 strategy P3):

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Tabla
   - Indices
 * - ``user_access_group_assignment``
   - ``user_id``, ``group_id``, ``(user_id, expires_at)``,
     ``expires_at``
 * - ``function_group_membership``
   - ``group_id``, ``function_id``
 * - ``functions``
   - ``codename``, ``is_active``, ``module``,
     ``(codename, is_active)``
 * - ``menu_items``
   - ``status``, ``(status, display_order)``,
     ``deprecated_at``

**Politica de cache** — degraded mode:

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Operacion
   - Comportamiento normal
   - Comportamiento degraded
 * - ``cache.get`` falla
   - retorna valor cacheado
   - log warning, query DB
 * - ``cache.set`` falla
   - escribe valor + TTL
   - log warning, ignora
 * - ``cache.delete`` falla
   - invalida key
   - log error, telemetria,
     UC continua

**Reemplaza/extiende a** ``EffectivePermissionsAggregator``: el
nuevo resolver consolida la logica de aggregation con la
politica de cache + bypass selectivo. Para v5.6.x se mantiene
``EffectivePermissionsAggregator`` como alias deprecado que
delega a ``UserCapabilityResolver``.

.. seealso::

 :doc:`function`
 :doc:`permission-cache`
 :doc:`assignment`
 :doc:`access-group-function`
 :doc:`effective-permissions-aggregator`
 :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
 :doc:`/backend/adr-back-010-function-is-critical-governance`
 :doc:`/arquitectura-tecnica/cache-strategy`
 :doc:`/backend/rbac-implementation-guide`
