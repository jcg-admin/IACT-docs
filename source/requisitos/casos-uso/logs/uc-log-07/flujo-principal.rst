.. _uc-log-07-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — GET. PASO 2 — JWT + RBAC.
PASO 3 — Validar.
PASO 4 — Cache lookup (TTL 30s).
PASO 5 — Query TSDB con time range +
agregacion.
PASO 6 — Compute P50/P95/P99 desde
histograms.
PASO 7 — Cache write.
PASO 8 — 200.
