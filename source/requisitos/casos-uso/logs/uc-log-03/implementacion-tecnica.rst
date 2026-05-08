.. _uc-log-03-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componentes: LogSearchEndpoint,
AuthorizationGuard, ThrottlePolicy,
LogSearchEngine (FTS), Sanitizer.

::

   contract LogSearchService:
     search(query, period, filters,
            cursor, page_size,
            invoker, ctx)
       returns: LogSearchResults

Stack-agnostico.
