.. _uc-rpt-15-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``TransferenciasReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract TransferReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteTransferencias

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('transferencias', trimestre, segmentos)
       if cached: return cached
       centros = TransferReportService.get(trimestre)
       centros_seg = TransferReportService.by_center(trimestre)
       reporte = construir_reporte_transferencias(
           centros, centros_seg, segmentos
       )
       MetricsCache.set('transferencias', trimestre, segmentos,
                        reporte, ttl=300)
       return reporte

