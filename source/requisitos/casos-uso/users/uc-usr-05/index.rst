.. meta::
 :artefacto: UC_USR_05
 :tipo: Caso de Uso (Spec Completa)
 :dominio: requisitos
 :subdominio: casos_uso/users
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante
 :normativa: CNST-009, CNST-013, CNST-025, CNST-026

.. _uc-usr-05:

==============================
UC_USR_05 — Bloquear Usuario
==============================

.. note::

 **Especificacion completa de 12 partes** — promocion del
 placeholder Reservado a spec Aprobada por el WP
 ``2026-05-08-04-10-27-uc-view-domain-alignment``.

Resumen
=======

UC_USR_05 ejecuta el **bloqueo administrativo manual** de
un User por parte de un admin. Transicion
``User.state: ACTIVE → BLOCKED``, cierre de Sessions
activas y emision de AuditEvent ``USER_BLOCKED``. La
cuenta se conserva (no es DELETE ni soft-delete); puede
ser desbloqueada por UC_USR_06.

Distinto de:

- **UC_USR_04 (eliminar)** — baja logica permanente
  (``state → ELIMINATED``), no reversible.
- **BR-015 (bloqueo automatico)** — transicion a BLOCKED
  disparada por el sistema tras N intentos fallidos. UC_USR_05
  es el equivalente manual con admin como actor.

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_USR_05
 * - **Modulo**
   - MOD_Users
 * - **Criticidad**
   - ALTA (afecta acceso del usuario; reversible via UC_USR_06)
 * - **Complejidad**
   - BAJA (1 dia)
 * - **Actor Principal**
   - User con funcion ``block_users``
 * - **Funcion RBAC**
   - ``block_users``
 * - **BReq satisfecho**
   - BReq-004 (Cumplimiento de Seguridad y Auditoria)
 * - **BRQ legacy**
   - BRQ-USR-005 (parcial)

Documentos vinculados
=====================

- :doc:`/requisitos/business-requirements/breq-004-cumplimiento-seguridad-auditoria`
- :doc:`/requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos`
  (bloqueo automatico — semantica relacionada pero distinta)
- :doc:`/requisitos/casos-uso/users/uc-usr-06/index`
  (desbloqueo — operacion inversa)
- :doc:`/requisitos/casos-uso/users/uc-usr-04/index`
  (eliminar — baja logica permanente, NO reversible)
- :doc:`/requisitos/casos-uso/auth/uc-auth-05/index`
  (gestion de sessions — patron similar de cierre masivo)

Estructura de la spec
=====================

.. toctree::
 :maxdepth: 1
 :caption: Las 12 partes

 informacion-general
 actores-precondiciones
 flujo-principal
 flujos-alternos
 excepciones
 requisitos-no-funcionales
 datos-involucrados
 diagramas-uml/index
 criterios-aceptacion
 patrones-diseno
 implementacion-tecnica
 testing
