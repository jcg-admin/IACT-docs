.. _uc-rpt-13-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``AbandonoReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract AbandonmentReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteAbandono

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('abandono', trimestre, segmentos)
       if cached: return cached
       reporte = AbandonmentReportService.get(trimestre)
       reporte_filtrado = filtrar_por_segmentos(reporte, segmentos)
       MetricsCache.set('abandono', trimestre, segmentos,
                        reporte_filtrado, ttl=300)
       return reporte_filtrado

