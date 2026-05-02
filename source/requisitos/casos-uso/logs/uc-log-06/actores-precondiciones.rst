.. _uc-log-06-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

User con ``view_system_status``.

::

   GET /api/system/status/

Response:

::

   {
     overall: green|yellow|red,
     services: [
       { name, status, latency_ms,
         last_check_at }, ...
     ],
     dependencies: [
       { name, status, latency_ms }, ...
     ],
     etl: { status, lag_max_seconds },
     alerts: { active_count, critical_count }
   }
