.. _uc-rpt-17-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``ClientesReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ServicioReportes``
- ``MetricsCache``

11.2 Contrato
=============

::

   contract ClientesReportService:
     get(trimestre, segmentos, invoker, ctx)
       returns: ReporteClientes

11.3 Pseudocodigo
=================

::

   procedure get(trimestre, invoker, ctx):
       require AuthorizationGuard.has(invoker,
                   'view_unique_clients_reports')
       segmentos = SegmentResolver.resolve(invoker.id)
       cached = MetricsCache.get('clientes', trimestre, segmentos)
       if cached: return cached
       data = ServicioReportes.clientes(trimestre)
       reporte = filtrar_por_segmentos(data, segmentos)
       MetricsCache.set('clientes', trimestre, segmentos,
                        reporte, ttl=300)
       return reporte

11.4 Implementacion ServicioReportes
=====================================

::

   ServicioReportes.clientes(trimestre):
       with connections['ivr'].cursor() as cursor:
           cursor.callproc('sp_rpt_clientes', [trimestre])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row))
                   for row in cursor.fetchall()]

El SP retorna ``telefono_hashed`` (no el numero raw). La capa
de aplicacion NUNCA almacena ni loguea el numero de telefono
original (CNST-001 — sin PII en logs).
