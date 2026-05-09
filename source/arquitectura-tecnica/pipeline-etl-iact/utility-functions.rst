.. meta::
 :artefacto: AT_PIPELINE_ETL_UTILITY_FUNCTIONS
 :tipo: Especificacion de Implementacion — Nivel 0
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 0
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_utility_functions:

==============================================================
Nivel 0 — Funciones de utilidad y schema fuente
==============================================================

Pre-requisito de todos los demas niveles. Cubre:

- Schema de las tablas fuente del cliente
  (``tbl_historico_tN_YYYY``).
- Condiciones de calidad observadas y su tratamiento.
- 7 funciones SQL de utilidad usadas por todos los SPs ETL
  y SPs de reporte.

----

Schema de cada tabla ``tbl_historico_tN_YYYY``
==============================================

Las 6 tablas fuente tienen el mismo schema. ``tN`` es el
trimestre (t1, t2, t3, t4) y ``YYYY`` el año.

.. list-table::
 :widths: 22 18 60
 :header-rows: 1

 * - Columna
   - Tipo
   - Descripcion
 * - ``dFecha``
   - DATE
   - Fecha de la llamada — filtro principal del ETL
 * - ``dHoraInicio``
   - DATETIME
   - Inicio — 38.8% de registros tienen ini > fin (G-29)
 * - ``dHoraFin``
   - DATETIME
   - Fin — puede ser anterior al inicio (bug G-29)
 * - ``cDID_800Transfer``
   - VARCHAR(20)
   - DID de entrada: ``19028031`` / ``19020001`` /
     ``19020084``
 * - ``cDID_Centro_Transferencia``
   - VARCHAR(50)
   - VDN destino — requiere normalizacion NK90
 * - ``cMenu``
   - VARCHAR(100)
   - Menu IVR navegado — mixed case, puede ser NULL/vacio
 * - ``cOpcion``
   - VARCHAR(100)
   - Opcion dentro del menu — NULLABLE
 * - ``cTelefono_Origen``
   - VARCHAR(20)
   - ANI — siempre presente
 * - ``cTelefono_Digitado``
   - VARCHAR(20)
   - Numero digitado — 21.2% NULL
 * - ``cEtiquetacliente``
   - VARCHAR(200)
   - Etiquetas CSV raw por registro

Condiciones de calidad observadas
----------------------------------

.. list-table::
 :widths: 32 16 52
 :header-rows: 1

 * - Condicion
   - Prevalencia
   - Tratamiento
 * - ``dHoraInicio > dHoraFin`` (G-29)
   - 38.8%
   - ``fn_duracion_seg()`` usa ABS(TIMESTAMPDIFF)
 * - ``cMenu IS NULL`` o vacio
   - ~8%
   - ``fn_normalizar_menu()`` → sentinel ``'VACIO'``
 * - ``cDID_Centro = 'cliente_colgo'``
   - 27.4%
   - ``fn_normalizar_centro()`` → sentinel
     ``'CLIENTE_COLGO'``
 * - ``cDID_Centro`` NULL o vacio
   - 1.3%
   - → sentinel ``'CASO_NULL'``
 * - ``cDID_Centro`` solo ceros
   - ~0.75% Puebla Q02+
   - → sentinel ``'CASO_ERROR_CEROS'``
 * - ``cDID_Centro`` NK90 longitud > 10
   - 5.67%
   - → ``LEFT(campo, LENGTH-10)``
 * - ``cDID_Centro`` char no numerico
   - 0.05%
   - → sentinel ``'ERROR_CARACTER_INICIAL'``
 * - ``cTelefono_Digitado IS NULL``
   - 21.2%
   - → columna ``no_digito_telefono += 1``
 * - ``cMenu`` contiene telefono
   - 1.2%
   - Pasa tal cual — ``sp_rpt_cMENU_ERROR`` lo detecta

Restricciones de acceso
------------------------

.. list-table::
 :widths: 38 62
 :header-rows: 1

 * - Restriccion
   - Impacto
 * - GRANT SELECT (CNST-ETL-001)
   - No se crean indices en la fuente
 * - Sin indices en ``tbl_historico_*`` (CNST-ETL-005)
   - Full table scan en cada corrida ETL
 * - Produccion en MariaDB 10.1.48 (CNST-ETL-007)
   - Sin window functions — subconsultas y variables
     de sesion
 * - Nombre de tabla dinamico (CNST-ETL-008)
   - ``PREPARE/EXECUTE`` obligatorio en SPs ETL

----

Las 7 funciones de utilidad
=============================

Resumen
-------

.. code-block:: text

   fn_did_segmento(p_did)
     '19028031' → 'nacional_A'
     '19020001' → 'nacional_B'
     '19020084' → 'puebla'
     cualquier otro → 'desconocido'
     Usada por: sp_etl_base_detalle, sp_etl_base_clientes

   fn_normalizar_menu(p_menu)
     NULL / '' / 'sin cMenu' → 'VACIO'
     cualquier otro → pass-through (mixed case)
     Usada por: sp_etl_base_detalle

   fn_normalizar_centro(p_centro)
     Orden de ramas es critico — 'cliente_colgo' antes que LENGTH > 10
     NULL/vacio              → 'CASO_NULL'
     'cliente_colgo'         → 'CLIENTE_COLGO'
     solo ceros              → 'CASO_ERROR_CEROS'
     char no numerico inicio → 'ERROR_CARACTER_INICIAL'
     LENGTH > 10             → LEFT(campo, LENGTH-10)  -- NK90
     valor limpio            → pass-through
     Usada por: sp_etl_base_detalle

   fn_duracion_seg(p_ini, p_fin)
     Retorna ABS(TIMESTAMPDIFF(SECOND, p_ini, p_fin))
     Maneja G-29 (38.8% tienen ini > fin) con ABS()
     NULL en cualquier argumento → 0
     Usada por: sp_rpt_centros_xsegmento (no en el ETL)

   ivr_es_dia_semana(p_fecha)
     RETURN DAYOFWEEK(p_fecha) NOT IN (1, 7)
     TRUE  = lunes a viernes
     FALSE = sabado o domingo
     El IVR opera 7 dias — festivos no aplican (datos confirman
     volumen normal en dias festivos)
     Usada por: sp_etl_base_detalle, ivr_contar_dias_semana,
                ivr_agregar_dias_semana, sp_rpt_centros_xsegmento

   ivr_contar_dias_semana(p_ini, p_fin)
     COUNT de dias lun-vie en el rango [p_ini, p_fin] inclusive
     O(n dias) — aceptable para rangos de un quarter (max 92 dias)
     Rango invertido → 0 (no error)
     Usada por: sp_rpt_centros_xsegmento

   ivr_agregar_dias_semana(p_fecha, p_n)
     Avanza p_n dias de semana desde p_fecha
     p_n = 0 → retorna p_fecha sin cambio
     Usada por: sp_rpt_centros_xsegmento (fechas de seguimiento SLA)

Detalle: ``fn_did_segmento(p_did)``
------------------------------------

Mapea DID de entrada al segmento canonico del IVR. Los 3 DIDs
operativos del cliente son fijos.

.. code-block:: sql

   CREATE FUNCTION fn_did_segmento(p_did VARCHAR(20))
   RETURNS VARCHAR(20)
   DETERMINISTIC
   BEGIN
       RETURN CASE p_did
           WHEN '19028031' THEN 'nacional_A'
           WHEN '19020001' THEN 'nacional_B'
           WHEN '19020084' THEN 'puebla'
           ELSE 'desconocido'
       END;
   END;

Detalle: ``fn_normalizar_centro(p_centro)``
--------------------------------------------

El **orden de ramas es critico**. La rama ``'cliente_colgo'``
debe evaluarse antes que ``LENGTH > 10`` porque
``'cliente_colgo'`` tiene longitud 13 y caeria en NK90 si se
evaluara primero.

.. code-block:: sql

   CREATE FUNCTION fn_normalizar_centro(p_centro VARCHAR(50))
   RETURNS VARCHAR(50)
   DETERMINISTIC
   BEGIN
       IF p_centro IS NULL OR TRIM(p_centro) = '' THEN
           RETURN 'CASO_NULL';
       ELSEIF p_centro = 'cliente_colgo' THEN
           RETURN 'CLIENTE_COLGO';
       ELSEIF p_centro REGEXP '^0+$' THEN
           RETURN 'CASO_ERROR_CEROS';
       ELSEIF p_centro NOT REGEXP '^[0-9]' THEN
           RETURN 'ERROR_CARACTER_INICIAL';
       ELSEIF LENGTH(p_centro) > 10 THEN
           RETURN LEFT(p_centro, LENGTH(p_centro) - 10);
       ELSE
           RETURN p_centro;
       END IF;
   END;

Detalle: ``ivr_es_dia_semana(p_fecha)``
----------------------------------------

Independencia del cliente. El IVR opera 7 dias y los datos
confirman volumen normal en festivos nacionales — por eso no
se mantiene un catalogo de festivos. Solo se distingue entre
lunes-viernes y sabado-domingo.

.. code-block:: sql

   CREATE FUNCTION ivr_es_dia_semana(p_fecha DATE)
   RETURNS BOOLEAN
   DETERMINISTIC
   BEGIN
       RETURN DAYOFWEEK(p_fecha) NOT IN (1, 7);
       -- DAYOFWEEK: 1=domingo, 2=lunes, ..., 7=sabado
   END;

Detalle: ``ivr_contar_dias_semana(p_ini, p_fin)``
---------------------------------------------------

O(n dias) iterando desde ``p_ini`` hasta ``p_fin``. Aceptable
para rangos de un quarter (max 92 dias).

.. code-block:: sql

   CREATE FUNCTION ivr_contar_dias_semana(p_ini DATE, p_fin DATE)
   RETURNS INT
   DETERMINISTIC
   BEGIN
       DECLARE v_count INT DEFAULT 0;
       DECLARE v_cur DATE DEFAULT p_ini;

       IF p_ini > p_fin THEN
           RETURN 0;
       END IF;

       WHILE v_cur <= p_fin DO
           IF ivr_es_dia_semana(v_cur) THEN
               SET v_count = v_count + 1;
           END IF;
           SET v_cur = DATE_ADD(v_cur, INTERVAL 1 DAY);
       END WHILE;
       RETURN v_count;
   END;

----

.. seealso::

 - :doc:`triggers` — disparo del ETL.
 - :doc:`orchestration` — ``sp_etl_maestro`` que coordina
   los SPs.
 - :doc:`etl-procedures` — SPs ETL que usan estas funciones.
 - :doc:`/arquitectura-tecnica/modulos/pipeline/index` —
   ARQ_MOD_004 perspectiva de monitoreo.
