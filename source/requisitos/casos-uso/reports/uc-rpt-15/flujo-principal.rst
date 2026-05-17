.. _uc-rpt-15-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — GET con filtros + period.
PASO 2 — JWT.
PASO 3 — RBAC view_reports.
PASO 4 — Resolver segmento.
PASO 5 — Validar.
PASO 6 — Cache lookup.

PASO 7a — ``ReportingService.callproc(
'sp_rpt_centros_transferencia',
[period, segments])`` sobre BD_IVR. El SP
retorna filas por centro de transferencia
ya pre-agregadas.

PASO 7b — ``ReportingService.callproc(
'sp_rpt_centros_xsegmento',
[period, segments])`` sobre BD_IVR. El SP
retorna las mismas filas re-agregadas
por segmento (contexto cruzado para el
heatmap).

PASO 8 — Combinar los dos result sets en
el ``TransferReportOutput`` (totals,
breakdowns por centro, breakdowns por
segmento). Backend NO recalcula KPIs.
PASO 9 — Construir heatmap centro x
segmento desde las filas de PASO 7b.
PASO 10 — Cache write.
PASO 11 — 200.

CNST-007: SOLO BD_IVR (read-only). Doble
SP — ambos del IVR legacy. La agregacion
la realiza cada SP en BD_IVR; el backend
solo combina los outputs.
