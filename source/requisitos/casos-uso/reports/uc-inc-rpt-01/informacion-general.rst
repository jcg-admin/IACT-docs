.. _uc-inc-rpt-01-parte-01:

==============================
Parte 1 — Informacion general
==============================

1.1 Identificacion
==================

.. list-table::
 :widths: 30 70

 * - **ID**
   - UC_INC_RPT_01
 * - **Nombre**
   - Resolver Segmento del Usuario
 * - **Tipo**
   - UC de inclusion (``<<include>>``)
 * - **Modulo**
   - MOD_Reports
 * - **Relacion**
   - Incluido por: UC_RPT_01..UC_RPT_17
 * - **Criticidad**
   - Alta (afecta el scope de datos de
     todos los reportes)

1.2 Proposito
=============

Determinar los segmentos IVR que el usuario
puede consultar. El resultado limita el
scope de todos los reportes IVR — un usuario
solo ve datos de los segmentos a los que
tiene acceso.

Es un UC de inclusion: no puede ejecutarse
de forma independiente. Es incluido por
TODOS los UCs de reporte del modulo
MOD_Reports.

1.3 Motivacion
==============

El IVR opera sobre tres segmentos:
``nacional_A`` (DID 19028031),
``nacional_B`` (DID 19020001) y
``Puebla`` (DID 19020084). Un usuario puede
tener acceso a uno, varios o todos los
segmentos segun su configuracion RBAC.

Sin resolver el segmento, cualquier consulta
a la Base Analitica IVR devolveria datos
mezclados de todos los segmentos, lo que
viola el principio de separacion de
responsabilidades operacionales.
