.. meta::
 :artefacto: ARQ_MOD_ADMIN
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq_mod_admin:

============================================================
ARQ_MOD_ADMIN: Administracion del sistema (Admin)
============================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo ``Admin`` agrupa las **operaciones administrativas**
del sistema IACT que no pertenecen a un dominio especifico:
gestion del catalogo de funciones (``UC_ADM_01``), gestion del
catalogo de agrupadores (``UC_ADM_03``), gestion de items de
menu (``UC_ADM_05``) y configuracion de parametros del
sistema. Es el modulo "back-office" de configuracion.

----

2. Responsabilidades
=====================

- **R-ADM-01:** CRUD del catalogo de ``Function`` (entidades
  del modelo de permisos).
- **R-ADM-02:** CRUD del catalogo de ``Agrupador``
  (representacion logica de grupos pre-definidos del sistema).
- **R-ADM-03:** Gestion de ``MenuItem`` con su FSM
  (DRAFT / ACTIVE / DEPRECATED / ARCHIVED) — ver
  :doc:`/arquitectura-tecnica/design-view/admin/menu-item-lifecycle`.
- **R-ADM-04:** Configuracion de parametros del sistema
  (``job_config``, umbrales, etc.).

Distincion vs. otros modulos
-----------------------------

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Pregunta
   - Modulo correcto
 * - "¿Que funciones existen en el catalogo?"
   - ``Admin`` (gestion del catalogo)
 * - "¿Que permisos tiene este usuario?"
   - ``Permissions`` (resolucion efectiva)
 * - "¿Que grupos tiene asignados este usuario?"
   - ``Access`` (asignacion)
 * - "¿Quien hizo este cambio?"
   - ``Audit`` (trazabilidad regulatoria)

----

3. Restricciones
=================

- ``CNST-005`` — el catalogo de ``Function`` es
  append-only en runtime; remover una function requiere
  migracion de datos manual.
- ``CNST-016`` — cambios en ``Agrupador`` requieren
  ``ADM_ADMIN`` permission y se registran en ``AuditEvent``.

----

4. Diagramas asociados (DesignView)
=====================================

- :doc:`/arquitectura-tecnica/design-view/admin/bounded-context` —
  contexto.
- :doc:`/arquitectura-tecnica/design-view/admin/interaction-pattern` —
  patron de orquestacion.
- :doc:`/arquitectura-tecnica/design-view/admin/menu-item-lifecycle` —
  FSM de ``MenuItem``.

.. seealso::

 - :doc:`/arquitectura-tecnica/modulos/coexistence-with-design-implementation-view` —
   guia de navegacion.
 - :doc:`/arquitectura-tecnica/domain-model/menu-item` —
   entidad principal gestionada.
 - :doc:`/arquitectura-tecnica/domain-model/function` —
   catalogo de capabilities.
