.. _uc-usr-07-parte-09:

==========================================
Parte 9 — Requisitos no funcionales
==========================================

9.1 Performance
================

P50
  ≤ 100 ms (operacion mas simple de los UCs de users —
  UPDATE de 1-2 campos + 1 AuditEvent).

P99
  ≤ 300 ms incluyendo validacion de unicidad de email.

Throughput
  100 RPS sostenidos (operacion frecuente, self-service).

9.2 Disponibilidad
===================

UC_USR_07 NO es operacion critica. Si el endpoint esta
caido, los Users no pueden editar perfil pero todas las
demas operaciones funcionan.

9.3 Concurrencia
=================

Locking
  Row-lock en ``User`` durante la transaccion.

Race condition email unico
  Resuelta por la atomicidad: la query de unicidad y el
  UPDATE estan en la misma transaccion con row-lock.

9.4 Auditabilidad
==================

Inmutabilidad
  AuditEvent ``PROFILE_UPDATED`` es inmutable (CNST-025).

Sin PII
  ``payload`` contiene SOLO ``fields_changed`` (lista de
  nombres), NO valores. CNST-026.

9.5 Seguridad
==============

Authn/Authz
  JWT + funcion ``edit_own_profile``.

Defensa contra escalation
  Whitelist de campos editables (``EDITABLE_FIELDS_SELF
  = {full_name, email}``); cualquier otro campo en
  payload retorna E6 ``FORBIDDEN_FIELD``.

Defensa contra impersonation
  ``target_user_id`` se infiere del JWT, NO se pasa
  como parametro de URL. Imposible editar a otro User.

9.6 Localizacion
=================

``full_name`` y ``email`` se preservan tal cual; el
sistema NO normaliza ni traduce. Los mensajes de error
usan codigos i18n estables.
