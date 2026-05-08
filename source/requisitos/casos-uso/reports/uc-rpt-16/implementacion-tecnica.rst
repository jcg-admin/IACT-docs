.. _uc-rpt-16-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Componentes
================

- ``MenuIVRReportView`` (DRF APIView)
- ``AuthorizationGuard``
- ``SegmentResolver`` (``<<include>>`` UC_INC_RPT_01)
- ``ReportingService`` —
  ``cursor.callproc('sp_rpt_menu_redirigidos', ...)``
  + ``cursor.callproc('sp_rpt_menu_centro', ...)``
  + ``cursor.callproc('sp_rpt_cMENU_ERROR', ...)``
  sobre BD_IVR (TRIPLE SP, una sub-vista cada uno)
- ``MetricsCache``

11.2 Contrato
=============

::

   contract IvrNavigationReportService:
     get(period, vista, segmentos,
         invoker, ctx)
       returns: ReporteMenuIVR
       throws: SinPermiso, UserWithoutSegment,
               ValidationError, BDTimeout

   # vista: 'redirigidos' | 'menu_centro' | 'errores'
   # selecciona cual de los 3 SPs invocar.

11.3 Pseudocodigo
=================

::

   SP_BY_VISTA = {
     'redirigidos': 'sp_rpt_menu_redirigidos',
     'menu_centro': 'sp_rpt_menu_centro',
     'errores':     'sp_rpt_cMENU_ERROR',
   }

   procedure get(period, vista, invoker, ctx):
       require AuthorizationGuard.has(
                 invoker, 'view_reports')
       segmentos = SegmentResolver.resolve(
                     invoker.id)
       if not segmentos:
           raise UserWithoutSegment

       sp = SP_BY_VISTA[vista]
       key = ('menu_ivr', period, vista,
              hash(segmentos))
       cached = MetricsCache.get(key)
       if cached: return cached

       try:
           rows = ReportingService.callproc(
             sp, [period, segmentos])
       except BDTimeout:
           raise

       # Cada SP entrega filas pre-agregadas
       # para su sub-vista. Backend no
       # recalcula ni hace path mining.
       reporte = MenuReportOutput.from_rows(
           vista=vista, rows=rows)
       MetricsCache.set(key, reporte, ttl=300)
       return reporte

11.4 Restricciones cross-cutting
================================

- Read-only sobre BD_IVR (CNST-007).
- TRIPLE SP — uno por sub-vista. Backend
  selecciona el SP segun ``vista`` y solo
  parsea las filas.
- Filtro por segmento (CNST-008) aplicado
  por cada SP al recibir la lista.

