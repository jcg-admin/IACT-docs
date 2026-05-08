.. _uc-usr-07-parte-04:

==========================================
Parte 4 — Flujos alternos
==========================================

A1 — Payload sin diff respecto al estado actual
================================================

**Trigger:** paso 5 detecta que todos los campos enviados
ya tienen el valor solicitado (no hay cambio real).

**Flujo:**

1. Sistema NO ejecuta UPDATE (ya esta como se solicita).
2. NO emite AuditEvent (no hay cambio que auditar).
3. Responde ``200 OK`` con
   ``{user_id, full_name, email, updated_at,
   no_changes: true}``.

**Razon:** auditoria limpia — no inflar log con eventos
que no representan cambio.

A2 — Cambio parcial (solo full_name)
======================================

**Trigger:** payload contiene unicamente ``full_name``.

**Flujo:**

1. Validacion de email se omite (no fue enviado).
2. UPDATE solo escribe ``full_name``.
3. AuditEvent ``PROFILE_UPDATED`` con
   ``fields_changed: ['full_name']``.

**Razon:** PATCH semantico — solo se actualiza lo
enviado; campos omitidos preservan su valor.

A3 — Cambio parcial (solo email)
==================================

**Trigger:** payload contiene unicamente ``email``.

**Flujo:**

1. Validacion email completa (formato + unicidad).
2. UPDATE solo escribe ``email``.
3. AuditEvent ``PROFILE_UPDATED`` con
   ``fields_changed: ['email']``.
