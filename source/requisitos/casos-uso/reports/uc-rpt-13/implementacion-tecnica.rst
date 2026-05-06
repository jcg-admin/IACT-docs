.. _uc-rpt-13-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``AbandonoReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ReportingService`` —
  ``cursor.callproc('sp_rpt_llamadas_abandonadas',
  [period, segments])`` sobre BD_IVR
- ``MetricsCache``

11.2 Contrato
=============

::

   contract AbandonmentReportService:
     get(period, segmentos, invoker, ctx)
       returns: ReporteAbandono
       throws: SinPermiso, UserWithoutSegment,
               ValidationError, BDTimeout

11.3 Pseudocodigo
=================

::

   procedure get(period, invoker, ctx):
       require AuthorizationGuard.has(
                 invoker, 'view_reports')
       segmentos = SegmentResolver.resolve(
                     invoker.id)
       if not segmentos:
           raise UserWithoutSegment

       key = ('abandono', period,
              hash(segmentos))
       cached = MetricsCache.get(key)
       if cached: return cached

       try:
           rows = ReportingService.callproc(
             'sp_rpt_llamadas_abandonadas',
             [period, segmentos])
       except BDTimeout:
           raise

       # El SP entrega filas por queue_id ya
       # agregadas (offered, abandoned, asa,
       # service_level, trend) — no se
       # re-agrega ni filtra por segmento en
       # backend; el filtro va en el SP.
       reporte = AbandonReportOutput.from_rows(rows)
       MetricsCache.set(key, reporte, ttl=300)
       return reporte

11.4 Restricciones cross-cutting
================================

- Read-only sobre BD_IVR (CNST-007).
- KPIs pre-calculados en el SP — sin
  re-agregacion en backend.
- Filtro por segmento (CNST-008) aplicado
  por el SP al recibir la lista.

