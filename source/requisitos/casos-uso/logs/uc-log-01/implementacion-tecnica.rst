.. _uc-log-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: SystemLogsEndpoint,
AuthorizationGuard, LogStoreClient,
PIIScanner.

::

   contract SystemLogsService:
     list(filters, period, page,
          invoker, ctx)
       returns: LogList
     tail(filters, invoker, ctx)
       returns: SSEStream

LogStore-agnostic: Loki, ELK, CloudWatch,
Splunk.
