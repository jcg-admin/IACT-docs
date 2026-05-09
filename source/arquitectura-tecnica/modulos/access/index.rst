.. meta::
 :artefacto: ARQ_MOD_ACCESS
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/access
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq_mod_access:

=================================================
ARQ_MOD_ACCESS: Asignaciones de acceso (Access)
=================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo ``Access`` gestiona el lado **transaccional** de
RBAC: asignacion y revocacion de grupos a usuarios, validacion
de Separation of Duties (SoD), y temporalidad de asignaciones
(``CNST-031``: permisos temporales). Es complementario al
modulo :doc:`/arquitectura-tecnica/modulos/permissions/index`,
que se ocupa de la **resolucion** del conjunto efectivo de
permisos derivado de esas asignaciones.

Separacion de responsabilidades
--------------------------------

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Aspecto
   - ``Access`` (este modulo)
   - ``Permissions``
 * - Pregunta que responde
   - "¿Quien tiene asignado que grupo, hasta cuando?"
   - "¿Que puede hacer este usuario ahora mismo?"
 * - Operaciones tipicas
   - ``assign_group``, ``revoke``, ``check_sod``
   - ``compute_effective_set``, ``has_permission``
 * - Persistencia
   - ``UserGroupAssignment`` (write-heavy)
   - cache derivado en memoria (read-heavy)
 * - UCs principales
   - UC_ACC_01..03 (asignar / revocar / consultar
     asignaciones)
   - UC_PERM_01..03 (consultar permisos efectivos,
     resolver conflicto)

----

2. Responsabilidades
=====================

- **R-ACC-01:** Crear asignaciones ``UserGroupAssignment``
  con ventana de validez ``[valid_from, valid_to]``.
- **R-ACC-02:** Revocar asignaciones (logical revoke con
  ``revoked_at``, no DELETE fisico — preserva historial).
- **R-ACC-03:** Validar SoD antes de cada asignacion via
  el patron de check de incompatibilidades
  (separation-check-flow).
- **R-ACC-04:** Notificar al modulo ``Permissions`` para
  invalidar el cache derivado del usuario afectado.

----

3. Restricciones
=================

- ``CNST-030`` — toda asignacion debe pasar el SoD check
  antes de persistirse.
- ``CNST-031`` — asignaciones temporales requieren
  ``valid_to``; el job de housekeeping las marca
  ``expired`` cuando ``now() > valid_to``.

----

4. Diagramas asociados (DesignView)
=====================================

- :doc:`/arquitectura-tecnica/design-view/access/bounded-context` —
  contexto.
- :doc:`/arquitectura-tecnica/design-view/access/interaction-pattern` —
  patron de orquestacion.
- :doc:`/arquitectura-tecnica/design-view/access/assignment-lifecycle` —
  FSM de ``UserGroupAssignment``.
- :doc:`/arquitectura-tecnica/design-view/access/separation-check-flow` —
  flujo de validacion SoD.

.. seealso::

 - :doc:`/arquitectura-tecnica/modulos/permissions/index` —
   modulo complementario.
 - :doc:`/arquitectura-tecnica/modulos/coexistence-with-design-implementation-view` —
   guia de navegacion entre modulos/, design-view/ e
   implementation-view/.
