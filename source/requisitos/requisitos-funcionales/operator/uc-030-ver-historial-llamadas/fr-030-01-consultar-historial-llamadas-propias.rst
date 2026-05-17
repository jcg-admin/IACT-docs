.. meta::
 :artefacto: FR-030.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-030-01:

======================================================================
FR-030.01: Consultar historial paginado de llamadas propias del agente
======================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-030.01
 * - **Nombre**
   - Consultar historial paginado de llamadas propias del agente
 * - **UC Origen**
   - UC_OPR_09: Ver Historial de Llamadas Propias
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
 * - **Módulo**
   - MOD_Operator
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar el historial de llamadas del agente autenticado CUANDO lo solicita, con período máximo de 7 días, sanitizando datos del llamante y paginando los resultados.

**Descripción:**

 Valida JWT (vista propia, sin RBAC adicional). Valida que el period del filtro no exceda 7 días. Query CallSession WHERE agent_id = invoker.id con los filtros. Sanitiza caller_hash (sin datos crudos del llamante, CNST-026). Devuelve lista paginada con disposition, duración y tags.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente solicita su historial de los últimos 3 días
 CUANDO GET /api/me/call-history/?period=3d
 ENTONCES 200 con lista paginada
 
 Escenario 1: Período válido
 DADO period ≤ 7 días
 ENTONCES resultados paginados con caller_hash
 
 Escenario 2: Período excedido
 DADO period = 10 días
 ENTONCES 422 período máximo 7 días

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_OPR_09: Ver Historial de Llamadas Propias
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-030-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_09
