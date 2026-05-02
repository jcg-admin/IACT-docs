.. _uc-rpt-15-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``TransferenciasReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ServicioReportes``
- ``MetricsCache``

11.2 Contrato
=============

::

   contract TransferenciasReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteTransferencias

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker, 'view_transfer_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('transferencias', trimestre, segmentos)
       if cached: return cached
       centros = ServicioReportes.centros_transferencia(trimestre)
       centros_seg = ServicioReportes.centros_xsegmento(trimestre)
       reporte = construir_reporte_transferencias(
           centros, centros_seg, segmentos
       )
       MetricsCache.set('transferencias', trimestre, segmentos,
                        reporte, ttl=300)
       return reporte

11.4 Implementacion ServicioReportes
=====================================

::

   ServicioReportes.centros_transferencia(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_centros_transferencia',
                           [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]

   ServicioReportes.centros_xsegmento(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_centros_xsegmento',
                           [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]
