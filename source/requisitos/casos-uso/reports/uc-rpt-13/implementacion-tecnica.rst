.. _uc-rpt-13-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``AbandonoReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ServicioReportes``
- ``MetricsCache``

11.2 Contrato
=============

::

   contract AbandonoReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteAbandono

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_queue_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('abandono', trimestre, segmentos)
       if cached: return cached
       reporte = ServicioReportes.llamadas_abandonadas(trimestre)
       reporte_filtrado = filtrar_por_segmentos(reporte, segmentos)
       MetricsCache.set('abandono', trimestre, segmentos,
                        reporte_filtrado, ttl=300)
       return reporte_filtrado

11.4 Implementacion ServicioReportes
=====================================

::

   ServicioReportes.llamadas_abandonadas(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_llamadas_abandonadas',
                           [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]

El SP retorna datos de todos los segmentos. La capa de servicio
filtra por los segmentos del usuario antes de retornar.
