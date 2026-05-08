.. _uc-rpt-15-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``TransferenciasReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ReportingService`` —
  ``cursor.callproc('sp_rpt_centros_transferencia', ...)``
  + ``cursor.callproc('sp_rpt_centros_xsegmento', ...)``
  sobre BD_IVR (DOBLE SP)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract TransferReportService:
     get(period, segmentos, invoker, ctx)
       returns: ReporteTransferencias
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

       key = ('transferencias', period,
              hash(segmentos))
       cached = MetricsCache.get(key)
       if cached: return cached

       try:
           rows_centros = ReportingService.callproc(
             'sp_rpt_centros_transferencia',
             [period, segmentos])
           rows_segmentos = ReportingService.callproc(
             'sp_rpt_centros_xsegmento',
             [period, segmentos])
       except BDTimeout:
           raise

       # Cada SP entrega filas pre-agregadas
       # desde BD_IVR. Backend solo combina
       # los dos result sets en el output.
       reporte = TransferReportOutput.from_rows(
           centros=rows_centros,
           segmentos=rows_segmentos)
       MetricsCache.set(key, reporte, ttl=300)
       return reporte

11.4 Restricciones cross-cutting
================================

- Read-only sobre BD_IVR (CNST-007).
- Doble SP — ambos del IVR legacy.
  Backend NO recalcula ni re-agrega.
- Filtro por segmento (CNST-008) aplicado
  por cada SP al recibir la lista.

