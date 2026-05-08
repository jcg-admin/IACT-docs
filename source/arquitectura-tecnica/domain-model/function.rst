.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_function:

========
Function
========

Unidad atomica de permiso RBAC. Cada funcion corresponde a una
operacion del sistema (p.ej. ``view_reports``, ``acknowledge_alert``).
Las funciones se agrupan en ``AccessGroup`` (via
``FunctionGroupMembership``) y se asignan a usuarios via
``UserAccessGroupAssignment``.

**v5.6.x extension:** se agrega el campo ``is_critical: Boolean`` que
fuerza bypass del servicio de cache en la verificacion de capability
(AP-2b). Cambios al flag solo via Django RunPython data migration —
ver :doc:`/backend/adr-back-010-function-is-critical-governance`.

.. uml::
 :caption: Clase Function v2.0.0 — incluye is_critical (v5.6.x).

 @startuml

 class Function {
   + id : UUID
   + codename : String          <<unique, p.ej. view_reports>>
   + name : String              <<display name>>
   + description : String
   + module : Module
   + is_active : Boolean        <<default True>>
   + is_critical : Boolean      <<default False, v5.6.x>>
   + created_at : DateTime
   + updated_at : DateTime
   --
   + register()                 <<via data migration>>
   + deactivate()               <<manage_function_catalog>>
   + view()                     <<view_assignments>>
   + bypass_cache_required() : Boolean
 }

 enum Module {
   AUTH
   USR
   ACC
   PIP
   RPT
   ALR
   AUD
   LOG
   ADM
   OPR
   SUP
 }

 Function "*" -- "1" Module : belongs_to
 Function "0..1" -- "0..1" MenuItem : wrapped_by\n(v5.6.x)

 note right of Function
   campo is_critical (v5.6.x):
   si True, UserCapabilityResolver
   .has_capability bypassa
   el servicio de cache
   y consulta DB directo.
   Cambios solo via
   data migration con
   review >= 2 (TD-RBAC-03).
 end note

 @enduml

**Campo ``is_critical`` — politica de uso (v5.6.x):**

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - Aspecto
   - Politica
 * - Default
   - ``False`` (mayoria de capabilities usan cache TTL 300s)
 * - True candidatos
   - Capabilities que modifican permisos de otros, modifican
     catalogo RBAC, o son acciones irreversibles
 * - Catalogo inicial True
   - 9 capabilities alineadas al catalogo canonico:
     ``assign_functions``, ``revoke_functions``,
     ``assign_function_groups``, ``revoke_function_group``,
     ``assign_functions_to_group``,
     ``manage_function_catalog``, ``manage_menu_catalog``,
     ``manage_menu_lifecycle``, ``deactivate_users``.
     Ver ADR-BACK-010 §3.3.
 * - Modificable en runtime
   - **No** — solo via Django RunPython data migration con
     review >= 2 aprobaciones
 * - UI admin
   - **Read-only** (django admin con
     ``readonly_fields=("is_critical",)``)
 * - Capability que lo modifica
   - ``manage_critical_function_flag`` — declarada activa en
     v5.6.x pero **sin titular** (TD-RBAC-03)

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function-group`
 :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 :doc:`/arquitectura-tecnica/domain-model/menu-item`
 :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver`
 :doc:`/backend/adr-back-010-function-is-critical-governance`
