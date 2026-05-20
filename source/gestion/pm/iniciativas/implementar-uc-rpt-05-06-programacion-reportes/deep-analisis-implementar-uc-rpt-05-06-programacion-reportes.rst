.. meta::
   :artefacto: DEEP-ANALISIS-IMPLEMENTAR-UC-RPT-05-06-PROGRAMACION-REPORTES
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/implementar-uc-rpt-05-06-programacion-reportes
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:25:00
   :ultimo_cambio: 2026-05-19T20:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-implementar-uc-rpt-05-06-programacion-reportes:

==============================================================
Deep-Analisis: UC_RPT_05/06 — gap real o gap de numeracion?
==============================================================

Pregunta de partida
====================

La iniciativa
``auditar-cobertura-uc-implementacion`` reporto:

   "UC_RPT_05 (uc-036-programar-reporte) y UC_RPT_06
   (uc-037-ver-reportes-programados): sin marker en api ni
   ui. Posible: feature de programacion de reportes esta
   solo en docs, no implementada."

Bajo CNST-004 (NO Celery, NO Channels, NO Redis),
implementar programacion de reportes es no-trivial:
requiere usar ``APScheduler`` (declarado en
``requirements/base.txt``) con persistencia en BD. Esta
iniciativa abrio para producir esa implementacion.

Investigacion (Fase 1 DISCOVER)
=================================

Paso 1 — Buscar scaffolding existente en apps/reports/
-------------------------------------------------------

.. code-block:: bash

   ls apps/reports/ | grep -iE "schedule|programar"

Output observado:

::

   schedule_service.py
   schedule_views.py

Paso 2 — Inspeccionar schedule_views.py
-----------------------------------------

Primeras lineas del archivo:

.. code-block:: python

   """
   apps/reports/schedule_views.py

   UC_RPT_07 — Programar Reporte. POST/PATCH/DELETE /api/reports/schedules/
   UC_RPT_08 — Ver Reportes Programados. GET /api/reports/schedules/
   """

**Observacion clave:** las views existen y estan
implementadas. Pero los markers son ``UC_RPT_07`` y
``UC_RPT_08``, no ``UC_RPT_05`` ni ``UC_RPT_06``.

Paso 3 — Verificar que UC_RPT_05/06 no existan
------------------------------------------------

.. code-block:: bash

   grep -E "UC_RPT_(0[5-9]|1[0-7])" apps/reports/*.py \\
     | grep -oE "UC_RPT_[0-9]+ — [^.\\n']+" | sort -u

Output (extracto):

::

   UC_RPT_07 — Delete scheduled report
   UC_RPT_07 — Eliminar schedule (baja logica BR-009)
   UC_RPT_07 — Modificar / pausar / reanudar schedule
   UC_RPT_07 — Programar Reporte
   UC_RPT_07 — Programar reporte periodico
   UC_RPT_07 — Schedule a report
   UC_RPT_07 — Update scheduled report
   UC_RPT_08 — Detalle de reporte programado
   UC_RPT_08 — List scheduled reports
   UC_RPT_08 — Listar reportes programados
   UC_RPT_08 — Scheduled report detail
   UC_RPT_08 — Ver Reportes Programados
   UC_RPT_09 — Actualizar filtro guardado
   ...

**No hay una sola entrada con ``UC_RPT_05`` o
``UC_RPT_06``.** El codigo salta de 04 directamente a 07.

Mapping correcto observado del dominio reports
================================================

.. list-table::
   :header-rows: 1
   :widths: 14 50 36

   * - Marker codigo
     - Descripcion en codigo
     - UC docs equivalente
   * - UC_RPT_01
     - Dashboard de KPIs IVR
     - uc-032-ver-dashboard
   * - UC_RPT_02
     - Real-time metrics (STUB por CNST-004)
     - uc-033-ver-metricas-tiempo-real
   * - UC_RPT_03
     - Ver Reportes Historicos
     - uc-034-ver-reportes-historicos
   * - UC_RPT_04
     - Exportar Reporte
     - uc-035-exportar-reporte
   * - **UC_RPT_05**
     - **(no existe en codigo)**
     - **gap de numeracion**
   * - **UC_RPT_06**
     - **(no existe en codigo)**
     - **gap de numeracion**
   * - UC_RPT_07
     - Programar Reporte (+ Delete/Update/Pause)
     - **uc-036-programar-reporte**
   * - UC_RPT_08
     - Ver Reportes Programados
     - **uc-037-ver-reportes-programados**
   * - UC_RPT_09
     - SavedFilter (Configurar Filtros)
     - uc-038-gestionar-filtros-guardados
   * - UC_RPT_10
     - Vista guardada
     - uc-039-guardar-vista
   * - UC_RPT_11..17
     - (sin verificar individualmente — pendiente)
     - uc-040..047

Por que el deep-analysis previo se equivoco
=============================================

H-A-PRE-1 — Asuncion implicita de linearidad
----------------------------------------------

La auditoria
``auditar-cobertura-uc-implementacion`` asumio que:

::

   uc-032 (1er UC del dominio reports en docs) <-> UC_RPT_01
   uc-033 (2do)                                <-> UC_RPT_02
   ...
   uc-036 (5to)                                <-> UC_RPT_05  ← BUG
   uc-037 (6to)                                <-> UC_RPT_06  ← BUG
   uc-038 (7mo)                                <-> UC_RPT_07  ← BUG

Realidad observable:

::

   uc-032 <-> UC_RPT_01
   uc-033 <-> UC_RPT_02
   uc-034 <-> UC_RPT_03
   uc-035 <-> UC_RPT_04
   uc-036 <-> UC_RPT_07   (salto sobre 05 y 06)
   uc-037 <-> UC_RPT_08
   uc-038 <-> UC_RPT_09

Causa de la asuncion: ningun documento normativo declara
explicitamente el mapping; la auditoria uso grep ciego de
markers y conto distintos, sin verificar a que UC docs
corresponde cada marker.

H-A-PRE-2 — Heuristica de marker no detecta gaps de numeracion
----------------------------------------------------------------

Grep de ``UC_RPT_05`` en codigo retorna 0 hits. La
auditoria interpreto 0 hits como "UC sin implementacion".
La interpretacion correcta es "marker no existe en codigo
— ambiguo: puede ser gap real o gap de numeracion sin
correspondencia con UC docs".

Para resolver la ambiguedad: leer la descripcion textual
del marker existente mas cercano y compararla con el
nombre del UC docs. Si la descripcion del marker
``UC_RPT_07 = "Programar Reporte"`` coincide con el UC
``uc-036-programar-reporte``, el gap es de numeracion,
no de implementacion.

Gap real en dominio reports
=============================

Tras corregir el mapping, el unico UC con status
"implementacion incompleta" en reports es:

* ``UC_RPT_02 / uc-033-ver-metricas-tiempo-real`` —
  **STUB explicito** por CNST-004.

Evidencia: ``apps/reports/realtime_view.py`` declara

.. code-block:: python

   """
   UC_RPT_02 — Ver Metricas en Tiempo Real (STUB).
   STUB: UC_RPT_02 requiere infraestructura SSE/ASGI con pub/sub
     Hallazgo H-F3-PRE-004: UC_RPT_02 requiere ASGI —
     se implementa como stub.
   """

El STUB retorna snapshot estatico en lugar de stream
real-time. Es decision arquitectonica explicita, no
omision: CNST-004 prohibe Channels (ASGI) y CNST_TECNICAS
prohibe Redis (pub/sub). Sin esos componentes, real-time
SSE no es viable. El proyecto opta por snapshot estatico
como compromiso aceptable.

Si el sponsor decide revisitar CNST-004 (por ejemplo
permitir Channels), abrir iniciativa
``revisar-cnst-004-realtime-metrics`` ANTES de
implementar codigo. La iniciativa de implementacion
quedaria gateada por la decision normativa.

Recomendaciones derivadas
==========================

R-1 — Actualizar el deep-analysis previo con la correccion
------------------------------------------------------------

``auditar-cobertura-uc-implementacion/deep-analisis-cobertura-uc-implementacion``
afirma "UC_RPT_05 y UC_RPT_06 sin marker en api ni ui...
Posible: feature de programacion de reportes esta solo
en docs, no implementada". Esa afirmacion es **incorrecta**.
Bajar a "gap de numeracion, los UCs docs equivalentes
estan implementados bajo UC_RPT_07/08".

R-2 — Verificar mapping para los otros 11 dominios
----------------------------------------------------

El bug puede repetirse en cualquier dominio donde la
numeracion del codigo no sea lineal con docs.
Candidatos a verificar: access (7 markers vs 2 docs —
ya identificado como deuda inversa pero el mapping
exacto sin verificar); users (7 ui markers vs 4 docs);
logs (8 markers vs 7 docs); pipeline (5 markers vs 4).

Iniciativa candidata:
``verificar-mapping-docs-codigo-todos-los-dominios``.

R-3 — Documentar gaps de numeracion como deuda documental
-----------------------------------------------------------

Idealmente la convencion deberia ser: si un marker se
retira, mantener el numero o documentar el gap. La
ausencia de UC_RPT_05/06 sin explicacion es ruido. Una
nota en ``apps/reports/README.md`` (o equivalente) podria
declarar "UC_RPT_05/06 reservados, no usados".

R-4 — UC_RPT_02 STUB: documentarlo en el RST del UC
-----------------------------------------------------

El RST de uc-033 puede no mencionar que la
implementacion es STUB. Sin esa nota, un lector cree que
hay endpoint real-time. Iniciativa
``documentar-stubs-en-rst-de-uc`` cubriria UC_RPT_02 y
cualquier otro stub similar.

Conclusion
===========

* El gap UC_RPT_05/06 **no existe**.
* Los UCs documentados uc-036/uc-037 **estan
  implementados** bajo UC_RPT_07/UC_RPT_08.
* El unico gap real del dominio reports es **UC_RPT_02
  como STUB** por restriccion arquitectonica explicita
  (CNST-004).
* El deep-analysis previo tiene un bug de mapping; se
  corregira en R-1.
* La iniciativa cierra COMPLETADA sin producir codigo.
  Su valor es la **calibracion correcta** de un claim
  previamente SPECULATIVE.
