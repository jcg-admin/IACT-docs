.. meta::
 :artefacto: FR-060.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-060-01:

=====================================================
FR-060.01: Consultar logs específicos del proceso ETL
=====================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-060.01
 * - **Nombre**
   - Consultar logs específicos del proceso ETL
 * - **UC Origen**
   - UC_LOG_02: Ver Logs del Proceso ETL
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
 * - **Módulo**
   - MOD_Logs
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar únicamente logs del proceso ETL CUANDO un usuario autorizado los consulta, filtrando implícitamente por servicio ETL.

**Descripción:**

 Idéntico a UC_LOG_01 pero con filtro implícito service LIKE 'etl-%' en la query al LogStore. Rango ≤ 24h. Sanitización estándar.

----

3. Criterio de Aceptación
-------------------------

::

 DADO operador consulta logs ETL
 CUANDO GET
 ENTONCES solo logs de servicios etl-* sanitizados
 
 Escenario 1: Filtro implícito
 DADO sin filtro de servicio en request
 ENTONCES solo logs etl-* en respuesta

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005
 * - **UC**
   - UC_LOG_02: Ver Logs del Proceso ETL
 * - **TEST**
   - TST-fr-060-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_02
