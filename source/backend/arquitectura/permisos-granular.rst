:orphan:

.. meta::
 :artefacto: BACK_ARQ_PERMISOS_GRANULAR
 :tipo: Documentacion de Arquitectura
 :dominio: backend
 :subdominio: arquitectura
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Importante

.. _back_arq_permisos_granular:

============================================================
Sistema de Permisos Granular
============================================================

Esta pagina es un punto de entrada al sistema RBAC de IACT.
El modelo conceptual y operativo se documenta en detalle en:

- :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` —
  modelo RBAC autoritativo.
- :doc:`/arquitectura-tecnica/modulos/permissions/index` —
  modulo arquitectonico de resolucion de permisos.
- :doc:`/arquitectura-tecnica/modulos/access/index` —
  modulo de asignaciones.
- :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
  patron de enforcement transversal.
- :doc:`/arquitectura-tecnica/implementation-view/permissions/effective-set-cache-pattern` —
  cache LRU + TTL de permisos efectivos.

----

Resumen del modelo
===================

El RBAC de IACT es **flat** (sin jerarquia de roles —
ver :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`)
con tres entidades principales:

- ``User`` — usuario autenticado.
- ``FunctionGroup`` — agrupacion de funciones (``Function``)
  asignable a usuarios via ``Assignment``.
- ``Function`` — capacidad atomica del sistema
  (codename, e.g. ``view_pipeline_status``).

Granularidad
=============

El catalogo cuenta con ~64 funciones atomicas activas que
cubren todas las operaciones expuestas por la API DRF.
Cada operacion (``GET``, ``POST``, ``DELETE``, ...) tiene
su funcion asociada — no hay "mega-permisos" tipo
``admin_all``.

Resolucion en runtime
======================

La resolucion del **conjunto efectivo** de un usuario
(union de funciones de los grupos asignados, filtrada por
ventana de validez) se documenta en:

- :doc:`/arquitectura-tecnica/design-view/permissions/effective-set-evaluation-flow`
- :doc:`/arquitectura-tecnica/implementation-view/permissions/interaction-pattern`

----

.. seealso::

 - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` —
   modelo RBAC autoritativo.
 - :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia` —
   ADR sobre flat RBAC.
 - :doc:`/backend/adr-back-003-orm-sql-hybrid-permissions` —
   ADR sobre estrategia hybrid ORM/SQL.
