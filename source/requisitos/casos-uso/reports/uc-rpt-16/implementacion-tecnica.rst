.. _uc-rpt-16-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``MenuIVRReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract MenuIVRReportService:
     get(trimestre, vista, invoker, ctx)
       returns: ReporteMenuIVR

   # vista: 'redirigidos' | 'menu_centro' | 'errores'

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, vista, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('menu_ivr', trimestre, vista, segmentos)
       if cached: return cached
       if vista == 'redirigidos':
           data = IvrNavigationReportService.get(trimestre)
       elif vista == 'menu_centro':
           data = IvrNavigationReportService.menu_centro(trimestre)
       else:
           data = IvrNavigationReportService.cmenu_error(trimestre)
       reporte = filtrar_por_segmentos(data, segmentos)
       MetricsCache.set('menu_ivr', trimestre, vista, segmentos,
                        reporte, ttl=300)
       return reporte

