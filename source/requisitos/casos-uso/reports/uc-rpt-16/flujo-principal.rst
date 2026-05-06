.. _uc-rpt-16-parte-03:

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
'sp_rpt_menu_redirigidos',
[period, segments])`` sobre BD_IVR. El SP
retorna filas pre-agregadas con counts
de redirecciones por opcion / nodo.

PASO 7b — ``ReportingService.callproc(
'sp_rpt_menu_centro', [period, segments])``
sobre BD_IVR. El SP retorna filas con
distribucion por centro de menu.

PASO 7c — ``ReportingService.callproc(
'sp_rpt_cMENU_ERROR', [period, segments])``
sobre BD_IVR. El SP retorna filas con
counts de errores / drops por nodo.

PASO 8 — Combinar los tres result sets en
``MenuReportOutput`` (3 sub-vistas:
redirigidos, por centro, errores).
Backend NO recalcula KPIs ni hace path
mining; cada SP entrega su sub-vista
ya pre-agregada.
PASO 9 — Cache write.
PASO 10 — 200.

CNST-007: SOLO BD_IVR (read-only). Triple
SP — los tres del IVR legacy. Las
sub-vistas son alternas, no flujos
paralelos: cada una corresponde a un
panel UI distinto del reporte de menu.
