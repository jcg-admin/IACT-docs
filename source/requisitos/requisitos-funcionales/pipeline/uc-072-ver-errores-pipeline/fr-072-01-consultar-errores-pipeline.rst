.. meta::
 :artefacto: FR-072.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-072-01:

===========================================================================
FR-072.01: Consultar ejecuciones fallidas del pipeline con mensaje de error
===========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-072.01
 * - **Nombre**
   - Consultar ejecuciones fallidas del pipeline con mensaje de error
 * - **UC Origen**
   - UC_PIP_02: Ver Errores del Pipeline
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

 El sistema DEBE retornar las ejecuciones fallidas del pipeline CUANDO un usuario con view_pipeline_errors las consulta, con filtros por período y trimestre y el mensaje de error de cada una.

**Descripción:**

 Valida JWT + view_pipeline_errors. Valida filtros (period dentro del rango CNST_018, trimestre en formato válido). Query Registro de Ejecuciones WHERE estado='fallido' + filtros + paginación. Retorna mensaje_error de cada ejecución fallida.

----

3. Criterio de Aceptación
-------------------------

::

 DADO operador consulta errores del Q1
 CUANDO GET con trimestre=Q1_25
 ENTONCES lista de ejecuciones fallidas con mensaje_error
 
 Escenario 1: Sin errores en período
 DADO sin ejecuciones fallidas
 ENTONCES lista vacía 200

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005
 * - **UC**
   - UC_PIP_02: Ver Errores del Pipeline
 * - **TEST**
   - TST-fr-072-01 (pendiente)

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
   - Versión inicial derivada de UC_PIP_02
