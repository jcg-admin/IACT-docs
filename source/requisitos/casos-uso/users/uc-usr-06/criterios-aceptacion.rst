.. _uc-usr-06-parte-06:

==========================================
Parte 6 — Criterios de aceptacion
==========================================

CA-01: Desbloqueo nominal de User BLOCKED por admin previo
============================================================

  | **Given** un admin con funcion ``unblock_users`` activa,
  |   y un User en ``state=BLOCKED`` con AuditEvent previo
  |   ``USER_BLOCKED`` (block_event_id = e1).
  | **When** invoca ``POST /users/{id}/unblock`` con
  |   ``reason='investigacion concluida sin sancion'``.
  | **Then** la respuesta es ``200 OK``,
  |   ``User.state = ACTIVE``,
  |   existe ``AuditEvent USER_UNBLOCKED`` con
  |   ``original_block_event_id = e1``,
  |   ``original_block_type = 'USER_BLOCKED'``,
  |   ``reason = '...'``.

CA-02: Desbloqueo de User BLOCKED por BR-015 automatico
=========================================================

  | **Given** un User en ``BLOCKED`` con ultimo AuditEvent
  |   ``ACCOUNT_LOCKED`` (BR-015 automatico, e2).
  | **When** el admin desbloquea con
  |   ``reason='falso positivo, password olvidado'``.
  | **Then** la respuesta es ``200 OK``,
  |   ``User.state = ACTIVE``,
  |   AuditEvent ``USER_UNBLOCKED`` con
  |   ``original_block_event_id = e2``,
  |   ``original_block_type = 'ACCOUNT_LOCKED'``.

CA-03: Idempotencia con User ya ACTIVE
=======================================

  | **Given** un User ``state = ACTIVE``.
  | **When** se invoca el desbloqueo.
  | **Then** ``200 OK`` con ``already_unblocked = true``,
  |   sin nuevo AuditEvent.

CA-04: Permission denied
=========================

  | **Given** un User SIN ``unblock_users``.
  | **When** invoca el endpoint.
  | **Then** ``403 PERMISSION_DENIED``,
  |   AuditEvent ``ACCESS_DENIED``.

CA-05: User ELIMINATED no se desbloquea
========================================

  | **Given** ``User.state = ELIMINATED``.
  | **When** admin intenta desbloquear.
  | **Then** ``409 USER_ELIMINATED``, state preservado.

CA-06: User INACTIVE no se desbloquea con UC_USR_06
======================================================

  | **Given** ``User.state = INACTIVE``.
  | **When** admin intenta desbloquear.
  | **Then** ``409 INVALID_STATE_TRANSITION`` con guidance
  |   a UC_USR_03.

CA-07: Estado inconsistente sin block AuditEvent
==================================================

  | **Given** ``User.state = BLOCKED`` pero NO existe
  |   AuditEvent ``USER_BLOCKED`` ni ``ACCOUNT_LOCKED``
  |   previo.
  | **When** admin desbloquea.
  | **Then** ``200 OK``, ``state = ACTIVE``,
  |   AuditEvent ``USER_UNBLOCKED`` con
  |   ``original_block_event_id = null``,
  |   y warning ``USER_STATE_INCONSISTENCY`` emitido.

CA-08: Auto-desbloqueo prohibido
=================================

  | **Given** admin con ``unblock_users``.
  | **When** intenta desbloquearse.
  | **Then** ``409 SELF_UNBLOCK_FORBIDDEN``.

CA-09: Reason invalida
=======================

  | **Given** payload sin ``reason``.
  | **When** invoca el endpoint.
  | **Then** ``400 REASON_REQUIRED``.

CA-10: Atomicidad ante fallo
=============================

  | **Given** falla SQL durante el UPDATE.
  | **Then** rollback completo, ``state`` permanece
  |   ``BLOCKED``, ``500 UNBLOCK_FAILED``.

CA-11: Sessions cerradas permanecen cerradas
=============================================

  | **Given** User BLOCKED con 3 Sessions CLOSED previas.
  | **When** se desbloquea.
  | **Then** las 3 Sessions siguen ``CLOSED``;
  |   el User debe re-loguear (UC_AUTH_01) para nueva
  |   sesion.

CA-12: Login post-unblock funciona
====================================

  | **Given** User recien desbloqueado.
  | **When** invoca UC_AUTH_01 con credenciales validas.
  | **Then** login exitoso, nueva Session creada.
