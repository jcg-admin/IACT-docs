.. _uc-rpt-17-parte-03:

==========================
Parte 3 — Flujo principal
==========================

PASO 1 — GET con period.
PASO 2 — JWT.
PASO 3 — RBAC view_reports.
PASO 4 — Resolver segmento.
PASO 5 — Validar.
PASO 6 — Cache lookup.

PASO 7 — ``ReportingService.callproc(
'sp_rpt_clientes', [period, segments])``
sobre BD_IVR. El SP retorna filas
pre-agregadas con:

- distinct count de ``telefono_hashed``
  por segmento / trimestre,
- distribucion de recurrencia
  (calls_per_client),
- new vs returning (calculado contra
  periodo prior dentro del SP),
- Top N por hash anonimizado.

CNST-007: SOLO BD_IVR (read-only). El
hash unidireccional de telefonos lo
realiza el ETL upstream que pobla
``base_ivr_clientes``; el backend NUNCA
ve el numero original ni rehashea.
Orden canonico: ETL anonymize →
``sp_rpt_clientes`` (lee hash) → backend.

PASO 8 — Construir response mapeando las
filas del SP a ``ClientReportOutput``.
Backend NO recalcula KPIs ni des-anonimiza.
PASO 9 — Cache write.
PASO 10 — 200.
