.. meta::
   :artefacto: ALCANCE-IMPLEMENTAR-UC-RPT-05-06-PROGRAMACION-REPORTES
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/implementar-uc-rpt-05-06-programacion-reportes
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-implementar-uc-rpt-05-06-programacion-reportes:

==============================================================
Alcance: Implementar UC_RPT_05/06 (resultado: discovery)
==============================================================

Por que existe (intent original)
==================================

La auditoria
``auditar-cobertura-uc-implementacion`` identifico
``UC_RPT_05`` y ``UC_RPT_06`` como "los unicos 2 UCs
in-scope estrictamente sin implementacion en ningun repo".
El sponsor pidio atacar el caso mas dificil. Esta
iniciativa abrio para producir codigo + UI + tests para
ambos UCs bajo restriccion CNST-004 (NO Celery — implica
usar APScheduler ya declarado en requirements/base.txt).

Por que se reformulo
=====================

Al ejecutar la Fase 1 DISCOVER (analisis del scaffolding
existente), aparecio ``apps/reports/schedule_views.py``
(202 lineas) con UC_RPT_07 = "Programar Reporte" y
UC_RPT_08 = "Ver Reportes Programados". El mapping linear
docs <-> codigo que la auditoria asumio resulto erroneo:
el codigo salta de ``UC_RPT_04`` directamente a
``UC_RPT_07``.

Verificacion textual:

.. code-block:: bash

   grep -oE "UC_RPT_[0-9]+ — [^.\\n']+" apps/reports/*.py \\
     | sort -u

Output incluye ``UC_RPT_07 — Programar Reporte`` y
``UC_RPT_08 — Ver Reportes Programados``, sin
``UC_RPT_05`` ni ``UC_RPT_06``.

**Conclusion observable:** los UCs documentados
``uc-036-programar-reporte`` y
``uc-037-ver-reportes-programados`` **estan implementados**
bajo marker distinto al asumido. No hay gap real.

Criterio de completitud verificable
=====================================

* Mapping correcto docs <-> codigo para el dominio
  ``reports`` documentado en el deep-analisis de esta
  iniciativa.
* Actualizacion del deep-analysis previo
  (``auditar-cobertura-uc-implementacion/deep-analisis-*``)
  con la correccion del bug de mapping lineal.
* Identificacion del unico gap real del dominio reports:
  ``UC_RPT_02`` (uc-033-ver-metricas-tiempo-real) como
  STUB explicito por CNST-004.
* Cierre de la iniciativa con estado COMPLETADA y la
  recomendacion clara: el gap original no existe, no
  implementar codigo.

In-scope
========

* Investigacion read-only en
  ``IACT-api/callcentersite/apps/reports/`` para mapear
  ``UC_RPT_NN`` a UC docs.
* Verificacion de que ``uc-036`` / ``uc-037`` tienen
  views, services, models y URLs.
* Verificacion de que ``UC_RPT_02`` es STUB por
  arquitectura.
* Correccion del deep-analysis previo con el mapping
  correcto y conclusiones actualizadas.

Out-of-scope
============

* Implementar codigo nuevo para UC_RPT_05/06: **el gap
  no existe**.
* Resolver UC_RPT_02 STUB: bloqueado por CNST-004
  (decision arquitectonica explicita: NO Channels, NO
  Celery, NO Redis). El STUB es intencional. Si el
  sponsor decide cambiar la decision, abre iniciativa
  dedicada
  ``revisar-cnst-004-realtime-metrics`` que cuestione la
  restriccion antes de implementar.
* Mapping linear para los otros dominios (auth/users/
  access/permissions/alerts/audit/logs/pipeline) — el
  deep-analysis previo asume linearidad ahi tambien
  pero no se verifico individualmente. Candidata a
  iniciativa
  ``verificar-mapping-docs-codigo-todos-los-dominios``.
* Tests, build, push de codigo nuevo — innecesarios al
  no haber codigo nuevo.
