.. _uc-log-02-parte-03:

==========================
Parte 3 — Flujo principal
==========================

Identico a UC_LOG_01 con scope etl
service implícito en query a LogStore.

PASO 1 — GET.
PASO 2 — JWT + RBAC.
PASO 3 — Validar.
PASO 4 — Query LogStore con filtro
``service like 'etl-%'`` + filtros.
PASO 5 — Sanitize.
PASO 6 — 200.
