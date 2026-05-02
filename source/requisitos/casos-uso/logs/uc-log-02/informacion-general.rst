.. _uc-log-02-parte-01:

==============================
Parte 1 — Informacion general
==============================

.. list-table::
 :widths: 30 70

 * - **ID**
   - UC_LOG_02
 * - **BReq**
   - BReq-005
 * - **Funcion RBAC**
   - ``view_etl_logs``

1.1 Proposito
=============

Variante de UC_LOG_01 enfocada en ETL.
Filtra automaticamente service ∈
{etl-runner, etl-validator,
etl-transformer, ...}.

1.2 Restricciones
=================

CNST-009. CNST-026 sin PII.

1.3 Diferencia
==============

Funcional identico a UC_LOG_01; solo
scope distinto. Funcion separada para
permisos granular: data engineers ven
ETL logs, no sistema general.
