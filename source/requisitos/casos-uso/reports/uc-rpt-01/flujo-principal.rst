.. _uc-rpt-01-parte-03:

==========================
Parte 3 — Flujo principal
==========================

3.1 Pasos
=========

**PASO 1 — Recepcion**

``GET /api/dashboard/?period=today``.

**PASO 2 — Auth**

JWT (CNST-009). Falla → 401.

**PASO 3 — RBAC**

``view_reports``. Falla → 403 +
UNAUTHORIZED audit.

**PASO 4 — Resolver segmento del User**

::

   segments = SegmentResolver.for(user_id)

Si vacio → EX-02. CNST-008 enforce:
los segmentos limitan SCOPE de la query.

**PASO 5 — Validar periodo**

``period`` ∈ {today, yesterday, last_hour,
last_7d}. Default: today.

**PASO 6 — Cache lookup**

::

   key = dashboard:{user_id}:{period}
        :{segments_hash}

Si hit < 30s, retornar.

**PASO 7 — ReportingService.callproc(sp_rpt_centros_xsegmento)**

::

   cursor.callproc(
     'sp_rpt_centros_xsegmento',
     [period, segments]
   )

Stored procedure del IVR legacy que retorna
**filas pre-agregadas** desde
``BD_IVR.base_ivr_detalle``:

- counts (total, answered, abandoned)
- sums / averages (durations)
- trend buckets (por hora / minuto)
- top centros por segmento

CNST-007: SOLO Base Analitica IVR (read-only).
Sin tocar BD operativa. La agregacion la
realiza el SP en BD_IVR; el backend NO
re-agrega ni re-calcula KPIs.

**PASO 8 — Construir response**

JSON con kpis, trend, segments_applied,
cache=false. Mapping directo de las filas
del SP a la estructura DashboardOutput.

**PASO 9 — Cache write**

::

   MetricsCache.set(key, response,
                    ttl=30s)

**PASO 10 — Respuesta 200**

Sin audit por invocacion (P-51 — read no
critical).

3.2 Resumen
===========

.. list-table::
 :widths: 8 50 22 20
 :header-rows: 1

 * - Paso
   - Accion
   - Componente
   - CNST
 * - 1
   - GET /api/dashboard/
   - View
   - —
 * - 2
   - JWT
   - Middleware
   - 009
 * - 3
   - RBAC view_reports
   - Guard
   - —
 * - 4
   - Resolver segmento
   - SegmentResolver
   - 008
 * - 5
   - Validar periodo
   - Validator
   - —
 * - 6
   - Cache lookup
   - MetricsCache
   - —
 * - 7
   - callproc(sp_rpt_centros_xsegmento)
   - ReportingService
   - 007
 * - 8
   - Construir response
   - View
   - —
 * - 9
   - Cache write
   - MetricsCache
   - —
 * - 10
   - 200 OK
   - View
   - —
