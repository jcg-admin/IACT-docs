.. meta::
 :artefacto: FR-071.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-071-01:

==================================================================================
FR-071.01: Consultar resumen de salud del pipeline ETL con las últimas ejecuciones
==================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-071.01
 * - **Nombre**
   - Consultar resumen de salud del pipeline ETL con las últimas ejecuciones
 * - **UC Origen**
   - UC_PIP_01: Ver Estado del Pipeline ETL
 * - **Paso UC**
   - Pasos 1-5 del flujo principal
 * - **Módulo**
   - MOD_Pipeline
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar el resumen de salud del pipeline ETL CUANDO un usuario con view_pipeline_status lo solicita, mostrando las últimas 20 ejecuciones y el estado general calculado.

**Descripción:**

 Valida JWT + view_pipeline_status. Query Registro de Ejecuciones: últimas 20 ordenadas por started_at DESC. Construye ResumenSalud: última exitosa, si hay en ejecución, última fallida. Calcula estado_general: ok (reciente) / degradado (>N horas) / crítico (sin éxito reciente).

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor solicita estado ETL
 CUANDO GET /api/v1/etl/supervision/
 ENTONCES 200 con ResumenSalud y últimas 20 ejecuciones
 
 Escenario 1: Pipeline saludable
 DADO última exitosa hace < 2h
 ENTONCES estado_general=ok
 
 Escenario 2: Pipeline crítico
 DADO sin ejecución exitosa en 24h
 ENTONCES estado_general=critico

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005
 * - **UC**
   - UC_PIP_01: Ver Estado del Pipeline ETL
 * - **TEST**
   - TST-fr-071-01 (pendiente)

----

6. Historial
------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambio
 * - 1.0.0
   - 2026-05-04
   - Versión inicial derivada de UC_PIP_01
