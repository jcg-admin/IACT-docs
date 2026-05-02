.. _uc-log-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 LogEntry
============

::

   LogEntry:
     timestamp, level, service,
     message, context: JSON,
     trace_id, request_id

7.2 Sanitization
================

Pipeline al ingresar a LogStore: PIIScanner
sobre context y message.

7.3 Retention
=============

- 30 dias online.
- > 30 dias → archive (UC_LOG_04 export).
