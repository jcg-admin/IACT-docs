.. _uc-log-05-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

User con ``view_infrastructure_logs``,
InfraLogStore.

::

   GET /api/logs/infra/?period=last_1h
       &filter[host]=...

Response: list de infra log entries.
