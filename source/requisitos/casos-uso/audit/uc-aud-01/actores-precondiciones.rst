.. _uc-aud-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

- **User con funcion** ``view_audit_log``
- **AuditRepo** (read replica)

Auth + RBAC.

::

   GET /api/audit/?period=last_7d
       &filter[module]=...

Response: timeline + cursor + summary
similar a UC_PERM_10.
