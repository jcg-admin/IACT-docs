.. _uc-rpt-17-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``ClientesReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract CallerReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteClientes

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker,
                   'view_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('clientes', trimestre, segmentos)
       if cached: return cached
       data = CallerReportService.get(trimestre)
       reporte = filtrar_por_segmentos(data, segmentos)
       MetricsCache.set('clientes', trimestre, segmentos,
                        reporte, ttl=300)
       return reporte

