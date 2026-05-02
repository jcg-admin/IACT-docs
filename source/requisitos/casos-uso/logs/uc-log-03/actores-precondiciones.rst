.. _uc-log-03-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

User con ``search_logs``, LogStore (FTS).

::

   POST /api/logs/search/
   body: { query, period, filters,
           page_size, cursor }

Range obligatorio ≤ 7 dias.
