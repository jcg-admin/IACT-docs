.. _uc-log-04-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

User con ``export_logs``, ExportWorker,
Storage, MailboxService.

::

   POST /api/logs/export/
   body: { filters, period,
           format: jsonl|csv,
           include_archive }

Response: 202 + job_id.
