.. _uc-log-01-parte-01:

==============================
Parte 1 — Informacion general
==============================

.. list-table::
 :widths: 30 70

 * - **ID**
   - UC_LOG_01
 * - **BReq**
   - BReq-005, BReq-006
 * - **Funcion RBAC**
   - ``view_system_logs``

1.1 Diferencia con UC_AUD/PERM
==============================

- AuditEvent: eventos de seguridad
  inmutables.
- System logs: eventos operacionales
  (info / warn / error). Mutables a
  nivel storage (compactacion, retention
  corta).

1.2 Restricciones
=================

CNST-009. CNST-026 sin PII en logs.

1.3 Out of scope
================

- Logs ETL especificos (UC_LOG_02).
- Search libre (UC_LOG_03).
- Export (UC_LOG_04).
- Logs infra (UC_LOG_05).
- Estado sistema (UC_LOG_06).
- Metricas tecnicas (UC_LOG_07).
