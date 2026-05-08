.. _uc-usr-07-parte-06:

==========================================
Parte 6 — Criterios de aceptacion
==========================================

CA-01: Edicion completa nominal
================================

  | **Given** un User ACTIVE autenticado con
  |   ``edit_own_profile`` activa.
  | **When** invoca ``PATCH /users/me`` con
  |   ``{full_name: 'Nuevo Nombre',
  |     email: 'nuevo@example.com'}``.
  | **Then** ``200 OK``,
  |   ``User.full_name = 'Nuevo Nombre'``,
  |   ``User.email = 'nuevo@example.com'``,
  |   AuditEvent ``PROFILE_UPDATED`` con
  |   ``fields_changed = ['full_name', 'email']``.

CA-02: Edicion parcial — solo full_name
=========================================

  | **Given** un User ACTIVE.
  | **When** envia ``{full_name: 'Nuevo'}``.
  | **Then** ``200 OK``, ``full_name`` modificado,
  |   ``email`` preservado, AuditEvent con
  |   ``fields_changed = ['full_name']``.

CA-03: Edicion parcial — solo email
=====================================

  | **Given** un User ACTIVE.
  | **When** envia ``{email: 'nuevo@x.com'}``
  |   con email valido y unico.
  | **Then** ``200 OK``, ``email`` modificado,
  |   AuditEvent con ``fields_changed = ['email']``.

CA-04: Idempotencia — payload identico al estado
==================================================

  | **Given** un User con ``full_name = 'X'``.
  | **When** envia ``{full_name: 'X'}``.
  | **Then** ``200 OK`` con ``no_changes: true``,
  |   sin AuditEvent emitido.

CA-05: Permission denied
=========================

  | **Given** un User SIN funcion ``edit_own_profile``.
  | **When** invoca el endpoint.
  | **Then** ``403 PERMISSION_DENIED``.

CA-06: Estado invalido (BLOCKED)
=================================

  | **Given** un User en BLOCKED (en escenario donde aun
  |   tiene token vivo no blacklisteado por timing).
  | **When** invoca el endpoint.
  | **Then** ``409 INVALID_STATE``.

CA-07: Email formato invalido
==============================

  | **Given** un User ACTIVE.
  | **When** envia ``{email: 'no-arroba'}``.
  | **Then** ``400 INVALID_EMAIL_FORMAT``.

CA-08: Email duplicado
=======================

  | **Given** existe otro User con email
  |   ``otra@example.com``.
  | **When** el actor envia
  |   ``{email: 'otra@example.com'}``.
  | **Then** ``409 EMAIL_ALREADY_TAKEN``.

CA-09: Payload vacio
=====================

  | **Given** un User ACTIVE.
  | **When** envia ``{}``.
  | **Then** ``400 EMPTY_PAYLOAD``.

CA-10: Campo prohibido (escalation attempt)
=============================================

  | **Given** un User ACTIVE.
  | **When** envia ``{primary_access_group_id: '...'}``.
  | **Then** ``400 FORBIDDEN_FIELD`` con guidance a
  |   UC_USR_03.

CA-11: Sesion permanece vigente tras edicion
==============================================

  | **Given** un User edita su perfil exitosamente.
  | **When** consulta ``GET /users/me`` con la misma
  |   sesion.
  | **Then** ``200 OK`` con los nuevos valores; sesion
  |   no requiere re-login.

CA-12: PII no en AuditEvent payload
=====================================

  | **Given** un User edita ``email``.
  | **When** se emite ``PROFILE_UPDATED``.
  | **Then** payload contiene ``fields_changed:
  |   ['email']`` pero NO contiene los valores antes/
  |   despues del email. CNST-026.

CA-13: Atomicidad ante fallo
=============================

  | **Given** falla SQL durante UPDATE.
  | **Then** rollback, perfil no modificado,
  |   ``500 PROFILE_UPDATE_FAILED``.
