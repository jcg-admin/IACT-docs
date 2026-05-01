.. _uc-log-06-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: SystemStatusEndpoint,
AuthorizationGuard, ServiceHealthChecker
(parallel), Aggregator, MetricsCache.

::

   contract SystemStatusService:
     get(invoker, ctx)
       returns: SystemStatusReport

Pseudocodigo: query paralelo + aggregate.
Stack-agnostico.
