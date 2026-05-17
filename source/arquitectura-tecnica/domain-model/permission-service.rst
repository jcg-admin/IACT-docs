.. meta::
 :artefacto: AT_DM_CLASS_PERMISSION_SERVICE
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

.. _dm_class_permission_service:

=================
PermissionService
=================

Servicio determinístico de **verificación de permisos
RBAC**. Es el punto único de evaluación: toda decisión de
autorización en el sistema (decoradores, middleware,
endpoints) consulta este servicio.

Implementa el **algoritmo canónico de resolución** del
``effective_set`` de un usuario:

1. Recupera ``Assignment`` activos del usuario.
2. Resuelve cada ``Assignment`` → ``AccessGroup`` →
   ``AccessGroupFunction`` → ``Function``.
3. Aplica ``ExceptionalPermission`` (positivos suman,
   negativos restan).
4. Verifica si la ``function_code`` consultada está en el
   set resultante.

El servicio consulta primero ``PermissionCache``; en miss
recalcula y persiste en cache.

.. uml::
 :caption: Clase PermissionService — verificación
           determinística de permisos RBAC con cache.

 @startuml

 class PermissionService {
   - rbac_repo : RBACRepo
   - cache : PermissionCache
   --
   + check(user_id : UUID, function_code : String, ctx : RequestContext) : CheckResult
   + check_bulk(user_id : UUID, function_codes : Set<String>, ctx : RequestContext) : BulkCheckResult
   + effective_set(user_id : UUID) : Set<String>
   - resolve_from_assignments(user_id : UUID) : Set<String>
   - apply_exceptional(user_id : UUID, base_set : Set<String>) : Set<String>
 }

 class CheckResult {
   + allowed : Boolean
   + reason : DenialReason
   + cached : Boolean
 }

 class BulkCheckResult {
   + results : Map<String, CheckResult>
   + cache_hit_rate : Float
 }

 enum DenialReason {
   NO_ASSIGNMENT
   FUNCTION_NOT_IN_GROUP
   EXCEPTION_DENIES
   USER_INACTIVE
   USER_BLOCKED
 }

 class RBACRepo
 class PermissionCache

 PermissionService "1" o-- "1" RBACRepo : reads
 PermissionService "1" *-- "1" PermissionCache : composes
 PermissionService "1" ..> "1" CheckResult : <<returns>>
 PermissionService "1" ..> "1" BulkCheckResult : <<returns>>
 CheckResult "0..*" -- "0..1" DenialReason : justified_by

 note right of PermissionService
   Determinismo: dado el mismo (user_id,
   function_code) y el mismo estado RBAC,
   el resultado es identico siempre.
 end note

 @enduml

Operaciones principales
=======================

- ``check(user_id, function_code, ctx)`` — verificación
  unitaria. Devuelve ``CheckResult`` con ``allowed``
  booleano y ``reason`` documentando la denegación si
  aplica.
- ``check_bulk(user_id, function_codes, ctx)`` — batch
  para múltiples códigos. Optimiza calculando
  ``effective_set`` una sola vez y validando contra el
  set.
- ``effective_set(user_id)`` — devuelve el conjunto
  completo de funciones efectivas del usuario.
- ``resolve_from_assignments(user_id)`` — operación
  privada: resuelve por groups+functions.
- ``apply_exceptional(user_id, base_set)`` — operación
  privada: aplica permisos excepcionales (suma o resta).

Restricciones aplicables
========================

- **CNST-031** rango temporal: ``ExceptionalPermission``
  solo aplica si ``now`` ∈
  [``granted_at``, ``expires_at``].
- **Determinismo** — mismo input → mismo output dado
  el mismo estado de BD.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`
  — UC principal de verificación.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — usado por ``MenuAssembler`` para filtrar Action.
- TODOS los UCs vía decoradores/middleware de
  autorización.

Relaciones
==========

- Agregación con ``RBACRepo`` (el repo existe
  independientemente).
- Composición con ``PermissionCache`` (el cache es interno
  al servicio).
