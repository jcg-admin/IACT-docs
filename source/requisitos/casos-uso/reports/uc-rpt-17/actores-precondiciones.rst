.. _uc-rpt-17-parte-02:

=====================================
Parte 2 — Actores y precondiciones
=====================================

2.1 Actores
===========

- **User con funcion**
  ``view_reports``
- **ReportingService** —
  ``cursor.callproc('sp_rpt_clientes',
  [period, segments])`` sobre BD_IVR.
- **ETL upstream** (sp_etl_base_clientes)
  — proceso previo que aplica hash
  unidireccional a ``cTelefono_Origen``
  antes de escribir ``base_ivr_clientes``;
  fuera del scope del UC pero
  precondicion de los datos.

2.2 Precondiciones
==================

Auth + RBAC + segmento. BD_IVR accesible
con ``base_ivr_clientes`` ya anonimizada
por el ETL; SP ``sp_rpt_clientes``
instalado y operando read-only sobre el
hash.

2.3 Postcondiciones
===================

Sin escrituras (read-only sobre BD_IVR
y BD operativa, CNST-007). Backend NUNCA
manipula PII raw — solo lee
``telefono_hashed``.

2.4 Datos de entrada
====================

::

   GET /api/reports/unique-clients/
       ?period=last_30d

2.5 Datos de salida
===================

::

   {
     period,
     distinct_clients_count,
     avg_calls_per_client,
     recurrencia_distribution: [
       { calls: 1, clients_count, pct },
       { calls: 2, clients_count, pct },
       { calls: "3+", clients_count, pct }
     ],
     new_vs_returning: {
       new_count, returning_count
     },
     top_volume_anonymized: [
       { client_hash_prefix,
         calls_count }, ...
     ]
   }
