.. meta::
 :artefacto: AT_PIPELINE_ETL_REPORT_PROCEDURES
 :tipo: Especificacion de Implementacion — Nivel 5
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 5
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_report_procedures:

==============================================================
Nivel 5 — SPs de reporte (sp_rpt_*)
==============================================================

Siete SPs leen ``base_ivr_detalle`` y ``base_ivr_clientes``
y devuelven result-sets para Django REST. Ningun SP de este
nivel toca ``tbl_historico_*`` — todo el costo de scan ya
fue pagado por el ETL.

.. list-table::
 :widths: 30 40 30
 :header-rows: 1

 * - SP
   - Lee de
   - Result-set
 * - ``sp_rpt_centros_transferencia``
   - ``base_ivr_detalle``
   - filas por ``centro_transferencia``
 * - ``sp_rpt_centros_xsegmento``
   - ``base_ivr_detalle``
   - filas por ``segmento × centro``
 * - ``sp_rpt_llamadas_abandonadas``
   - ``base_ivr_detalle``
   - agregado de ``no_digito_telefono``
 * - ``sp_rpt_menu_redirigidos``
   - ``base_ivr_detalle``
   - filas por ``menu``
 * - ``sp_rpt_menu_centro``
   - ``base_ivr_detalle``
   - filas por ``menu × centro``
 * - ``sp_rpt_cMENU_ERROR``
   - ``base_ivr_detalle``
   - filas con ``menu = 'ERROR'``
 * - ``sp_rpt_clientes``
   - ``base_ivr_clientes``
   - 3 filas por quarter (clientes unicos)

----

Patron comun
=============

Todos los SPs de reporte siguen el mismo contrato:

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_<nombre>(
       IN p_quarter VARCHAR(10)    -- 'Q02_26'
   )
   BEGIN
       SELECT <columnas>
       FROM base_ivr_detalle              -- o base_ivr_clientes
       WHERE trimestre = p_quarter
         [AND <filtro especifico>]
       GROUP BY <grain del reporte>
       ORDER BY <criterio del reporte>;
   END;

Sin parametros adicionales — el quarter es el unico input.
Sin filtros por mes (el grain ya esta agregado por mes en
``base_ivr_detalle``; el reporte muestra el quarter completo).

----

``sp_rpt_centros_transferencia``
==================================

Ranking de centros por volumen total. Lee ``base_ivr_detalle``
agregando los 3 meses del quarter.

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_centros_transferencia(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           centro_transferencia,
           SUM(total_llamadas)        AS total_llamadas,
           SUM(misma_linea)           AS misma_linea,
           SUM(linea_diferente)       AS linea_diferente,
           SUM(no_digito_telefono)    AS no_digito_telefono
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
       GROUP BY centro_transferencia
       ORDER BY total_llamadas DESC;
   END;

----

``sp_rpt_centros_xsegmento``
==============================

Centros por segmento, con desglose entre-semana / fin-de-semana.
Aprovecha ``llamadas_entre_semana`` pre-computado en el ETL —
sin segundo scan a la fuente.

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_centros_xsegmento(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           segmento,
           centro_transferencia,
           SUM(total_llamadas)         AS total_llamadas,
           SUM(llamadas_entre_semana)  AS llamadas_entre_semana,
           SUM(llamadas_fines_semana)  AS llamadas_fines_semana
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
       GROUP BY segmento, centro_transferencia
       ORDER BY segmento, total_llamadas DESC;
   END;

----

``sp_rpt_llamadas_abandonadas``
=================================

Llamadas en las que el usuario no digito numero (``no_digito_telefono``).

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_llamadas_abandonadas(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           segmento,
           menu,
           opcion,
           SUM(no_digito_telefono)  AS abandonadas,
           SUM(total_llamadas)      AS total
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
         AND no_digito_telefono > 0
       GROUP BY segmento, menu, opcion
       ORDER BY abandonadas DESC;
   END;

----

``sp_rpt_menu_redirigidos``
=============================

Distribucion por opcion de menu (excluye ``SIN_OPCION``).

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_menu_redirigidos(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           menu,
           opcion,
           SUM(total_llamadas)  AS total_llamadas
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
         AND opcion <> 'SIN_OPCION'
       GROUP BY menu, opcion
       ORDER BY menu, total_llamadas DESC;
   END;

----

``sp_rpt_menu_centro``
=======================

Cruzado ``menu × centro_transferencia``.

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_menu_centro(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           menu,
           centro_transferencia,
           SUM(total_llamadas)  AS total_llamadas
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
       GROUP BY menu, centro_transferencia
       ORDER BY menu, total_llamadas DESC;
   END;

----

``sp_rpt_cMENU_ERROR``
=======================

Filas en las que ``fn_normalizar_menu()`` clasifico el menu
como ``ERROR`` — diagnostico de calidad del catalogo.

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_cMENU_ERROR(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           segmento,
           centro_transferencia,
           opcion,
           SUM(total_llamadas)  AS total_llamadas
       FROM base_ivr_detalle
       WHERE trimestre = p_quarter
         AND menu = 'ERROR'
       GROUP BY segmento, centro_transferencia, opcion
       ORDER BY total_llamadas DESC;
   END;

----

``sp_rpt_clientes``
=====================

Clientes unicos por segmento. Lee ``base_ivr_clientes``
(3 filas por quarter).

.. code-block:: sql

   CREATE PROCEDURE sp_rpt_clientes(
       IN p_quarter VARCHAR(10)
   )
   BEGIN
       SELECT
           segmento,
           clientes_unicos
       FROM base_ivr_clientes
       WHERE trimestre = p_quarter
       ORDER BY segmento;
   END;

----

.. seealso::

 - :doc:`intermediate-tables` — DDL de ``base_ivr_*``.
 - :doc:`utility-functions` — funciones usadas en el ETL
   que materializa estas tablas.
 - :doc:`django-rest-integration` — capa que invoca estos
   SPs via ``cursor.callproc()``.
