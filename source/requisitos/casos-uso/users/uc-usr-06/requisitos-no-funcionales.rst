.. _uc-usr-06-parte-09:

==========================================
Parte 9 — Requisitos no funcionales
==========================================

9.1 Performance
================

P50
  ≤ 150 ms (operacion mas simple que UC_USR_05; sin
  cierre masivo de Sessions ni blacklisting).

P99
  ≤ 500 ms incluyendo lookup del block_event y emision
  del AuditEvent.

Throughput
  10 RPS sostenidos.

9.2 Disponibilidad
===================

UC_USR_06 NO es operacion critica para disponibilidad
del sistema. Si esta caido, los Users bloqueados
permanecen bloqueados hasta restablecimiento.

9.3 Concurrencia
=================

Locking
  Row-lock en ``User`` durante la transaccion.

Idempotencia
  Si dos admins desbloquean simultaneamente, el segundo
  recibe ``200 OK`` con ``already_unblocked = true``.

9.4 Auditabilidad
==================

Inmutabilidad
  AuditEvent ``USER_UNBLOCKED`` es inmutable (CNST-025).

Sin PII
  payload sin email/full_name/identificadores personales
  (CNST-026).

Trazabilidad par bloqueo↔desbloqueo
  ``original_block_event_id`` permite reconstruir el
  ciclo bloqueo→desbloqueo en consultas de auditoria.

9.5 Seguridad
==============

Authn/Authz
  JWT vigente + funcion ``unblock_users``.

Audit failure
  Si el AuditEvent NO se persiste, rollback completo —
  sin AuditEvent no hay desbloqueo.

9.6 Localizacion
=================

Mismo enfoque que UC_USR_05: ``reason`` se preserva tal
cual; codigos de error son i18n estables.
