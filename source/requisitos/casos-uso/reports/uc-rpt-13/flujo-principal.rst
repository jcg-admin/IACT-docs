.. _uc-rpt-13-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — GET con filtros + period.
PASO 2 — JWT.
PASO 3 — RBAC view_reports.
PASO 4 — Resolver segmento.
PASO 5 — Validar.
PASO 6 — Cache lookup.
PASO 7 — ``ReportingService.callproc(
'sp_rpt_llamadas_abandonadas',
[period, segments])`` sobre BD_IVR. El SP
retorna filas pre-agregadas por queue_id
con counts de abandono y trend buckets.
PASO 8 — Construir summary mapeando las
filas del SP a la estructura
AbandonReportOutput (sin re-calculo).
PASO 9 — Cache write.
PASO 10 — 200.

CNST-007: SOLO BD_IVR (read-only). El
backend NO re-agrega ni recalcula KPIs;
la agregacion la realiza el SP.

3.1 Resumen
===========

Estructuralmente analogo a otros reportes
IVR del modulo; la dimension principal es
``queue_id`` y el SP especifico es
``sp_rpt_llamadas_abandonadas``.
