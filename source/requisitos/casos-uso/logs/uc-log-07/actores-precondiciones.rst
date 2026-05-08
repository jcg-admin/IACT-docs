.. _uc-log-07-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

User con ``view_technical_metrics``,
MetricsTSDB (Prometheus / similar).

::

   GET /api/metrics/?period=last_1h
       &filter[service]=...
       &group_by=service|endpoint
