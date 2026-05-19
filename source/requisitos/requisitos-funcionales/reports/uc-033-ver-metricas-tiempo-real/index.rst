.. _uc_033_ver_metricas_tiempo_real:

===================================
FR-033: Ver Métricas en Tiempo Real
===================================

.. warning::

   **UC_RPT_02 implementado como STUB** por restriccion
   arquitectonica explicita CNST-004 (NO Channels,
   NO Celery, NO Redis).

   El endpoint actual
   (``apps/reports/realtime_view.py``) retorna un
   snapshot estatico o 503 segun configuracion. La
   implementacion completa requiere SSE/ASGI con pub/sub
   (topics: ``call_state_changes``,
   ``agent_state_changes``, ``queue_state_snapshots``),
   inviable bajo el stack actual Django WSGI sincronico.

   La decision de revisitar CNST-004 (que habilitaria
   real-time completo) esta diferida a la iniciativa
   ``revisar-cnst-004-realtime-metrics`` (plan #16,
   P4 — requiere decision del sponsor antes de
   implementar codigo).

   Hasta entonces, el STUB es comportamiento
   **intencional**, no omision. Cualquier consumer del
   endpoint debe usar polling (UC_RPT_01 dashboard).

Requisitos Funcionales derivados de UC_RPT_02.

.. toctree::
   :maxdepth: 1

   fr-033-01-emitir-kpis-tiempo-real
