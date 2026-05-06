.. _uc-rpt-17-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``ClientesReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ReportingService`` —
  ``cursor.callproc('sp_rpt_clientes',
  [period, segments])`` sobre BD_IVR
  (lee solo ``telefono_hashed``)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract CallerReportService:
     get(period, segmentos, invoker, ctx)
       returns: ReporteClientes
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

       key = ('clientes', period,
              hash(segmentos))
       cached = MetricsCache.get(key)
       if cached: return cached

       try:
           rows = ReportingService.callproc(
             'sp_rpt_clientes',
             [period, segmentos])
       except BDTimeout:
           raise

       # El SP entrega filas pre-agregadas
       # con telefono_hashed (NO PII raw),
       # distinct counts, recurrence, new
       # vs returning. Backend solo parsea.
       reporte = ClientReportOutput.from_rows(rows)
       MetricsCache.set(key, reporte, ttl=300)
       return reporte

11.4 Restricciones cross-cutting
================================

- Read-only sobre BD_IVR (CNST-007).
- Backend NUNCA ve telefono raw —
  el hash lo aplica el ETL upstream
  (``sp_etl_base_clientes``) antes de
  poblar ``base_ivr_clientes`` (CNST-026).
- Filtro por segmento (CNST-008) aplicado
  por el SP al recibir la lista.
- Top N expone solo prefix de hash
  (no full hash, no reidentificable).

