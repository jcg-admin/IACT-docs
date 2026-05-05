.. meta::
 :artefacto: AT_DM_CLASS_PERMISSION_CACHE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_permission_cache:

===============
PermissionCache
===============

Cache de resultados de verificación de permisos
(``PermissionService.check``). Reduce la carga sobre la BD
en el path crítico de evaluación de RBAC en cada request.

La invalidación es **explícita y dirigida**: cuando un
usuario cambia sus asignaciones (``Assignment``,
``ExceptionalPermission``) o cambia la composición de un
``AccessGroup`` que el usuario posee, se invalida el cache
del usuario afectado.

.. uml::
 :caption: Clase PermissionCache — cache TTL con
           invalidación dirigida por usuario.

 @startuml

 class PermissionCache {
   - storage_backend : CacheBackend
   - default_ttl : Duration
   --
   + get(key : CacheKey) : CacheEntry
   + set(key : CacheKey, value : Boolean, ttl : Duration) : void
   + invalidate(user_id : UUID) : Integer
   + invalidate_by_function(function_code : String) : Integer
   + invalidate_all() : Integer
   + stats() : CacheStats
 }

 class CacheKey {
   + user_id : UUID
   + function_code : String
   --
   + serialize() : String
 }

 class CacheEntry {
   + value : Boolean
   + cached_at : DateTime
   + expires_at : DateTime
   + hit_count : Integer
 }

 class CacheStats {
   + total_hits : Integer
   + total_misses : Integer
   + hit_rate : Float
   + entry_count : Integer
 }

 PermissionCache ..> CacheKey : keyed_by
 PermissionCache ..> CacheEntry : returns
 PermissionCache ..> CacheStats : reports

 note right of PermissionCache
   Invalidacion dirigida por user_id
   (no flush global) — recovery rapido
   tras cambio de Assignment.
 end note

 @enduml

Operaciones principales
=======================

- ``get(key)`` — devuelve el ``CacheEntry`` si presente y
  no expirado, o ``null``.
- ``set(key, value, ttl)`` — almacena resultado de
  evaluación con TTL.
- ``invalidate(user_id)`` — elimina TODAS las entradas
  cuyo ``CacheKey.user_id`` coincida. Devuelve cantidad
  invalidada.
- ``invalidate_by_function(function_code)`` — invalida
  todas las entradas con ese function_code. Útil cuando
  cambia la semántica de la función.
- ``invalidate_all()`` — flush completo. Operación de
  emergencia.
- ``stats()`` — métricas para monitoreo (hit rate,
  entry count).

Política de invalidación
========================

- Cambio en ``Assignment`` del usuario U →
  ``invalidate(U)``.
- Cambio en ``ExceptionalPermission`` de U →
  ``invalidate(U)``.
- Cambio en ``AccessGroupFunction`` (composición) →
  ``invalidate_all()`` para los users con ese
  ``AccessGroup`` (lista resuelta por servicio
  invocante).

Restricciones aplicables
========================

- TTL acotado: incluso sin invalidación explícita, el
  cache expira para evitar staleness indefinido.
- ``stats`` no expone PII; solo agregados.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`
  — verificación de permiso (consume cache).
- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`
  — gestión de composición (dispara invalidación).
- :doc:`/requisitos/casos-uso/access/uc-acc-06/index`
  — concesión excepcional (dispara invalidación).

Relaciones
==========

- Componente de ``PermissionService`` (composición
  fuerte): el cache no tiene sentido sin el servicio que
  lo consulta.
- Asociado con ``CacheBackend`` (servicio de
  infraestructura: Redis, Memcached, in-memory).
