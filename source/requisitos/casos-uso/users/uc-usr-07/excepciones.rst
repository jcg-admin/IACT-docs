.. _uc-usr-07-parte-05:

==========================================
Parte 5 — Excepciones
==========================================

E1 — Actor sin funcion ``edit_own_profile``
=============================================

**Trigger:** paso 2 detecta funcion ausente.

**Respuesta:** ``403 PERMISSION_DENIED``.

**Audit:** ``ACCESS_DENIED`` con
``attempted_action: 'edit_own_profile'``.

**Nota:** este caso es raro porque la funcion se asigna
default a todos los Users, pero un admin puede haberla
revocado explicitamente.

E2 — User en estado no-ACTIVE
==============================

**Trigger:** paso 4 detecta state distinto de ACTIVE
(BLOCKED/INACTIVE/ELIMINATED).

**Respuesta:** ``409 INVALID_STATE`` con
``{state: '<state actual>', message: 'profile editing
requires ACTIVE state'}``.

**Razon:** defensa adicional aunque la autenticacion
deberia haberlo filtrado (BLOCKED no autentica).

E3 — Email con formato invalido
=================================

**Trigger:** paso 6 detecta formato no compliant con RFC
5322 simple.

**Respuesta:** ``400 INVALID_EMAIL_FORMAT`` con
``{field: 'email', constraint: 'valid email format'}``.

E4 — Email no unico
=====================

**Trigger:** paso 6 detecta colision con email
existente de otro User.

**Respuesta:** ``409 EMAIL_ALREADY_TAKEN`` con
``{field: 'email', message: 'email already used by
another user'}``.

**Audit:** NO se emite AuditEvent (CNST-026 — error de
input antes del cambio efectivo).

E5 — Payload vacio
====================

**Trigger:** payload no contiene ``full_name`` ni
``email``.

**Respuesta:** ``400 EMPTY_PAYLOAD`` con
``{message: 'at least one field required'}``.

E6 — Campo invalido en payload
================================

**Trigger:** payload incluye campos NO permitidos
(``primary_access_group_id``, ``state``, ``segment_id``,
``username``, ``user_id``).

**Respuesta:** ``400 FORBIDDEN_FIELD`` con
``{forbidden_fields: [...], message: 'use UC_USR_03 for
admin modifications'}``.

**Razon:** previene escalation — un User no puede
auto-asignarse privilegios via este endpoint.

E7 — Falla de transaccion
==========================

**Trigger:** falla SQL durante UPDATE o emit.

**Respuesta:** ``500 PROFILE_UPDATE_FAILED`` con
``transaction_rolled_back: true``.

**Recovery:** rollback completo — perfil no se modifica,
AuditEvent no se persiste.
