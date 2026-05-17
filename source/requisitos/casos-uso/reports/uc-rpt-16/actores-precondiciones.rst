.. _uc-rpt-16-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **User con funcion** ``view_reports``
- **ReportingService** —
  ``cursor.callproc('sp_rpt_menu_
  redirigidos', ...)`` +
  ``cursor.callproc('sp_rpt_menu_centro',
  ...)`` + ``cursor.callproc('sp_rpt_
  cMENU_ERROR', ...)`` sobre BD_IVR
  (TRIPLE SP, una sub-vista cada uno).

2.2 Precondiciones
==================

Auth + RBAC + segmento. BD_IVR accesible
y los SPs ``sp_rpt_menu_redirigidos``,
``sp_rpt_menu_centro`` y
``sp_rpt_cMENU_ERROR`` instalados.

2.3 Postcondiciones
===================

Sin escrituras (read-only sobre BD_IVR
y BD operativa, CNST-007).

2.4 Datos de entrada
====================

::

   GET /api/reports/ivr/
       ?period=last_30d
       &filter[ivr_id]=...

Detalle path:

::

   GET /api/reports/ivr/{ivr_id}/paths/

2.5 Datos de salida
===================

::

   {
     period,
     totals: { entries, completed,
                dropped, avg_time_seconds },
     root_distribution: [
       { option, count, pct }, ...
     ],
     drop_off_by_node: [
       { node_id, drop_rate_pct }, ...
     ],
     top_paths: [
       { path: [opt1, opt2, ...],
         count }, ...
     ]
   }
