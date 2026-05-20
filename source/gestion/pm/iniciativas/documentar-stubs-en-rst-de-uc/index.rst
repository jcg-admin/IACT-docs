.. meta::
   :artefacto: INICIATIVA-DOCUMENTAR-STUBS-EN-RST-DE-UC
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:05:00
   :ultimo_cambio: 2026-05-19T22:05:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-documentar-stubs-en-rst-de-uc:

==============================================================
Iniciativa: Documentar STUBs en RST de UC
==============================================================

P3 plan #15. Anota en el RST de cada UC implementado como
STUB explicito que el comportamiento es intencional, no
omision.

Inventario de STUBs verificado por grep
==========================================

.. code-block:: bash

   grep -rln "STUB" /home/user/IACT-api/callcentersite/apps/

Output: 1 archivo — ``apps/reports/realtime_view.py``.
**Unico STUB en el sistema:**

* **UC_RPT_02** = uc-033-ver-metricas-tiempo-real.
  Razon: CNST-004 prohibe Channels/Celery/Redis ->
  real-time SSE inviable.

Cambios aplicados
==================

* ``source/requisitos/requisitos-funcionales/reports/uc-033-ver-metricas-tiempo-real/index.rst``:
  anadida admonicion ``.. warning::`` al inicio con
  explicacion del STUB, referencia a CNST-004, e
  iniciativa hermana
  ``revisar-cnst-004-realtime-metrics`` (plan #16) que
  gateria cualquier implementacion futura.

sphinx-build dummy limpio (0 warnings).

Iniciativa hermana
====================

* ``revisar-cnst-004-realtime-metrics`` (plan #16, P4):
  requiere decision sponsor antes de implementar
  real-time completo. Si se revoca CNST-004, abre
  iniciativa de implementacion. Si se confirma,
  el STUB queda permanente y este RST se actualiza con
  esa decision.
