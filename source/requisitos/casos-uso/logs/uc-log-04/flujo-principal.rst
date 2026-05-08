.. _uc-log-04-parte-03:

==========================
Parte 3 — Flujo principal
==========================

Identico a UC_RPT_04 / UC_AUD_03:

POST → JWT + RBAC → Validar → Crear job
→ Encolar → Audit QUEUED → 202.

Worker: re-check permiso → stream query
LogStore → sanitize → escribir → upload
storage → mailbox notify → audit
COMPLETED.
