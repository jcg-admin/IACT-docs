.. _uc-usr-05-parte-06:

==========================================
Parte 6 — Criterios de aceptacion
==========================================

Cada criterio se expresa en forma Given/When/Then y
referencia el flujo del que proviene (3.x principal,
A.x alterno, E.x excepcion).

CA-01: Bloqueo nominal de User ACTIVE
======================================

  | **Given** un admin con funcion ``block_users``
  |   activa, y un User objetivo en estado ``ACTIVE``
  |   con 2 Sessions ACTIVE y 3 refresh tokens vivos.
  | **When** el admin invoca ``POST /users/{id}/block``
  |   con ``reason='investigacion ABC-123'``.
  | **Then** la respuesta es ``200 OK``,
  |   ``User.state = BLOCKED``,
  |   las 2 Sessions pasan a ``CLOSED``
  |   con ``close_reason = 'USER_BLOCKED'``,
  |   los 3 tokens estan en ``BlacklistedToken``,
  |   y existe un ``AuditEvent USER_BLOCKED`` con
  |   ``sessions_closed_count = 2``,
  |   ``tokens_blacklisted_count = 3``,
  |   ``reason = 'investigacion ABC-123'``.

CA-02: Idempotencia logica con User ya BLOCKED
===============================================

  | **Given** un User en estado ``BLOCKED``.
  | **When** un admin invoca el bloqueo nuevamente.
  | **Then** la respuesta es ``200 OK`` con
  |   ``already_blocked = true``,
  |   NO se crea nuevo AuditEvent ``USER_BLOCKED``,
  |   y NO se modifica nada.

CA-03: Bloqueo desde estado INACTIVE
=====================================

  | **Given** un User en estado ``INACTIVE`` sin Sessions
  |   ACTIVE ni tokens vivos.
  | **When** el admin invoca el bloqueo con razon valida.
  | **Then** la respuesta es ``200 OK``,
  |   ``User.state = BLOCKED``,
  |   AuditEvent ``USER_BLOCKED`` con
  |   ``sessions_closed_count = 0``,
  |   ``tokens_blacklisted_count = 0``,
  |   ``from_state = 'INACTIVE'``.

CA-04: Permission denied
=========================

  | **Given** un User autenticado SIN funcion
  |   ``block_users`` activa.
  | **When** invoca el endpoint de bloqueo.
  | **Then** la respuesta es ``403 PERMISSION_DENIED``,
  |   y existe AuditEvent ``ACCESS_DENIED`` con
  |   ``attempted_action = 'block_users'``.

CA-05: User objetivo inexistente
=================================

  | **Given** un admin valido y un ``user_id`` que NO
  |   existe en BD.
  | **When** invoca el bloqueo.
  | **Then** la respuesta es ``404 USER_NOT_FOUND``
  |   y NO se emite AuditEvent.

CA-06: Auto-bloqueo prohibido
==============================

  | **Given** un admin con ``block_users`` activa.
  | **When** intenta bloquearse a si mismo.
  | **Then** la respuesta es ``409 SELF_BLOCK_FORBIDDEN``
  |   y NO se modifica nada.

CA-07: Bloqueo de User ELIMINATED prohibido
============================================

  | **Given** un User en estado ``ELIMINATED``.
  | **When** el admin intenta bloquear.
  | **Then** la respuesta es ``409 USER_ELIMINATED``,
  |   y el state se preserva.

CA-08: Reason invalida
=======================

  | **Given** payload sin ``reason`` o con ``reason``
  |   vacia / >500 chars.
  | **When** invoca el bloqueo.
  | **Then** la respuesta es ``400 REASON_REQUIRED``
  |   con constraint documentada.

CA-09: Atomicidad ante fallo
=============================

  | **Given** que ocurre fallo SQL durante el cierre de
  |   sesiones (paso 6).
  | **When** la transaccion intenta commit.
  | **Then** rollback completo,
  |   ``User.state`` permanece ``ACTIVE``,
  |   Sessions permanecen ``ACTIVE``,
  |   tokens NO se blacklistean,
  |   y el endpoint responde ``500 BLOCK_FAILED``.

CA-10: Override de razon sobre bloqueo automatico
==================================================

  | **Given** un User bloqueado automaticamente por
  |   BR-015 (ultimo AuditEvent ``ACCOUNT_LOCKED``).
  | **When** un admin invoca UC_USR_05 con razon
  |   administrativa.
  | **Then** ``state`` permanece ``BLOCKED``,
  |   se emite AuditEvent ``USER_BLOCK_REASON_OVERRIDE``
  |   con ambas razones (original automatica + nueva
  |   admin).
