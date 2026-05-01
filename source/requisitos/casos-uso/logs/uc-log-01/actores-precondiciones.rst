.. _uc-log-01-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

- **User con funcion** ``view_system_logs``
- **LogStore** (Loki / Elasticsearch /
  CloudWatch / similar)

::

   GET /api/logs/system/?period=last_1h
       &filter[level]=warn|error
       &filter[service]=...

Response: list de log entries con
timestamp + level + message + context.
