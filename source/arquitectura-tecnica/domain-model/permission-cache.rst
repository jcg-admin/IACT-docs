.. meta::
 :artefacto: AT_DM_CLASS_PERMISSION_CACHE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_permission_cache:

===============
PermissionCache
===============

Cache de resultados de verificacion de permisos. TTL configurable.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase PermissionCache — stub pendiente de desarrollo.

 @startuml

 class PermissionCache {
  + get(key)
  + set(key, value, ttl)
  + invalidate(user_id)
 }

 @enduml
