.. _uc-log-02-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

- **User con funcion** ``view_etl_logs``
- **LogStore**

::

   GET /api/logs/etl/?period=last_1h
       &filter[pipeline_id]=...

Identica estructura que UC_LOG_01.
