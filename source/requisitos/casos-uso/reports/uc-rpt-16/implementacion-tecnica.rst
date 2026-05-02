.. _uc-rpt-16-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``MenuIVRReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ServicioReportes``
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
       require AuthorizationGuard.has(invoker, 'view_ivr_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('menu_ivr', trimestre, vista, segmentos)
       if cached: return cached
       if vista == 'redirigidos':
           data = ServicioReportes.menu_redirigidos(trimestre)
       elif vista == 'menu_centro':
           data = ServicioReportes.menu_centro(trimestre)
       else:
           data = ServicioReportes.cmenu_error(trimestre)
       reporte = filtrar_por_segmentos(data, segmentos)
       MetricsCache.set('menu_ivr', trimestre, vista, segmentos,
                        reporte, ttl=300)
       return reporte

11.4 Implementacion ServicioReportes
=====================================

::

   ServicioReportes.menu_redirigidos(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_menu_redirigidos', [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]

   ServicioReportes.menu_centro(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_menu_centro', [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]

   ServicioReportes.cmenu_error(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_cMENU_ERROR', [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]
