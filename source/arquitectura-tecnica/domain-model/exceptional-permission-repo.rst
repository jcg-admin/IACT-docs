.. meta::
 :artefacto: AT_DM_CLASS_EXCEPTIONAL_PERMISSION_REPO
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

.. _dm_class_exceptional_permission_repo:

==========================
ExceptionalPermissionRepo
==========================

Repositorio CRUD de ``ExceptionalPermission`` (concesiones
o revocaciones excepcionales de ``Function`` específicas a
usuarios, fuera del modelo ``AccessGroup``). Modela la
necesidad de excepciones con ventana temporal:
``valid_from``, ``valid_until``.

Operaciones de escritura emiten ``AuditEvent``
(responsabilidad del servicio) y disparan invalidación de
``PermissionCache`` (CNST-031 rango temporal exige
re-evaluación al expirar).

.. uml::
 :caption: Clase ExceptionalPermissionRepo — CRUD de
           permisos excepcionales con soporte temporal.

 @startuml

 class ExceptionalPermissionRepo {
   - storage_backend : StorageBackend
   --
   + grant(user_id : UUID, function_code : String, \
           valid_from : DateTime, valid_until : DateTime, \
           reason : String, granted_by : UUID) : UUID
   + revoke(exceptional_permission_id : UUID, \
            actor_user_id : UUID, reason : String) : ExceptionalPermission
   + find_active_by_user(user_id : UUID, at : DateTime) : List<ExceptionalPermission>
   + find_expiring_in(days : Integer) : List<ExceptionalPermission>
   + get_by_id(exceptional_permission_id : UUID) : ExceptionalPermission
 }

 class ExceptionalPermission
 class TemporalFilter {
   + valid_at : DateTime
   + state : ExceptionalState
 }

 ExceptionalPermissionRepo ..> ExceptionalPermission : persists
 ExceptionalPermissionRepo ..> TemporalFilter : queries with

 note right of ExceptionalPermissionRepo
   find_expiring_in: feed para alertas
   y workflow de renovacion. CNST-031
   exige rango temporal explicito.
 end note

 @enduml

Operaciones principales
=======================

- ``grant(...)`` — concede un permiso excepcional con
  ventana temporal. Razón obligatoria por trazabilidad.
- ``revoke(id, actor, reason)`` — revocación anticipada.
  Marca como ``REVOKED`` antes de su expiración natural.
- ``find_active_by_user(user_id, at)`` — devuelve
  excepcionales válidos en el momento ``at``. Usado por
  ``PermissionService``.
- ``find_expiring_in(days)`` — query de mantenimiento:
  permisos que expiran en N días. Útil para workflows
  de renovación y alertas.

Restricciones aplicables
========================

- **CNST-031** — rango temporal obligatorio:
  ``valid_from`` ≤ ``valid_until``.
- **BR-009** — bajas lógicas: ``revoke`` no DELETE.
- **CNST-025** — auditoría obligatoria (responsabilidad
  del servicio invocante).
- **P-32** — reason-required en ``grant`` y ``revoke``.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/access/uc-acc-06/index` —
  concesión excepcional (``grant``).
- :doc:`/requisitos/casos-uso/access/uc-acc-07/index` —
  revocación excepcional (``revoke``).
- :doc:`/requisitos/casos-uso/access/uc-acc-09/index` —
  vencimiento de agrupador (cron consume
  ``find_expiring_in``).

Relaciones
==========

- Persiste y consulta ``ExceptionalPermission``.
- Usado por ``RBACRepo`` (delegación) y por servicios
  de gestión de permisos (escritura).
